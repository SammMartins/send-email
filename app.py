import streamlit as st
from pages import menu_lateral, tela_de_login


# -------------------------------------- Configurações da página
def main():
    st.session_state["autenticado"] = False  # Inicializa o estado de autenticação como falso
    tela_de_login()
    if st.session_state["autenticado"] == True:
        menu_lateral()

# -------------------------------------- Autenticação --------------------------------------
if __name__ == '__main__':
    main()    
        