import os
import shutil
import time
from dotenv import load_dotenv
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
SOURCE_FILE = os.getenv('SOURCE_FILE')
BACKUP_FOLDER = os.getenv('BACKUP_FOLDER')

# Hàm sao lưu cơ sở dữ liệu
def backup_database():
    try:
        if os.path.exists(SOURCE_FILE):
            file_name = os.path.basename(SOURCE_FILE)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_FOLDER, f"{timestamp}_{file_name}")

            shutil.copy(SOURCE_FILE, backup_file)
            print(f"Đã sao lưu database vào {backup_file}")
            return f"Sao lưu thành công: {backup_file}"
        else:
            return "Không tìm thấy file sql."
    except Exception as e:
        print(f"Lỗi khi sao lưu database: {e}")
    
# Hàm gửi email
def send_email(sender, receiver, subject, body, password):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        print(f"Email đã được gửi đến {receiver}")
        server.quit()
    except Exception as e:
        print(f"Không thể gửi email: {e}")

# Hàm thực thi
def job():
    result = backup_database()
    subject = "Kết quả sao lưu cơ sở dữ liệu"
    body = result
    send_email(SENDER_EMAIL, RECEIVER_EMAIL, subject, body, SENDER_PASSWORD)

schedule.every().day.at("00:00").do(job)
print("Đang chờ đến giờ để sao lưu databasse và gửi email...")

while True:
    schedule.run_pending()
    time.sleep(5)
