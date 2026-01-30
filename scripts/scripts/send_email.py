import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz

# ===============================
# VARIÁVEIS DE AMBIENTE
# ===============================
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]
EMAIL_TO = os.environ["EMAIL_TO"]

# ===============================
# FUNÇÃO: VERIFICA 06H BRASIL
# ===============================
def agora_e_6h_brasil():
    tz_brasil = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(tz_brasil)
    return agora.hour == 6

# ===============================
# FUNÇÃO: ENVIO DE E-MAIL
# ===============================
def enviar_email(conteudo):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = "📊 Relatório Diário — Robô de Portfólio"

    msg.attach(MIMEText(conteudo, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
    server.send_message(msg)
    server.quit()

# ===============================
# EXECUÇÃO PRINCIPAL
# ===============================
if __name__ == "__main__":

    if not agora_e_6h_brasil():
        print("⏰ Ainda não é 06:00 no Brasil — e-mail NÃO enviado.")
        sys.exit(0)

    tz_brasil = pytz.timezone("America/Sao_Paulo")
    data_brasil = datetime.now(tz_brasil).strftime("%d/%m/%Y")

    relatorio = f"""
📊 RELATÓRIO DIÁRIO — ROBÔ DE PORTFÓLIO

✅ Execução automática
✅ Status: OK
✅ Origem: GitHub Actions
📅 Data: {data_brasil}

Este relatório é enviado apenas uma vez por dia às 06:00
(horário oficial do Brasil).
"""

    enviar_email(relatorio)
    print("📨 E-mail enviado com sucesso às 06:00 (Brasil).")
