import random
from flask_mail import Message


otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(email, otp, otp_expiration):
    otp_storage[email] = (otp, otp_expiration)

def retrieve_otp(email):
    return otp_storage.get(email, (None, None))

def clear_otp(email):
    if email in otp_storage:
        del otp_storage[email]

def send_otp_email(email, otp):
    from app import mail
    message = Message(subject='OTP Verification', recipients=[email])
    message.body = f'Your OTP is: {otp}.'

    with mail.connect() as conn:
        conn.send(message)
