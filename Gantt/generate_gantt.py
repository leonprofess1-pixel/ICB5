import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name
from datetime import datetime, timedelta

# 1. 데이터 내장 (CSV 파일 없이도 실행 가능하도록 함)
data = [
    {"Activity":"활동 01","PlanStart":2,"PlanDuration":5,"ActualStart":2,"ActualDuration":4,"PercentComplete":0.39},
    {"Activity":"활동 02","PlanStart":1,"PlanDuration":6,"ActualStart":1,"ActualDuration":6,"PercentComplete":1.0},
    {"Activity":"활동 03","PlanStart":2,"PlanDuration":4,"ActualStart":2,"ActualDuration":5,"PercentComplete":0.35},
    {"Activity":"활동 04","PlanStart":4,"PlanDuration":8,"ActualStart":4,"ActualDuration":6,"PercentComplete":0.1},
    {"Activity":"활동 05","PlanStart":4,"PlanDuration":2,"ActualStart":4,"ActualDuration":8,"PercentComplete":0.85},
    {"Activity":"활동 06","PlanStart":4,"PlanDuration":3,"ActualStart":4,"ActualDuration":6,"PercentComplete":0.85},
    {"Activity":"활동 07","PlanStart":5,"PlanDuration":4,"ActualStart":5,"ActualDuration":3,"PercentComplete":0.5},
    {"Activity":"활동 08","PlanStart":5,"PlanDuration":2,"ActualStart":5,"ActualDuration":5,"PercentComplete":0.6},
    {"Activity":"활동 09","PlanStart":5,"PlanDuration":2,"ActualStart":5,"ActualDuration":6,"PercentComplete":0.75},
    {"Activity":"활동 10","PlanStart":6,"PlanDuration":5,"ActualStart":6,"ActualDuration":7,"PercentComplete":1.0},
    {"Activity":"활동 11","PlanStart":6,"PlanDuration":1,"ActualStart":5,"ActualDuration":8,"PercentComplete":0.6},
    {"Activity":"활동 12","PlanStart":9,"PlanDuration":3,"ActualStart":9,"ActualDuration":3,"PercentComplete":0.0},
    {"Activity":"활동 13","PlanStart":9,"PlanDuration":6,"ActualStart":9,"ActualDuration":7,"PercentComplete":0.5},
    {"Activity":"활동 14","PlanStart":9,"PlanDuration":3,"ActualStart":9,"ActualDuration":1,"PercentComplete":0.0},
    {"Activity":"활동 15","PlanStart":9,"PlanDuration":4,"ActualStart":8,"ActualDuration":5,"PercentComplete":0.01},
    {"Activity":"활동 16","PlanStart":10,"PlanDuration":5,"ActualStart":10,"ActualDuration":3,"PercentComplete":0.8},
    {"Activity":"활동 17","PlanStart":11,"PlanDuration":2,"ActualStart":11,"ActualDuration":5,"PercentComplete":0.0},
    {"Activity":"활동 18","PlanStart":12,"PlanDuration":6,"ActualStart":12,"ActualDuration":7,"PercentComplete":0.0},
    {"Activity":"활동 19","PlanStart":12,"PlanDuration":1,"ActualStart":12,"ActualDuration":5,"PercentComplete":0.0},
    {"Activity":"활동 20","PlanStart":14,"PlanDuration":5,"ActualStart":14,"ActualDuration":6,"PercentComplete":0.0},
    {"Activity":"활동 21","PlanStart":14,"PlanDuration":8,"ActualStart":14,"ActualDuration":2,"PercentComplete":0.44},
    {"Activity":"활동 22","PlanStart":14,"PlanDuration":7,"ActualStart":14,"ActualDuration":3,"PercentComplete":0.0},
    {"Activity":"활동 23","PlanStart":15,"PlanDuration":4,"ActualStart":15,"ActualDuration":8,"PercentComplete":0.12},
    {"Activity":"활동 24","PlanStart":15,"PlanDuration":5,"ActualStart":15,"ActualDuration":3,"PercentComplete":0.05},
    {"Activity":"활동 25","PlanStart":15,"PlanDuration":8,"ActualStart":15,"ActualDuration":5,"PercentComplete":0.0},
    {"Activity":"활동 26","PlanStart":16,"PlanDuration":28,"ActualStart":16,"ActualDuration":30,"PercentComplete":0.5}
]

