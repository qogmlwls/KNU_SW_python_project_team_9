# 네이버 블로그 제목, 본문 가져오기
# 이미지, 동영상 가져오기 (변수값에 넣기, 갯수)
# 광고 블로그인지 판별하기
# 결과 출력

from fastapi import FastAPI, Query
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = FastAPI()

# 광고 관련 키워드 (원하는 만큼 추가 가능)
ad_keywords = [
    "#광고", "#협찬", "#체험단", "#PPL", "소정의 원고료", "원고료를 지원받아", "제품을 제공받아", 
    "대가를 받고", "후원을 받아", "협찬을 받아", "리뷰 요청", "서포터즈", "이 글은 협찬을 받아 작성되었습니다"
]


def analyze_blog(url: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)
        driver.switch_to.frame("mainFrame")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title_tag = soup.select_one(".se-title-text") or soup.select_one(".pcol1")
        content_tag = soup.select_one(".se-main-container") or soup.select_one("#postViewArea")

        title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
        content = content_tag.get_text(separator=' ', strip=True) if content_tag else "본문 없음"

        is_ad = any(keyword in content for keyword in AD_KEYWORDS)
        return {
            "title": title,
            "summary": content[:300],
            "category": "광고" if is_ad else "일반"
        }
    finally:
        driver.quit()

@app.get("/check_blog")
def check_blog(url: str = Query(...)):
    return analyze_blog(url)
