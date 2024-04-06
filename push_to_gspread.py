import sys
import gspread
from serial import Serial
from datetime import datetime
from gspread.exceptions import WorksheetNotFound
from gspread.exceptions import SpreadsheetNotFound


def get_current_time():
    date_time = datetime.now()
    month = date_time.month
    day = date_time.day
    year = date_time.year
    time = date_time.strftime("%H:%M:%S")
    return time, day, month, year


def get_information(finger_id):
    try:
        data_base = sheet.worksheet("DATA")
        student_id = data_base.cell(finger_id+1, 2).value
        student_name = data_base.cell(finger_id+1, 3).value
        return student_id, student_name
    except SpreadsheetNotFound:
        print("Vui lòng điền thông tin lớp học vào bảng tính 'DATA' trước!")
        sys.exit()


def delete_member(finger_id):
    try:
        data_base = sheet.worksheet("DATA")
        data_base.update_cell(finger_id + 1, 2, '')
        data_base.update_cell(finger_id + 1, 3, '')
    except WorksheetNotFound:
        print("Bảng tính DATA không tồn tại")


def add_member(finger_id):
    student_id = input("Nhập mã sinh viên: ")
    student_name = input("Nhập họ và tên: ")

    try:
        data_base = sheet.worksheet("DATA")
        data_base.update_cell(finger_id + 1, 2, student_id)
        data_base.update_cell(finger_id + 1, 3, student_name)
    except WorksheetNotFound:
        print("Bảng tính DATA không tồn tại")


def push_2_gspread(finger_id):
    time, day, month, year = get_current_time()
    current_time = str(time)
    current_date = str(day) + "/" + str(month) + "/" + str(year)

    student_id, student_name = get_information(finger_id)

    try:
        work_sheet = sheet.worksheet("Điểm danh ngày " + str(current_date))
    except WorksheetNotFound:
        work_sheet = sheet.add_worksheet("Điểm danh ngày " + str(current_date), rows=130, cols=3)

    work_sheet.update_cell(finger_id, 1, student_id)
    work_sheet.update_cell(finger_id, 2, student_name)
    work_sheet.update_cell(finger_id, 3, current_time)


# !importan
arduino = Serial(port='COM8', baudrate=9600)  # Replace by COM available
google_sheet = gspread.service_account(filename='service_account.json')
your_mail = "thanh139ptit@gmail.com"

sheet_name = "Class " + str(input("Nhập lớp: "))
try:
    sheet = google_sheet.open(sheet_name)
except SpreadsheetNotFound:
    sheet = google_sheet.create(sheet_name)
    sheet.add_worksheet("DATA", 130, 3)
    sheet.share(your_mail, perm_type='user', role='writer')
    print("Vui lòng điền thông tin lớp học vào bảng tính 'DATA' trước!")
    member = int(input("Nhập số lượng sinh viên (<120): "))
    for student in range(member):
        student_id = input(f"Nhập mã sinh viên {student + 1}: ")
        student_name = input(f"Họ và tên sinh viên {student + 1}: ")

        try:
            data_base = sheet.worksheet("DATA")
            data_base.update_cell(student + 2, 1, student+1)
            data_base.update_cell(student + 2, 2, student_id)
            data_base.update_cell(student + 2, 3, student_name)
        except WorksheetNotFound:
            print("Bảng tính DATA không tồn tại")


while True:
    incoming_data = arduino.readline().decode()
    try:
        data = incoming_data.split('|')
        if data[0] == "ADD":
            add_member(int(data[1]))
        elif data[0] == "DEL":
            delete_member(int(data[1]))
            # pass
        elif int(data[0]) > 0:
            push_2_gspread(int(data[0]))
    except:
        push_2_gspread(int(incoming_data))

