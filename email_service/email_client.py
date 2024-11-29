import smtplib
import os
import toml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime

def enviar_email(assunto, saudacao, corpo, lista_contatos, assinatura):
    load_dotenv()
    email = os.getenv("email")
    senha = os.getenv("password")

    if not email or not senha:
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Salvar o erro sem sobrescrever o arquivo e logs anteriores
        with open("log_errors.txt", "a") as file:
            file.write(f"{horario} - Erro ao enviar e-mail: Credenciais não encontradas\n")

        return False
        

    try:
        # Configuração do servidor
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, senha)

        with open("lista_contatos.toml", "r") as file:
            data = toml.load(file)
        
        with open(f"assinaturas/{assinatura}.html", "r") as file:
            assinatura_email = file.read()

        for lista in lista_contatos:
            if "Contatos" in data[lista]:
                for contato in data[lista]["Contatos"]:
                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = contato["Email"]
                    msg['Subject'] = assunto
                    
                    msg.attach(MIMEText(f"{saudacao.format(Nome=contato['Nome'])}<br><br>{corpo}<br><br>{assinatura_email}", 'html'))

                    server.sendmail(email, contato["Email"], msg.as_string())

    except Exception as e:
        print(f"Erro ao enviar email: {e}")

        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Salvar o erro sem sobrescrever o arquivo e logs anteriores
        with open("log_errors.txt", "a") as file:
            file.write(f"{horario} - Erro ao enviar e-mail: {e}\n")

        return False
    finally:
        server.quit()

    return True