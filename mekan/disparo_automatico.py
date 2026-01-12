import pandas as pd
from sqlalchemy import create_engine
import smtplib
from email.message import EmailMessage
import schedule  # <--- PRECISA INSTALAR: pip install schedule
import time

# 1. Configuração do Banco
url_conexao = "mysql+pymysql://root:JGwsTBYFWtLCVfBsOKJmZLzmTNexZjhF@yamanote.proxy.rlwy.net:12296/railway"
engine = create_engine(url_conexao)

def enviar_relatorio_agendado():
    try:
        # 2. Gera o relatório
        df = pd.read_sql("SELECT * FROM usuarios", engine)
        df.to_excel("relatorio_automatico.xlsx", index=False)

        # 3. Configura o e-mail
        msg = EmailMessage()
        msg['Subject'] = '📊 Relatório Diário Automático - Jotta Store'
        msg['From'] = 'mekanics153@gmail.com'
        msg['To'] = 'mekanics153@gmail.com'
        msg.set_content(f"Relatório gerado automaticamente pelo sistema.\nTotal de registros: {len(df)}")

        with open("relatorio_automatico.xlsx", 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='xlsx', filename="relatorio_automatico.xlsx")

        # 4. Envia
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('mekanics153@gmail.com', 'rfvpmoeolsqelzjo')
            smtp.send_message(msg)
        
        print(f"✅ Relatório enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no envio automático: {e}")

# --- O QUE MUDA PARA FICAR CORRETO ---

# Agendar para as 08:30 (Atenção: Railway usa horário UTC!)
# Se você quer 08:30 no Brasil, e o Railway estiver em UTC, 
# você deve ajustar para o horário correspondente (ex: 11:30 UTC)
schedule.every().day.at("08:30").do(enviar_relatorio_agendado)

print("🚀 Script rodando... Aguardando horário para disparo.")

if __name__ == "__main__":
    # Loop infinito para manter o script vivo e verificando o relógio
    while True:
        schedule.run_pending()
        time.sleep(60) # Verifica o relógio a cada 1 minuto