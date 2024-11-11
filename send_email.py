import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import configparser
import logging
import os

# Pegar a hora atual
hora_atual = datetime.now().strftime('%H:%M:%S')

def send_email(to_email, subject, body):
    # Configurar caminho para arquivo de credenciais
    path_config = '/home/samm/'

    # Definir o caminho para o arquivo de log
    path_logging = '/home/samm/PyProjects/send_email/'
    log_file = os.path.join(path_logging, 'send_email_errors.log')

    # Configurar o logging para registrar erros
    logging.basicConfig(filename=log_file, level=logging.ERROR)

    # Carregar credenciais do arquivo config.ini
    config = configparser.ConfigParser()
    config.read(path_config + 'config.ini')

    try:
        # Pegar as credenciais do arquivo
        from_email = config['credentials']['email']
        password = config['credentials']['password']
        
        # Criar o objeto de mensagem
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Assinatura personalizada (HTML)
        signature = """
        <table style="border:none; border-collapse:collapse;">
            <colgroup>
                <col width="30">
                <col width="160">
                <col width="295">
            </colgroup>
            <tbody>
                <tr style="height:48.7671pt;">
                    <td colspan="2" style="vertical-align:top; padding:2.15433pt; overflow:hidden;">
                        <br>
                        <p dir="ltr" style="line-height:1.2; margin-top:0pt; margin-bottom:0pt;">
                            <span style="font-size:11pt; background-color:transparent; vertical-align:baseline;">
                                <font color="#689dd9" face="Nunito, sans-serif">
                                    <b>Sammuel</b>
                                </font>
                            </span>
                            <span style="font-size:11pt; font-family:Arial,sans-serif; color:rgb(0,0,0); background-color:transparent; vertical-align:baseline;">
                            </span>
                            <span style="font-size:11pt; font-family:Nunito,sans-serif; color:rgb(104,157,217); background-color:transparent; font-weight:900; vertical-align:baseline;">
                                Martins
                            </span>
                            <span style="font-size:15pt; font-family:Nunito,sans-serif; color:rgb(104,157,217); background-color:transparent; font-weight:800; vertical-align:baseline;">
                                <br>
                            </span>
                            <span style="font-size:8pt; font-family:Nunito,sans-serif; color:rgb(72,76,128); background-color:transparent; font-weight:900; vertical-align:baseline;">
                                Analista de Suporte
                            </span>
                        </p>
                        <br>
                    </td>
                    <td rowspan="3" style="vertical-align:top; padding:5pt; overflow:hidden;">
                        <p dir="ltr" style="line-height:1.2; margin-top:0pt; margin-bottom:0pt;">
                            <span style="font-size:11pt; font-family:Arial,sans-serif; color:rgb(0,0,0); background-color:transparent; vertical-align:baseline;">
                                <span style="border:none; display:inline-block; overflow:hidden; width:251px; height:159px;">
                                    <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXerqh8lEN4IcyJKo6_zCDxPX7RuP6GfRUB5bdcKAkd6iSEspnY7lgbzhqC-9PQ9yDFq8cxKgga4bapkYL1ha0-NHhUe83BvSoYGOQHeVwwTUjC8SWa3srwHWnfPHS0y1H9uUOZOrdk4_dFNbOjU-ndu1pqD?key=gjGecb5domMhmHOu7eLJRw" width="251" height="160.6509584664537" style="margin-left:0px;" class="CToWUd a6T" data-bit="iit" tabindex="0">
                                </span>
                            </span>
                        </p>
                    </td>
                </tr>
                <tr style="height:21.179pt;">
                    <td colspan="2" style="vertical-align:top; overflow:hidden;">
                        <p dir="ltr" style="line-height:1.2; margin-top:0pt; margin-bottom:0pt;">
                            <a href="http://wa.me/5577934219279" target="_blank">
                                <span style="font-size:11pt; font-family:Oswald,sans-serif; color:rgb(17,85,204); background-color:transparent; vertical-align:baseline;">
                                    <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXd_Ue9epPvTcyMsoqtezKWPL6OiMRMa57p6ZcgKrXyCWMXhOr_rMgOxNbUe5txEH52eKKMorHCbK0cFXPHc1aU64ucWqLN3AdJ2QuGQ4-FFA5uE52YOhc7L6C_lZvzfEAbE7qT_MF4VUlYkkoFXWepL64I?key=gjGecb5domMhmHOu7eLJRw" width="20" height="20" style="margin-left:0px;">
                                </span>
                            </a>
                            <a href="https://www.instagram.com/tivic.tecnologia/" target="_blank">
                                <span style="font-size:11pt; font-family:Oswald,sans-serif; color:rgb(17,85,204); background-color:transparent; vertical-align:baseline;">
                                    <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXdF78NcfMq1ouOVwywyfjwoWVuKcianYwBPu3p_3WOx3yCYo7tgBhHCxTcwZYVrgfuXWl8d2zivhxlGaXR9DelCzjSPPUofX1oXesxY8t6wEbUPJ0wRRipm_gc6hVWRZaz_wpJiDkORFxI9L8hATD9ge8U?key=gjGecb5domMhmHOu7eLJRw" width="20" height="20" style="margin-left:0px;">
                                </span>
                            </a>
                            <a href="https://www.linkedin.com/company/tivic-tecnologia-e-informacao/" target="_blank">
                                <span style="font-size:11pt; font-family:Oswald,sans-serif; color:rgb(17,85,204); background-color:transparent; vertical-align:baseline;">
                                    <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXe7mnsPWkU3t--TL9y-wbcgB2jtoeCB-RxQehwt_eg9zJqteTPU0VtOZPv0fu8Ho1rp8eheGETyUi-wcy544qOAO80HAgUkm29G3DF8nB_T2h_iwuY7gqnDkW3GH9W1vEwgrF2T28JKMuBbWmrh0bONGjA?key=gjGecb5domMhmHOu7eLJRw" width="20" height="20" style="margin-left:0px;">
                                </span>
                            </a>
                        </p>
                    </td>
                </tr>
                <tr style="height:19.5pt;">
                    <td style="vertical-align:middle; padding:2.15433pt; overflow:hidden;">
                        <p dir="ltr" style="line-height:1.2; margin-top:0pt; margin-bottom:0pt;">
                            <img src="https://lh7-rt.googleusercontent.com/docsz/AD_4nXfdL76lMfeUjmvVn_VSa6Hn6j0RMfrugq1y4Vk5lSH46WKDwsAGC2amIhBGE58i_YQi7W8XO5Qrqd5oOaMvTLAR7tXzywicr-lTdOtURwoA9arTVX6b7Bs2gHXw6XamMf9TtEq07zC-FpPTTEgnIfk9Sw?key=gjGecb5domMhmHOu7eLJRw" width="19" height="19" style="margin-left:0px;">
                        </p>
                    </td>
                    <td style="vertical-align:middle; padding:4.98898pt; overflow:hidden;">
                        <p dir="ltr" style="line-height:1.2; margin-top:0pt; margin-bottom:0pt;">
                            <span style="font-size:9pt; font-family:Oswald,sans-serif; color:rgb(104,157,217); background-color:transparent; vertical-align:baseline;">
                                Av. Espanha, 74 - Candeias.
                            </span>
                        </p>
                        <p dir="ltr" style="line-height:1.2; margin-top:0pt; margin-bottom:0pt;">
                            <span style="font-size:9pt; font-family:Oswald,sans-serif; color:rgb(104,157,217); background-color:transparent; vertical-align:baseline;">
                                Vitória da Conquista - BA
                            </span>
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
        """
        # Adicionar o corpo do e-mail + assinatura
        body_with_signature = body + signature
        msg.attach(MIMEText(body_with_signature, 'html'))  # Usar 'html' para HTML, ou 'plain' para texto simples
        
        # Tentar conectar ao servidor do Gmail
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
        except smtplib.SMTPAuthenticationError:
            logging.error(f"{hora_atual} Erro de autenticação: Verifique suas credenciais.")
            print(f"{hora_atual} Erro de autenticação: Verifique suas credenciais.")
            return
        except smtplib.SMTPConnectError:
            logging.error(f"{hora_atual} Erro de conexão: Não foi possível conectar ao servidor SMTP.")
            print(f"{hora_atual} Erro de conexão: Não foi possível conectar ao servidor SMTP.")
            return
        except Exception as e:
            logging.error(f"{hora_atual} Erro ao tentar conectar ao servidor SMTP: {e}")
            print(f"{hora_atual} Erro ao tentar conectar ao servidor SMTP: {e}")
            return

        # Tentar enviar o e-mail
        try:
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            print(f"{hora_atual} E-mail enviado com sucesso para {to_email}")
        except smtplib.SMTPRecipientsRefused:
            logging.error(f"{hora_atual} Erro: O destinatário {to_email} foi recusado.")
            print(f"{hora_atual} Erro: O destinatário {to_email} foi recusado.")
        except smtplib.SMTPDataError:
            logging.error(f"{hora_atual} Erro ao enviar o e-mail: Problema com os dados enviados.")
            print(f"{hora_atual} Erro ao enviar o e-mail: Problema com os dados enviados.")
        except Exception as e:
            logging.error(f"{hora_atual} Erro inesperado ao enviar o e-mail: {e}")
            print(f"{hora_atual} Erro inesperado ao enviar o e-mail: {e}")
        finally:
            server.quit()

    except FileNotFoundError:
        logging.error(f"{hora_atual} Arquivo de configuração 'config.ini' não encontrado.")
        print(f"{hora_atual} Erro: Arquivo de configuração 'config.ini' não encontrado.")
    except KeyError as e:
        logging.error(f"{hora_atual} Erro: A chave {e} não foi encontrada no arquivo de configuração.")
        print(f"{hora_atual} Erro: A chave {e} não foi encontrada no arquivo de configuração.")
    except Exception as e:
        logging.error(f"{hora_atual} Erro inesperado: {e}")
        print(f"{hora_atual} Erro inesperado: {e}")
