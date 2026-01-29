import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- 설정 ---
LOGIN_URL = "https://hr.workup.plus/cloudhr/1.0/login"
USER_ID = "leonprof1010@idlook.co.kr"
USER_PW = "tmdalsdl11!"
SAVE_FOLDER = "crawled_data"

if not os.path.exists(SAVE_FOLDER): os.makedirs(SAVE_FOLDER)

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🌐 사이트 접속 중...")
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 15)

    print("🔑 로그인 정보 입력 중...")
    
    # 1. 아이디 입력 (알려주신 userId 사용)
    id_field = wait.until(EC.visibility_of_element_located((By.ID, "userId")))
    id_field.send_keys(USER_ID)

    # 2. 비밀번호 입력 (ID 대신 'type=password' 속성으로 찾기)
    # 이렇게 하면 ID가 password든 userPw든 상관없이 찾아냅니다.
    pw_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    pw_field.send_keys(USER_PW)

    print("🖱️ 로그인 버튼 클릭...")
    # 3. 로그인 버튼 (엔터 키 입력 또는 버튼 클릭)
    # 버튼을 찾기 어려울 경우, 비밀번호 칸에서 엔터를 치는 것이 가장 확실합니다.
    from selenium.webdriver.common.keys import Keys
    pw_field.send_keys(Keys.ENTER)

    # 로그인 후 페이지 전환 대기
    time.sleep(5)
    
    print(f"현재 URL: {driver.current_url}")
    
    # 4. 데이터 수집 및 엑셀 저장
    # (접속 성공 여부를 기록하는 기초 샘플)
    data = [{
        "수집시간": time.strftime('%Y-%m-%d %H:%M:%S'),
        "결과": "로그인 성공" if "login" not in driver.current_url else "로그인 실패",
        "현재URL": driver.current_url
    }]
    
    df = pd.DataFrame(data)
    save_path = os.path.join(SAVE_FOLDER, f"workup_report_{time.strftime('%H%M%S')}.xlsx")
    df.to_excel(save_path, index=False)
    
    print(f"✅ 엑셀 파일이 생성되었습니다: {save_path}")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    driver.save_screenshot("debug_error.png")
    print("📸 에러 화면을 'debug_error.png'로 저장했습니다.")

finally:
    # driver.quit()
    pass