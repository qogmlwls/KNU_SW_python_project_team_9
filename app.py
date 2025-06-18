from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import requests
import time

from io import BytesIO
import easyocr
from PIL import Image
import numpy as np
import cv2
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64
import logging

# FastAPI 및 CORS 설정
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 광고 키워드 정의
COMPENSATION_KEYWORDS = [
    "원고료", "수수료", "광고료", "연구료", "광고비", "소정의",
    "대가를 받고", "금전적 보상", "지원받아 작성", "지급받아 작성"
]

PRODUCT_SPONSORSHIP_KEYWORDS = [
    "협찬", "협찬을", "협찬을 받아", "협찬받고", "협찬받아",
    "지원받은", "지원받아", "지원을 받아",
    "제공받아", "제공을 받아", "제공받은", "제공받았습니다",
    "무료제공", "제품 협찬", "서비스 제공",
    "무상 제공", "체험단", "제공받은 후기", "협찬을 통해 작성", "제품 지원"
]

SPONSORSHIP_RELATION_KEYWORDS = [
    "업체", "업체의", "해당 업체의", "해당 업체로부터", "업체로부터",
    "해당업체의 협찬", "업체의 협찬", "정보성 후기글", "광고성", "제휴",
    "소속", "후원", "협력", "브랜드로부터", "제공받았지만 솔직하게",
    "지원받아 솔직하게"
]

FIRST_KEYWORDS = [
    "포스팅", "본 포스팅은", "본 포스팅", "이 포스팅은"
]

AD_KEYWORDS = sorted(set(
    COMPENSATION_KEYWORDS +
    PRODUCT_SPONSORSHIP_KEYWORDS +
    SPONSORSHIP_RELATION_KEYWORDS +
    FIRST_KEYWORDS
))

# EasyOCR 설정
reader = easyocr.Reader(['ko'], gpu=False)

# 이미지 전처리
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary

# 키워드 매칭
def match_keywords(text, keywords):
    return [kw for kw in keywords if kw in text]

# Base64 이미지 디코딩 및 OCR
def decode_base64_image(data):
    try:
        if not data.startswith("data:image/"):
            return ""
        header, encoded = data.split(",", 1)
        if len(encoded) % 4 != 0:
            logger.warning(f"Invalid Base64 data: {encoded[:30]}... (truncated)")
            return ""
        img_data = BytesIO(base64.b64decode(encoded))
        image = Image.open(img_data).convert("RGB")
        np_image = np.array(image)
        preprocessed_image = preprocess_image(np_image)
        result = reader.readtext(preprocessed_image)
        return " ".join([detection[1] for detection in result])
    except Exception as e:
        logger.error(f"[Base64 Image OCR Error] Failed to process image: {e}")
        return ""

# 이미지 OCR 처리
def extract_text_from_images(image_tags):
    def process_image(src):
        try:
            if src.startswith("data:image"):
                return decode_base64_image(src)

            response = requests.get(src, timeout=5)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if image is None:
                return ""

            h, w = image.shape[:2]
            max_dim = 1000
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                image = cv2.resize(image, (int(w * scale), int(h * scale)))

            preprocessed_image = preprocess_image(image)
            result = reader.readtext(preprocessed_image)
            return " ".join([detection[1] for detection in result])
        except Exception as e:
            logger.error(f"[OCR Error] Failed to process image: {e}")
            return ""

    image_texts = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_image, img.get("src")) for img in image_tags if img.get("src")]
        for future in as_completed(futures):
            image_texts.append(future.result())

    return " ".join(filter(None, image_texts))

# 블로그 분석 함수
def analyze_blog(url: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(2)

        try:
            driver.switch_to.frame("mainFrame")
        except Exception as e:
            logger.warning(f"Failed to switch to mainFrame: {e}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title_tag = soup.select_one(".se-title-text") or soup.select_one(".pcol1")
        content_tag = soup.select_one(".se-main-container") or soup.select_one("#postViewArea")

        title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
        content = content_tag.get_text(separator=' ', strip=True) if content_tag else ""

        logger.info("=== HTML Content Text Extracted ===")

        image_tags = soup.find_all("img")
        image_text = extract_text_from_images(image_tags)
        logger.info("=== OCR Image Text Extracted ===")

        total_text = " ".join(filter(None, [content.strip(), image_text]))

        matched_keywords = match_keywords(total_text, AD_KEYWORDS)
        is_ad = len(matched_keywords) > 0

        return {
            "title": title,
            "category": "광고 문구 있음" if is_ad else "광고 문구 없음",
            "matched_keywords": matched_keywords
        }

    except Exception as e:
        logger.error(f"Error analyzing blog: {e}")
        raise HTTPException(status_code=500, detail="블로그 분석 중 오류가 발생했습니다.")
    finally:
        driver.quit()

# API 엔드포인트
@app.get("/check_blog")
def check_blog(url: str = Query(...)):
    return analyze_blog(url)
