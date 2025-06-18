//백엔드 코드 (이미지 검사 전)
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AD_KEYWORDS = [
    "#광고", "광고", "#협찬","협찬", "#체험단", "체험단", "#PPL", "원고료", "소정의 원고료", "지원받아", "제공받아", 
    "대가 받고", "후원 받아", "협찬 받아", "리뷰 요청", "서포터즈", "식사권", "제공 받아"
]

def analyze_blog(url: str):
    options = Options()
    options.add_argument("--headless")
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
        content = content_tag.get_text(separator=' ', strip=True) if content_tag else "본문 없음"

        is_ad = any(keyword in content for keyword in AD_KEYWORDS)

        images = soup.find_all("img")
        videos = soup.find_all("iframe")

        return {
            "title": title,
            "summary": content[:300],
            "image_count": len(images),
            "video_count": len(videos),
            "category": "광고 문구 있음" if is_ad else "광고 문구 없음"
        }
    finally:
        driver.quit()

@app.get("/check_blog")
def check_blog(url: str = Query(...)):
    return analyze_blog(url)
