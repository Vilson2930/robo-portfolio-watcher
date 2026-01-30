import os
import time
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =====================================================
# CONFIGURAÇÃO DE FUSO HORÁRIO (BRASIL - BRT = UTC-3)
# =====================================================
BRT = timezone(timedelta(hours=-3))

# =====================================================
# HORA ALVO DE ENVIO (14:30 BRT)
# =====================================================
HORA_ENVIO = 14
MINUTO_ENVIO = 30

# =====================================================
# DADOS DE E-MAIL (VINDOS DOS SECRETS DO GITHUB)
# =====================================================
EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_RECEIVER = os.getenv("EMAIL_TO")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Validação básica
if not EMAIL_SENDER or not EMAIL_RECEIVER or not APP_PASSWORD:
    raise ValueError("Secrets de e-mail não configurados corretamente.")

# =====================================================
# CALCULA QUANTO TEMPO ESPERAR ATÉ 14:30 BRT
# =====================================================
agora = datetime.now(BRT)
horario_envio = agora.replace(
    hour=HORA_ENVIO,
    minute=MINUTO_ENVIO,
    second=0,
    microsecond=0
)

# Se já passou das 14:30 hoje, envia no próximo dia
if agora >= horario_envio:
    horario_envio += timedelta(days=1)

segundos_espera = (horario_envio - agora).total_seconds()

print(f"Aguardando até {horario_envio.strftime('%d/%m/%Y %H:%M:%S')} BRT")
print(f"Tempo de espera: {int(segundos_espera)} segundos")

time.sleep(segundos_espera)

# =====================================================
# MONTA O E-MAIL
# =====================================================
mensagem = MIMEMultipart()
mensagem["From"] = EMAIL_SENDER
mensagem["To"] = EMAIL_RECEIVER
mensagem["Subject"] = "Relatório automático - Observador de Portfólio"

corpo = f"""
Relatório enviado automaticamente.

Horário de envio (BRT):
{datetime.now(BRT).strftime('%d/%m/%Y %H:%M:%S')}

Status:
Sistema funcionando corretamente.
"""

mensagem.attach(MIMEText(corpo, "plain"))

# =====================================================
# ENVIO DO E-MAIL (SMTP GMAIL)
# =====================================================
with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL_SENDER, APP_PASSWORD)
    servidor.send_message(mensagem)

print("E-mail enviado com sucesso.")
