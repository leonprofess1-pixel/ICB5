import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# --- 설정 ---
LOGIN_URL = "https://hr.workup.plus/cloudhr/1.0/login"
TARGET_URL = "https://hr.workup.plus/cloudhr/1.0/view/work/approval/vacationApr"
USER_ID = "leonprof1010@idlook.co.kr"
USER_PW = "tmdalsdl11!"
TARGET_FILE = r"C:\Users\Administrator\OneDrive\OneDrive - IDLOOK\바탕 화면\연차사용내역_반자동.xlsm"

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🌐 사이트 접속 중...")
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 15)

    print("🔑 로그인 정보 입력 중...")
    
    # 1. 아이디 입력
    id_field = wait.until(EC.visibility_of_element_located((By.ID, "userId")))
    id_field.send_keys(USER_ID)

    # 2. 비밀번호 입력
    pw_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    pw_field.send_keys(USER_PW)

    print("🖱️ 로그인 중...")
    pw_field.send_keys(Keys.ENTER)
    time.sleep(5)
    
    print(f"✅ 로그인 성공!")
    
    # 3. 타겟 페이지로 이동
    print(f"📄 휴가 승인 페이지로 이동 중...")
    driver.get(TARGET_URL)
    time.sleep(3)
    
    # 4. "수신처리중" 선택
    print("🎯 결재상태 '수신처리중' 선택 중...")
    try:
        select_element = wait.until(EC.presence_of_element_located((By.ID, "searchApplStatusCd")))
        select = Select(select_element)
        select.select_by_value("31")  # 수신처리중
        print("✅ '수신처리중' 선택 완료!")
        time.sleep(2)
        
        # 검색 버튼 클릭 (있다면)
        try:
            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button.btn-search, input[type='submit']")
            search_button.click()
            print("🔍 검색 버튼 클릭!")
            time.sleep(3)
        except:
            print("ℹ️ 검색 버튼 없음 (자동 검색됨)")
    except Exception as e:
        print(f"⚠️ 드롭다운 선택 오류: {e}")
    
    # 5. IBSheet 데이터가 로드될 때까지 대기
    print("\n⏳ 데이터 로딩 대기 중...")
    time.sleep(5)
    
    # 6. BeautifulSoup으로 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 7. IBSheet 데이블에서 데이터 행 추출
    print("\n🔍 데이터 크롤링 중...")
    
    crawled_data = []
    
    # IBSheet의 데이터 행 찾기
    data_rows = soup.find_all('tr', class_='IBISUDataRow')
    
    print(f"✅ 발견된 데이터 행 수: {len(data_rows)}")
    
    for idx, row in enumerate(data_rows, 1):
        row_dict = {
            '번호': idx,
            '상태': '',
            '세부내역': '',
            '신청일': '',
            '결재상태': '',
            '소속': '',
            '사번': '',
            '성명': '',
            '직위': '',
            '근태명': '',
            '시작일': '',
            '종료일': '',
            '총일수': '',
            '적용일수': '',
            '시작시간': '',
            '종료시간': '',
            '적용시간': '',
            '취소여부': '',
            '신청사유': '',
            '첨부파일': ''
        }
        
        # 모든 td 셀 찾기
        cells = row.find_all('td')
        
        for cell in cells:
            classes = cell.get('class', [])
            
            # HideCol0로 시작하는 클래스에서 컬럼명 찾기
            col_name = None
            for cls in classes:
                if 'HideCol0' in cls:
                    col_name = cls.replace('HideCol0', '')
                    break
            
            if not col_name:
                continue
            
            # 셀 내용 추출
            cell_text = cell.get_text(strip=True)
            
            # 빈 값 처리
            if not cell_text or cell_text == '&nbsp;':
                cell_text = ''
            
            # 컬럼명에 따라 매핑
            if col_name == 'applYmd':
                row_dict['신청일'] = cell_text
            elif col_name == 'applStatusCd':
                row_dict['결재상태'] = cell_text
            elif col_name == 'orgNm':
                row_dict['소속'] = cell_text
            elif col_name == 'sabun':
                row_dict['사번'] = cell_text
            elif col_name == 'name':
                row_dict['성명'] = cell_text
            elif col_name == 'jikweeNm':
                row_dict['직위'] = cell_text
            elif col_name == 'gntNm':
                row_dict['근태명'] = cell_text
            elif col_name == 'sYmd':
                # 날짜 형식 변환: 2026-01-30 -> 20260130
                if cell_text and '-' in cell_text:
                    row_dict['시작일'] = cell_text.replace('-', '')
                else:
                    row_dict['시작일'] = cell_text
            elif col_name == 'eYmd':
                # 날짜 형식 변환: 2026-01-30 -> 20260130
                if cell_text and '-' in cell_text:
                    row_dict['종료일'] = cell_text.replace('-', '')
                else:
                    row_dict['종료일'] = cell_text
            elif col_name == 'holDay':
                row_dict['총일수'] = cell_text
            elif col_name == 'closeDay':
                row_dict['적용일수'] = cell_text
            elif col_name == 'reqSHm':
                row_dict['시작시간'] = cell_text
            elif col_name == 'reqEHm':
                row_dict['종료시간'] = cell_text
            elif col_name == 'requestHour':
                row_dict['적용시간'] = cell_text
            elif col_name == 'cancleYn':
                row_dict['취소여부'] = cell_text
            elif col_name == 'reason':
                row_dict['신청사유'] = cell_text
            elif col_name == 'btnFile':
                # 첨부파일이 있는지 확인
                if '다운로드' in cell_text:
                    row_dict['첨부파일'] = 'O'
                else:
                    row_dict['첨부파일'] = ''
        
        # 상태와 세부내역은 아이콘이므로 기본값 설정
        row_dict['상태'] = ''
        row_dict['세부내역'] = '📄'
        
        # 필수 데이터가 있는 행만 추가 (성명, 소속, 사번 중 하나라도 있어야 함)
        if row_dict['성명'] or row_dict['소속'] or row_dict['사번']:
            crawled_data.append(row_dict)
            print(f"행 {len(crawled_data)}: {row_dict['성명']} - {row_dict['근태명']} ({row_dict['시작일']})")
        else:
            print(f"행 {idx}: 빈 데이터 - 건너뜀")
    
    # 8. DataFrame 생성
    if crawled_data:
        df = pd.DataFrame(crawled_data)
        
        # 빈 행 제거 (성명, 소속, 사번이 모두 비어있는 행)
        df = df[
            (df['성명'].notna() & (df['성명'] != '')) | 
            (df['소속'].notna() & (df['소속'] != '')) | 
            (df['사번'].notna() & (df['사번'] != ''))
        ]
        
        # 번호 재정렬
        df['번호'] = range(1, len(df) + 1)
        
        # 컬럼 순서 지정
        column_order = [
            '번호', '상태', '세부내역', '신청일', '결재상태',
            '소속', '사번', '성명', '직위', '근태명',
            '시작일', '종료일', '총일수', '적용일수',
            '시작시간', '종료시간', '적용시간', '취소여부', '신청사유', '첨부파일'
        ]
        
        df = df[column_order]
        
        # 9. win32com을 사용하여 Excel 파일에 데이터 입력 (도형 보호)
        print(f"\n📂 Excel 파일 열기: {TARGET_FILE}")
        
        try:
            import win32com.client
            
            # Excel 애플리케이션 시작
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False  # 백그라운드 실행
            excel.DisplayAlerts = False  # 경고창 비활성화
            
            # 워크북 열기
            wb = excel.Workbooks.Open(TARGET_FILE)
            
            # "입력값" 시트 선택
            try:
                ws = wb.Worksheets("입력값")
                print("✅ '입력값' 시트 찾음")
            except:
                ws = wb.Worksheets.Add()
                ws.Name = "입력값"
                print("✅ '입력값' 시트 생성")
            
            # A2부터 T열까지 기존 데이터만 삭제 (도형은 보존)
            print("🗑️ 기존 데이터 삭제 중... (도형 개체 보호)")
            last_row = ws.UsedRange.Rows.Count
            if last_row > 1:
                # A2:T{last_row} 범위만 값 삭제
                delete_range = ws.Range(f"A2:T{last_row}")
                delete_range.ClearContents()  # 값만 삭제, 서식과 개체는 유지
            
            # A1에 헤더 입력
            print("📝 헤더 입력 중...")
            for col_idx, col_name in enumerate(column_order, 1):
                ws.Cells(1, col_idx).Value = col_name
            
            # A2부터 데이터 입력 (T열까지만)
            print("📊 데이터 입력 중... (값만 붙여넣기, 도형 보호)")
            for row_idx, row_data in enumerate(df.values, 2):
                for col_idx, value in enumerate(row_data, 1):
                    if col_idx <= 20:  # T열(20)까지만
                        ws.Cells(row_idx, col_idx).Value = value
            
            # 저장 및 닫기
            wb.Save()
            wb.Close()
            excel.Quit()
            
            print(f"\n✅ 데이터 입력 완료!")
            print(f"📊 총 {len(df)}개 행 입력")
            print(f"💾 파일: {TARGET_FILE}")
            print(f"📄 시트: 입력값")
            print(f"📍 위치: A2부터 T열까지")
            print(f"🛡️ U, V열 도형 개체 보호됨")
            
        except ImportError:
            print("\n⚠️ win32com 모듈이 설치되지 않았습니다.")
            print("💡 설치 방법: pip install pywin32")
            
        except Exception as e:
            print(f"\n⚠️ 파일 처리 중 오류: {e}")
            import traceback
            traceback.print_exc()
            
            # Excel 프로세스 정리
            try:
                excel.Quit()
            except:
                pass
        
        # 데이터 미리보기
        print(f"\n📋 데이터 미리보기:")
        print(df.to_string(index=False, max_rows=5))
        
    else:
        print("\n⚠️ 크롤링된 데이터가 없습니다.")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n✅ 작업 완료! 브라우저를 종료합니다.")
    driver.quit()