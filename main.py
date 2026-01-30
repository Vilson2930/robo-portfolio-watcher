import time
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===============================
# EMAIL SETTINGS
# ===============================
EMAIL_SENDER = "vilsonjosepereirapinto@gmail.com"
EMAIL_RECEIVER = "vilsonjosepereirapinto@gmail.com"

# Gmail APP PASSWORD (16 characters)
APP_PASSWORD = "adrsqtbyeeqigdxm"

# ===============================
# BRAZIL TIMEZONE (BRT = UTC-3)
# ===============================
BRT = timezone(timedelta(hours=-3))

now_brt = datetime.now(BRT)

target_time = now_brt.replace(
    hour=13,
    minute=35,
    second=0,
    microsecond=0
)

# If current time already passed 13:35, send immediately
if target_time > now_brt:
    wait_seconds = (target_time - now_brt).total_seconds()
    print(f"Waiting until 13:25 BRT ({int(wait_seconds)} seconds)...")
    time.sleep(wait_seconds)
else:
    print("Target time already passed. Sending immediately.")

# ===============================
# EMAIL CONTENT
# ===============================
send_time = datetime.now(BRT).strftime("%d/%m/%Y %H:%M:%S")

body = f"""
TEST REPORT – PORTFOLIO WATCHER

Scheduled time: 13:25 BRT
Actual send time: {send_time}

If you received this email, automatic delivery is WORKING.
"""

msg = MIMEMultipart()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "TEST – Scheduled Email 13:35 BRT"

msg.attach(MIMEText(body, "plain"))

# ===============================
# SEND EMAIL
# ===============================
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully.")

except Exception as error:
    print("ERROR sending email:")
    print(error)
