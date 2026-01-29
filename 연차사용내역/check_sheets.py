
import openpyxl

try:
    workbook = openpyxl.load_workbook(r'테스트파일\vac_Test.xlsx')
    print("Excel 파일의 시트 목록:")
    for sheet_name in workbook.sheetnames:
        print(f"- {sheet_name}")
except FileNotFoundError:
    print(r"오류: '테스트파일\vac_Test.xlsx' 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"오류 발생: {e}")
