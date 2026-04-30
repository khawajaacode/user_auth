import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

async def send_otp_email(to_email: str, otp: str):
    message = MIMEMultipart()
    message["From"] = settings.GMAIL_USER
    message["To"] = to_email
    message["Subject"] = "Your OTP Code"

    body = f"""
    Your OTP code is: {otp}
    
    This code expires in 5 minutes.
    Do not share this code with anyone.
    """

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(settings.GMAIL_USER, settings.GMAIL_PASSWORD)
        server.sendmail(settings.GMAIL_USER, to_email, message.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")