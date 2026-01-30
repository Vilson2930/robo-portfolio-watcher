import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# FUSO HORÁRIO BRASIL (BRT = UTC-3)
# =========================================================
BRT = timezone(timedelta(hours=-3))
agora = datetime.now(BRT)

# =========================================================
# DADOS DE E-MAIL (VINDOS DOS SECRETS DO GITHUB)
# =========================================================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

if not EMAIL_USER or not EMAIL_APP_PASSWORD or not EMAIL_TO:
    raise ValueError("Secrets de e-mail não configurados corretamente.")

# =========================================================
# CONTEÚDO DO E-MAIL
# =========================================================
assunto = "Relatório Diário do Robô de Portfólio"

corpo = f"""
Relatório Diário – Robô de Portfólio

Data/Hora (Brasil): {agora.strftime('%d/%m/%Y %H:%M')}

Status:
✔ Robô executado com sucesso
✔ Envio automático funcionando
✔ GitHub Actions operacional

Este e-mail foi enviado automaticamente.
"""

# =========================================================
# MONTAGEM DO E-MAIL
# =========================================================
msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg["Subject"] = assunto
msg.attach(MIMEText(corpo, "plain"))

# =========================================================
# ENVIO VIA SMTP GMAIL
# =========================================================
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
        server.send_message(msg)

    print("✅ E-mail enviado com sucesso.")

except Exception as e:
    print("❌ Erro ao enviar e-mail:")
    print(e)
    raise
