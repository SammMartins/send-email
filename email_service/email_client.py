import smtplib
import os
import re
import toml
import streamlit as st
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
        with open("log_erros.txt", "a") as file:
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
                    
                    # Substituir negrito e itálico no corpo do e-mail
                    corpo_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', corpo)
                    corpo_html = re.sub(r'__(.*?)__', r'<i>\1</i>', corpo_html)
                    
                    # Substituir listas não ordenadas
                    corpo_html = re.sub(r'^\* (.*)', r'<ul><li>\1</li></ul>', corpo_html, flags=re.MULTILINE)
                    corpo_html = re.sub(r'</ul>\n<ul>', '', corpo_html)  # Remover listas aninhadas incorretamente
                    
                    # Substituir listas ordenadas
                    corpo_html = re.sub(r'^\d+\. (.*)', r'<ol><li>\1</li></ol>', corpo_html, flags=re.MULTILINE)
                    corpo_html = re.sub(r'</ol>\n<ol>', '', corpo_html)  # Remover listas aninhadas incorretamente
                    
                    corpo_html = corpo_html.replace('\n', '<br>')
                    
                    msg.attach(MIMEText(f"{saudacao.format(Nome=contato['Nome'])}<br><br>{corpo_html}<br><br>{assinatura_email}", 'html'))
        
                    server.sendmail(email, contato["Email"], msg.as_string())
        

    except Exception as e:
        print(f"Erro ao enviar email: {e}")

        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Salvar o erro sem sobrescrever o arquivo e logs anteriores
        with open("log_erros.txt", "a") as file:
            file.write(f"{horario} - Erro ao enviar e-mail: {e}\n")

        return False
    finally:
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("log_auditoria.txt", "a") as file:
            file.write(f"{horario} - E-mail enviado por {st.session_state['email_usuario']}\n")

        print(f"E-mail enviado por {st.session_state['email_usuario']}")

        server.quit()

    return True