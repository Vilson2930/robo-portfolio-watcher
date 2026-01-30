import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================================================
# FUSO HORÁRIO DO BRASIL (BRT = UTC-3)
# ==================================================
BRT = timezone(timedelta(hours=-3))
agora = datetime.now(BRT)

# ==================================================
# EXECUTA SOMENTE APÓS 21:00 BRT
# ==================================================
if agora.hour < 21:
    print("Ainda não são 21h no horário do Brasil. Encerrando execução.")
    exit(0)

# ==================================================
# SECRETS DO GITHUB
# ==================================================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

if not EMAIL_USER or not EMAIL_APP_PASSWORD or not EMAIL_TO:
    raise ValueError("Secrets de e-mail não configurados corretamente.")

# ==================================================
# CONTEÚDO DO RELATÓRIO
# ==================================================
assunto = "Relatório Diário do Robô de Portfólio"
corpo = f"""
Relatório gerado com sucesso.

Data/Hora (Brasil): {agora.strftime('%d/%m/%Y %H:%M')}
"""

# ==================================================
# ENVIO DE E-MAIL
# ==================================================
mensagem = MIMEMultipart()
mensagem["From"] = EMAIL_USER
mensagem["To"] = EMAIL_TO
mensagem["Subject"] = assunto
mensagem.attach(MIMEText(corpo, "plain"))

with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL_USER, EMAIL_APP_PASSWORD)
    servidor.send_message(mensagem)

print("Relatório enviado com sucesso.")
