import os
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================================================
# FUSO HORÁRIO BRASIL (BRT = UTC-3)
# ==================================================
BRT = timezone(timedelta(hours=-3))
agora = datetime.now(BRT)

# ==================================================
# DADOS DO E-MAIL (VINDOS DOS SECRETS DO GITHUB)
# ==================================================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

if not EMAIL_USER or not EMAIL_TO or not EMAIL_APP_PASSWORD:
    raise RuntimeError("Segredos de e-mail não configurados corretamente")

# ==================================================
# CONTEÚDO DO RELATÓRIO
# ==================================================
assunto = f"Relatório Diário - {agora.strftime('%d/%m/%Y')}"
corpo = f"""
Relatório diário gerado automaticamente.

Data e hora (Brasil):
{agora.strftime('%d/%m/%Y %H:%M')}

Status:
✅ Robô executado com sucesso

Este e-mail foi enviado automaticamente pelo GitHub Actions.
"""

# ==================================================
# MONTAGEM DO E-MAIL
# ==================================================
mensagem = MIMEMultipart()
mensagem["From"] = EMAIL_USER
mensagem["To"] = EMAIL_TO
mensagem["Subject"] = assunto
mensagem.attach(MIMEText(corpo, "plain"))

# ==================================================
# ENVIO VIA GMAIL (SMTP)
# ==================================================
with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL_USER, EMAIL_APP_PASSWORD)
    servidor.send_message(mensagem)

print("✅ E-mail enviado com sucesso")
