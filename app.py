import streamlit as st
from email_service.email_client import EmailClient

def main():
    st.title('Envio de E-mails com Streamlit')
    
    recipient = st.text_input('Destinatário do E-mail')
    subject = st.text_input('Assunto do E-mail')
    body = st.text_area('Corpo do E-mail')
    
    if st.button('Enviar E-mail'):
        email_client = EmailClient()
        if email_client.send_email(recipient, subject, body):
            st.success('E-mail enviado com sucesso!')
        else:
            st.error('Erro ao enviar o e-mail.')

if __name__ == '__main__':
    main()
