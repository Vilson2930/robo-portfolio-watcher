import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ===============================
# CONFIGURAÇÕES DE EMAIL
# ===============================
EMAIL_REMETENTE = "vilsonjosepereirapinto@gmail.com"
EMAIL_DESTINO = "vilsonpinto@escola.pr.gov.br"

# ⚠️ USE APENAS SENHA DE APP DO GMAIL (16 caracteres, sem espaços)
SENHA_APP = "COLE_AQUI_SUA_SENHA_DE_APP"

# ===============================
# AGUARDA 5 MINUTOS
# ===============================
print("⏳ Teste iniciado. Aguardando 5 minutos para envio do e-mail...")
time.sleep(300)  # 300 segundos = 5 minutos

# ===============================
# CONTEÚDO DO RELATÓRIO (TESTE)
# ===============================
agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

mensagem = f"""
RELATÓRIO DE TESTE – PORTFOLIO WATCHER

Horário de envio: {agora}

Este é um EMAIL DE TESTE.
Se você recebeu esta mensagem, o envio automático está FUNCIONANDO corretamente.

Próximo passo:
✔️ Substituir este texto pelo relatório real
✔️ Agendar envio diário automático
"""

# ===============================
# MONTAGEM DO EMAIL
# ===============================
msg = MIMEMultipart()
msg["From"] = EMAIL_REMETENTE
msg["To"] = EMAIL_DESTINO
msg["Subject"] = "📊 TESTE – Relatório automático (5 minutos)"

msg.attach(MIMEText(mensagem, "plain"))

# ===============================
# ENVIO DO EMAIL
# ===============================
try:
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(EMAIL_REMETENTE, SENHA_APP)
    servidor.send_message(msg)
    servidor.quit()

    print("✅ Email enviado com sucesso!")

except Exception as erro:
    print("❌ ERRO AO ENVIAR EMAIL")
    print(erro)