df = pd.DataFrame(data)

# 기본 설정
base_date = datetime(2024, 1, 1)

# 날짜 데이터 변환 (계산용)
df['Plan_Start_Date'] = df['PlanStart'].apply(lambda x: base_date + timedelta(days=int(x)-1))
df['Actual_Start_Date'] = df['ActualStart'].apply(lambda x: base_date + timedelta(days=int(x)-1))

# 엑셀 파일 생성
output_filename = 'Date_Based_Gantt_Chart_Dynamic.xlsx'
writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
workbook = writer.book
worksheet = workbook.add_worksheet('Gantt Chart')

# 포맷
header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#D7E4BC', 'border': 1})
date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align': 'center', 'border': 1})
num_format = workbook.add_format({'align': 'center', 'border': 1})
text_format = workbook.add_format({'border': 1})
plan_fill = workbook.add_format({'bg_color': '#92CDDC', 'pattern': 1}) # Blue
actual_fill = workbook.add_format({'bg_color': '#E26B0A', 'pattern': 1, 'font_color': 'white'}) # Orange

# 상단 설정 (프로젝트 시작일 관리)
worksheet.write('B1', '프로젝트 시작일 (Start Date):', header_format)
worksheet.write_datetime('C1', base_date, date_format)
workbook.define_name('ProjectStart', '=Gantt Chart!$C$1')

# 헤더 작성
headers = ['활동 (Activity)', '계획 시작일', '계획 기간(일)', '계획 종료일', '실제 시작일', '실제 기간(일)', '실제 종료일', '진척률']
start_row = 2
for col_num, header in enumerate(headers):
    worksheet.write(start_row, col_num, header, header_format)

# 데이터 채우기
data_row_start = start_row + 1
current_row = data_row_start

for index, data in df.iterrows():
    worksheet.write(current_row, 0, data['Activity'], text_format)
    worksheet.write_datetime(current_row, 1, data['Plan_Start_Date'], date_format)
    worksheet.write_number(current_row, 2, data['PlanDuration'], num_format)
    worksheet.write_formula(current_row, 3, f'=B{current_row+1}+C{current_row+1}-1', date_format)
    worksheet.write_datetime(current_row, 4, data['Actual_Start_Date'], date_format)
    worksheet.write_number(current_row, 5, data['ActualDuration'], num_format)
    worksheet.write_formula(current_row, 6, f'=E{current_row+1}+F{current_row+1}-1', date_format)
    worksheet.write_number(current_row, 7, data['PercentComplete'], num_format)
    current_row += 1

# 타임라인 생성
timeline_start_col = len(headers)
max_days = 60

# 타임라인 첫 날짜
first_col_letter = xl_col_to_name(timeline_start_col)
worksheet.write_formula(start_row, timeline_start_col, '=ProjectStart', date_format)

# 타임라인 나머지 날짜
for i in range(1, max_days):
    col_idx = timeline_start_col + i
    prev_col_letter = xl_col_to_name(col_idx - 1)
    worksheet.write_formula(start_row, col_idx, f'={prev_col_letter}{start_row+1}+1', date_format)
    worksheet.set_column(col_idx, col_idx, 3)

# 조건부 서식 적용
last_data_row = current_row
last_col_letter = xl_col_to_name(timeline_start_col + max_days - 1)
timeline_range = f'{first_col_letter}{data_row_start+1}:{last_col_letter}{last_data_row}'

# 계획(Plan) 서식
worksheet.conditional_format(timeline_range, {
    'type': 'formula',
    'criteria': f'=AND({first_col_letter}${start_row+1}>=$B{data_row_start+1}, {first_col_letter}${start_row+1}<=$D{data_row_start+1})',
    'format': plan_fill
})

# 실제(Actual) 서식
worksheet.conditional_format(timeline_range, {
    'type': 'formula',
    'criteria': f'=AND({first_col_letter}${start_row+1}>=$E{data_row_start+1}, {first_col_letter}${start_row+1}<=$G{data_row_start+1})',
    'format': actual_fill
})

# 열 너비 조정
worksheet.set_column('A:A', 20)
worksheet.set_column('B:H', 12)

writer.close()
print(f"파일이 성공적으로 생성되었습니다: {output_filename}")