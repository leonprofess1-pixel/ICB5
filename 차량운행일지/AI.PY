import pandas as pd
import glob
import os
import sys

def merge_excel_files():
    # 1. 현재 파이썬 파일(AI.PY)이 위치한 폴더 경로를 구함
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"작업 대상 폴더: {script_dir}")

    # 2. 저장할 결과 파일명 설정 (경로 포함)
    output_filename = "합쳐진_결과물.xlsx"
    
    # 3. 해당 폴더 안에 있는 모든 .xlsx 파일 찾기 (경로 결합)
    search_pattern = os.path.join(script_dir, "*.xlsx")
    input_files = glob.glob(search_pattern)
    
    # 결과 파일이 목록에 포함되지 않도록 제외
    input_files = [f for f in input_files if os.path.basename(f) != output_filename]
        
    # 임시 파일(~$로 시작하는 파일) 제외
    input_files = [f for f in input_files if not os.path.basename(f).startswith('~$')]

    if not input_files:
        print("\n[오류] 지정된 폴더에 합칠 .xlsx 파일이 없습니다.")
        print(f"확인된 위치: {script_dir}")
        return

    print(f"\n총 {len(input_files)}개의 파일을 발견했습니다. 병합을 시작합니다...")

    all_data = []

    # 4. 각 파일을 순회하며 데이터 읽기
    for file in input_files:
        try:
            # 파일명만 깔끔하게 출력
            simple_name = os.path.basename(file)
            print(f"읽는 중: {simple_name}")
            
            df = pd.read_excel(file)
            all_data.append(df)
        except Exception as e:
            print(f"[오류] {os.path.basename(file)}을(를) 읽는 도중 문제가 발생했습니다: {e}")

    # 5. 데이터 하나로 합치기 및 저장
    if all_data:
        try:
            print("데이터를 하나로 합치는 중...")
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # 결과물 저장 경로
            save_path = os.path.join(script_dir, output_filename)
            
            print(f"파일 저장 중: {output_filename}")
            combined_df.to_excel(save_path, index=False)
            
            print("\n[완료] 모든 파일이 성공적으로 합쳐졌습니다!")
            print(f"저장된 위치: {save_path}")
            
        except Exception as e:
            print(f"[오류] 파일을 저장하는 도중 문제가 발생했습니다: {e}")
            print("혹시 결과 파일이 이미 열려있다면 닫고 다시 실행해주세요.")
    else:
        print("합칠 데이터가 없습니다.")

if __name__ == "__main__":
    merge_excel_files()