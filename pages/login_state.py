# 1- Verificação Inicial: Quando o usuário abre a aplicação, o código verifica na "memória" (st.session_state) 
#    se existe uma indicação de que ele está autenticado.
from email_validator import validate_email, EmailNotValidError
import streamlit as st

# Define o domínio permitido para login
DOMINIO_PERMITIDO = "tivic.com.br"
SENHA_ACESSO = "huZ!NcyE8cMdQD3"


# Configurações geral das páginas
st.set_page_config(
    page_title='SEND-EMAIL', 
    page_icon=':blue[:material/send:]', 
    initial_sidebar_state = 'collapsed',
    layout='wide',
)


def tela_de_login():
    """
    Exibe a tela de login e processa a autenticação do usuário.
    """
    coluna1, coluna2, coluna3 = st.columns([1, 1.5, 1]) 
    with coluna2:
        st.write("Por favor, utilize seu e-mail corporativo para acessar.")

        # Campos do formulário de login
        with st.form("login_form"):
            email = st.text_input("Seu e-mail corporativo", placeholder="exemplo@exemplo.com.br")
            email = email.strip()
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            submit_button = st.form_submit_button("Entrar", disabled = False)

        if submit_button:
            if not email:
                st.error("Por favor, insira o seu e-mail.")
                return
            elif senha != SENHA_ACESSO:
                st.error("Senha incorreta. Tente novamente.")
                return
            else:
                try:
                    # Valida o formato do e-mail e extrai as informações
                    validacao = validate_email(email, check_deliverability=False)
                    email_dominio = validacao.domain

                    # Verifica se o domínio é o permitido
                    if email_dominio == DOMINIO_PERMITIDO:
                        st.success("Login bem-sucedido! Acesso a ferramenta concedido.")
                        # Armazena o status de autenticação e o e-mail na memória da sessão
                        st.session_state["autenticado"] = True
                        st.session_state["email_usuario"] = email
                    else:
                        st.error(f"Acesso negado. Domínio do e-mail não permitido.")

                except EmailNotValidError as e:
                    # Exibe um erro se o e-mail for inválido
                    st.error(f"O endereço de e-mail é inválido: {e}")


def logout():
    """
    Realiza o logout do usuário limpando o estado da sessão.
    """
    st.session_state["autenticado"] = False
    st.session_state.pop("email_usuario", None) # Remove o e-mail do usuário
    st.rerun()            