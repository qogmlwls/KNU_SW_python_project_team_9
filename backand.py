# 네이버 블로그 제목, 본문 가져오기
# 이미지, 동영상 가져오기 (변수값에 넣기, 갯수)
# 광고 블로그인지 판별하기
# 결과 출력


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


# 광고 관련 키워드 (원하는 만큼 추가 가능)
ad_keywords = [
    "#광고", "#협찬", "#체험단", "#PPL", "소정의 원고료", "원고료를 지원받아", "제품을 제공받아", 
    "대가를 받고", "후원을 받아", "협찬을 받아", "리뷰 요청", "서포터즈", "이 글은 협찬을 받아 작성되었습니다"
]


# 크롬 드라이버 설정
options = Options()
options.add_argument('--headless')  # 창 없이 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# 크롤링할 블로그 글 URL
# url = 'https://blog.naver.com/아이디/글번호'  # 예: https://blog.naver.com/naver_diary/223456789012
url = 'https://blog.naver.com/chemist_sun/223856739539'  # 예: https://blog.naver.com/naver_diary/223456789012

driver.get(url)
time.sleep(2)  # 페이지 로딩 대기

# iframe 안으로 들어가기
driver.switch_to.frame('mainFrame')

# 현재 페이지 소스를 BeautifulSoup으로 파싱
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 제목 가져오기
title_tag = soup.select_one('.se-title-text') or soup.select_one('.pcol1')
title = title_tag.get_text(strip=True) if title_tag else '제목 없음'

# 본문 가져오기
content_tag = soup.select_one('.se-main-container') or soup.select_one('#postViewArea')
content = content_tag.get_text(strip=True) if content_tag else '본문 없음'

print("제목:", title)
print("본문:", content[:300], "...")  # 본문 앞 300자만 출력
#print("본문:", content)  # 본문 앞 300자만 출력


# 광고 판단
is_ad = any(keyword in content for keyword in ad_keywords)


print("분류:", "광고" if is_ad else "일반")


driver.quit()



