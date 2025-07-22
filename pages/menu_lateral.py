# bibliotecas
import streamlit as st
from streamlit_extras.colored_header import colored_header
from pages.login_state import tela_de_login

def menu_lateral():
    menu_lateral = st.sidebar
    with menu_lateral:

        colored_header(
            label=':blue[SEND-EMAIL :material/send:]',
            description="Projeto para automatizar o envio de e-mails",
            color_name="blue-70",
        )

        # Links para as páginas
        st.subheader("Menu de Navegação")
        st.page_link("pages/tela_envio.py", icon=":material/send:", label="Enviar E-mail")
        st.page_link("pages/gerenciar_contatos.py", icon=":material/contacts:", label="Gerenciar Contatos")
        st.page_link("pages/log.py", icon=":material/overview:", label="Log")
        st.divider()
        logout = st.button("Logout", icon=":material/logout:", on_click=lambda: st.session_state.clear(), help="Sair da sessão atual")
        if logout:
            st.tela_de_login()  # Redireciona para a tela de login após logout

    return 