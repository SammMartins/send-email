import streamlit as st
from utils import create_email, informativo_atualizacao, informativo_indisponibilidade, notificacao
from pages import menu_lateral
from pages.login_state import tela_de_login
from email_service import enviar_email

if st.session_state["autenticado"] == False:
    st.warning("Você precisa estar autenticado para acessar esta página.")
    tela_de_login()
    st.stop()
else:
    menu_lateral()

st.title(':blue[SEND-EMAIL :material/send:]', anchor = False)
template_opcao1 = "CRIAR NO E-MAIL"
template_opcao2 = "INFORMATIVO DE ATUALIZAÇÃO DESKTOP"
template_opcao3 = "INFORMATIVO DE INDISPONIBILIDADE"
template_opcao4 = "NOTIFICAÇÃO NA's NP's"

col1, col2, col3 = st.columns([1, 0.7, 0.3])

template_container = col1.container(border=True)
template_selecionado = template_container.selectbox("SELECIONE O TEMPLATE DE E-MAIL", options=[template_opcao1, template_opcao2, template_opcao3, template_opcao4], index=0, help='Selecione o template de e-mail que deseja utilizar.')

help_template_container = col2.container(border=False)
help_template_container.markdown('<br>', unsafe_allow_html=True)
# help_template_container.write(':material/info: **Escolha um template de e-mail, ou crie um do zero.**')

st.divider()

if template_selecionado == template_opcao1:
    create_email()
elif template_selecionado == template_opcao2:
    informativo_atualizacao()
elif template_selecionado == template_opcao3:
    informativo_indisponibilidade()
elif template_selecionado == template_opcao4:
    notificacao()
else:
    create_email()