import os
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =====================================================
# FUSO HORÁRIO DO BRASIL (BRT = UTC-3)
# =====================================================
BRT = timezone(timedelta(hours=-3))
agora = datetime.now(BRT)

# =====================================================
# HORÁRIO PROGRAMADO PARA ENVIO (21:00 BRT)
# =====================================================
horario_envio = agora.replace(hour=21, minute=0, second=0)

# Se passou da meia-noite e já é depois das 21h
if agora.hour >= 21:
    horario_envio = horario_envio
else:
    # Se ainda não chegou 21h, não envia
    print("Ainda não é 21h no horário do Brasil. Encerrando execução.")
    exit(0)

# =====================================================
# DADOS DE E-MAIL (SECRETS DO GITHUB)
# =====================================================
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

if not EMAIL_USER or not EMAIL_APP_PASSWORD or not EMAIL_TO:
    raise ValueError("Secrets de e-mail não configurados corretamente.")

# =====================================================
# CONTEÚDO DO RELATÓRIO
# =====================================================
assunto = "Relatório Diário do Robô de Portfólio"
corpo = f"""
Olá,

Este é o relatório diário automático do Robô de Portfólio.

Data e hora do envio (Brasil):
{agora.strftime('%d/%m/%Y %H:%M:%S')}

Status do sistema:
- Execução automática: OK
- Horário programado: 21h (BRT)
- Envio de e-mail: OK

Atenciosamente,
Robô de Portfólio
"""

msg = MIMEMultipart()
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO
msg["Subject"] = assunto
msg.attach(MIMEText(corpo, "plain"))

# =====================================================
# ENVIO DO E-MAIL
# =====================================================
with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL_USER, EMAIL_APP_PASSWORD)
    servidor.send_message(msg)

print("Relatório enviado com sucesso às 21h (BRT).")
