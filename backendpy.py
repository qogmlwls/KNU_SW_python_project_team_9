from fastapi import FastAPI, Query
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

reader = easyocr.Reader(['ko'], gpu=False)

# 이미지 태그에서 OCR 텍스트 추출
def extract_text_from_images(image_tags):
    all_text = ""
    for img in image_tags:
        src = img.get("src")
        if not src or src.startswith("data:"):
            continue  # base64 인라인 이미지 혹은 빈 src는 건너뜀
        try:
            response = requests.get(src, timeout=5)
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if image is not None:
                result = reader.readtext(image)
                for detection in result:
                    all_text += detection[1] + " "
        except Exception as e:
            print(f"[Image OCR Error] Failed to process image: {e}")
            continue
    return all_text

# 전체 페이지 스크린샷에서 OCR
def extract_text_from_full_screenshot(driver):
    MAX_HEIGHT = 5000
    total_height = driver.execute_script("return document.body.scrollHeight")
    adjusted_height = min(total_height, MAX_HEIGHT)

    driver.set_window_size(1200, adjusted_height)
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(0.5)

    screenshot = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(screenshot))

    # PIL → numpy → BGR (OpenCV 호환)
    np_image = np.array(image)
    image_bgr = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

    result = reader.readtext(image_bgr)
    return " ".join([text for (_, text, _) in result])

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
        except:
            pass

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title_tag = soup.select_one(".se-title-text") or soup.select_one(".pcol1")
        content_tag = soup.select_one(".se-main-container") or soup.select_one("#postViewArea")

        title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
        content = content_tag.get_text(separator=' ', strip=True) if content_tag else ""

        full_text = content + " " + soup.get_text(separator=' ', strip=True)

        # 이미지 OCR
        image_tags = soup.find_all("img")
        image_text = extract_text_from_images(image_tags)

        # 전체 화면 OCR
        screenshot_text = extract_text_from_full_screenshot(driver)

        # 전체 텍스트 통합
        total_text = " ".join([full_text, image_text, screenshot_text])

        # 광고 키워드 매칭
        matched_keywords = [kw for kw in AD_KEYWORDS if kw in total_text]
        is_ad = len(matched_keywords) > 0

        return {
            "title": title,
            "category": "광고 문구 있음" if is_ad else "광고 문구 없음",
            "matched_keywords": matched_keywords
        }

    finally:
        driver.quit()

# API 엔드포인트
@app.get("/check_blog")
def check_blog(url: str = Query(...)):
    return analyze_blog(url)
