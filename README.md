# 블로그 바이럴 탐지기 

블로그 내용을 끝까지 읽지 않아도, 광고 관련 키워드(예: "협찬", "소정의 원고료")가 본문에 포함되어 있는지 알려주는 프로그램입니다.
결과 예시 : "소정의 원고료", "협찬" 이 감지됨.


## 목적 및 주요 기능 설명

배경 : 일상생활에서 네이버 블로그를 검색하다 보면, 광고성 글인지 모르고 끝까지 읽은 후에야 광고임을 알게 되어 불편함을 느끼는 경우가 많았습니다.
이를 해결하기 위해, 블로그를 클릭하기 전에 광고 여부를 미리 확인할 수 있는 방법이 없을까 하는 문제의식에서 이 프로그램을 개발하게 되었습니다.

목적 : 사용자가 블로그를 클릭하기 전에 해당 글이 광고인지 아닌지를 사전에 인지할 수 있도록 돕는 것을 목적으로 합니다.

주요 기능 : 블로그의 본문(텍스트와 이미지)에서 광고 관련 키워드가 포함되어 있는지를 탐지하고, 감지된 경우 시각적으로 표시해주는 기능 
- 네이버 블로그 본문 수집
   입력된 url을 통해 블로그의 html 내용을 가져옵니다.
- 이미지 내 텍스트 추출 (OCR)
   광고 문구가 이미지 형태로 포함된 경우를 위해 이미지에서도 텍스트를 추출합니다.
- 광고 관련 키워드 탐지
   사전에 정의한 광고 관련 키워드가 블로그 본문에 포함되어있는지 문자열 비교를 통해 탐지합니다.
- 시각적 표시
   광고 관련 키워드가 감지된 경우, 해당 블로그 element의 배경색을 변경합니다.


## 설치 및 실행 방법

본 프로젝트는 다음과 같은 환경에서 설치 및 실행되었습니다:

서버 사양
- 하드웨어 : CPU: 4 rCore, RAM: 4 GB, HDD: SSD 50 GB, NETWORK: 10 Gbps
- 운영체제 : Ubuntu 20.04 LTS(64bit)
- 웹 브라우저 : Google chrome 137.0.7151.103
- 웹 드라이버 : ChromeDriver 137.0.7151.103

백앤드 설치 및 실행 방법
1. 서버 구축 및 환경 설정 진행
   1-1. git 설치 : sudo apt install git -y
   1-2. 프로젝트 가져오기 : git clone https://github.com/qogmlwls/KNU_SW_python_project_team_9.git
   app.py 가 위치한 폴더로 이동 ex. cd ~/KNU_SW_python_project_team_9
   라이브러리, 프로그램 설치 :
   sudo apt install python3 python3-pip -y
   sudo pip install easyocr selenium beautifulsoup4 requests
   * pip show easyocr 로 설치되었는지 확인*
   sudo pip install fastapi uvicorn
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt install ./google-chrome-stable_current_amd64.deb -y
   google-chrome --version (결과값 : 137.0.7151.103)
   **크롬 브라우저와 driver 버전이 같아야 함.
   wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.103/linux64/chromedriver-linux64.zip
   unzip chromedriver-linux64.zip
   sudo mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
   sudo chmod +x /usr/bin/chromedriver
   chromedriver --version
   pip install webdriver-manager
2. FastAPI 서버 실행
   uvicorn app:app --host 0.0.0.0 --port 80 &

프론트앤드 설치 및 실행 방법
1. chrome-extension-test 폴더 다운로드
2. 크롬 브라우저에서 확장 프로그램 등록 (개발자 모드)
   크롬 주소창에 chrome://extensions/ 입력
   우측 상단의 [개발자 모드] 활성화
   압축해제된 확장프로그램을 로드합니다 클릭
   chrome-extension-test 폴더 선택
3. 네이버 검색 > 블로그 화면으로 이동
  (ex. https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=%ED%98%91%EC%B0%AC) 


## 사용된 third-party 라이브러리

- FastAPI : 작업 요청을 받아 결과를 응답하는 API 서버를 만드는 데 사용됩니다.
- Selenium, beautifulsoup4, requests, webdriver-manager : 크롬 브라우저를 제어하여 블로그 본문(텍스트, 이미지 링크)을 추출하는 데 사용됩니다.
- easyocr, PIL, numpy, cv2 : 이미지에서 문자열 추출하는데 사용됩니다.

