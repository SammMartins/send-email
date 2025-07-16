# bibliotecas
import streamlit as st
from streamlit_extras.colored_header import colored_header

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

    return 