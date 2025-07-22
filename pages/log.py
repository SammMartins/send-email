# ler arquivos do log
import os
import streamlit as st
from pages import menu_lateral
from pages.login_state import tela_de_login

if st.session_state["autenticado"] == False:
    st.warning("Você precisa estar autenticado para acessar esta página.")
    tela_de_login()
    st.stop()
else:
    menu_lateral()

def exibir_log_auditoria():
    """
    Lê o arquivo de log de auditoria e retorna seu conteúdo.
    """
    log_file_path = "log_auditoria.txt"  # Caminho do arquivo de log

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            log_content = file.read()
        return log_content
    else:
        return "Arquivo de log não encontrado."
    
def exibir_log_erros():
    """
    Lê o arquivo de log de erros e retorna seu conteúdo.
    """
    log_file_path = "log_erros.txt"  # Caminho do arquivo de log

    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            log_content = file.read()
        return log_content
    else:
        return "Arquivo de log não encontrado."    

st.title(':blue[LOG :material/overview:]', anchor=False)

# selecionar tipo de log
col1, col2 = st.columns([0.3, 0.7])
tipo_log_container = col1.container(border=True)

with tipo_log_container:
    tipo_log = st.selectbox("Selecione o tipo de log:", ["Log de Auditoria", "Log de Erros"], help="Escolha o tipo de log que deseja visualizar.")

st.divider()
st.markdown("<br>", unsafe_allow_html=True)

log_content = None  # Inicializa a variável

if tipo_log == "Log de Auditoria":
    st.header("Log de Auditoria")
    log_content = exibir_log_auditoria()
elif tipo_log == "Log de Erros":
    st.header("Log de Erros no envio de e-mails")
    log_content = exibir_log_erros()
else:
    st.warning("Selecione um tipo de log válido.")

if log_content:
    st.text_area("Conteúdo do Log", value=log_content, height=500)
else:
    st.warning("Nenhum log disponível.")
