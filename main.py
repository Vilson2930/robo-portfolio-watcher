import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================================
# FUSO HORÁRIO BRASIL (BRT = UTC-3)
# ================================
BRT = timezone(timedelta(hours=-3))
agora = datetime.now(BRT)

# ================================
# DADOS DE E-MAIL (SECRETS)
# ================================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

if not EMAIL_USER or not EMAIL_APP_PASSWORD or not EMAIL_TO:
    raise ValueError("Secrets de e-mail não configurados corretamente.")

# ================================
# CONTEÚDO DO RELATÓRIO
# ================================
assunto = "Relatório Diário do Robô de Portfólio"

corpo = f"""
Relatório diário do robô de portfólio

Data/Hora (Brasil): {agora.strftime('%d/%m/%Y %H:%M:%S')}

Status:
- Execução concluída com sucesso
- Envio de e-mail funcionando

Este é um teste de garantia.
"""

# ================================
# MONTAGEM DO E-MAIL
# ================================
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg["Subject"] = assunto
msg.attach(MIMEText(corpo, "plain"))

# ================================
# ENVIO DO E-MAIL (GMAIL)
# ================================
with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL_USER, EMAIL_APP_PASSWORD)
    servidor.send_message(msg)

print("Relatório enviado com sucesso.")
