import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from ssl import create_default_context


load_dotenv()

password = os.getenv("EMAIL_PASSWORD")

def send_recovery_email(to_email: str, recovery_link: str):
    sender_email = "ddd755505@gmail.com"
    subject = "Recuperación de Contraseña"
    body = f"Hola,\n\nPara restablecer tu contraseña, sigue el siguiente enlace:\n{recovery_link}\n\nSi no solicitaste este cambio, ignora este mensaje."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    
    context = create_default_context()

    # Conectar al servidor SMTP y enviar el correo
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as server:
        print(f"Conectando al servidor SMTP {sender_email, password}")
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
