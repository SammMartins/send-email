import streamlit as st
import toml
from components import menu_lateral
from email_service import enviar_email
import time 

menu_lateral()

def main():
    st.title(':blue[SEND-EMAIL :material/send:]', anchor = False)
    st.subheader('Enviar E-mail', anchor = False)

    left_column1, separador, right_column1 = st.columns([1, 0.1, 1])

    assunto_email = left_column1.text_input('ASSUNTO DO E-MAIL', placeholder = 'Digite o assunto do e-mail', value = 'Informativo de Atualização do Sistema eTrânsito Desktop', autocomplete="")
    
    saudacao = left_column1.text_input(
            'SAUDAÇÃO DO E-MAIL', 
            placeholder = 'Utilize "{Nome}" para ser substituido pelo nome do contato', 
            value = 'Olá, {Nome}. Bom dia!', 
            autocomplete="", 
            max_chars = 30,
            help='Exemplo de uso: "Olá, {Nome}. Bom dia!" Nesse caso, "{Nome}" será substituido pelo nome do contato.'
        )
    
    corpo_email = left_column1.text_area('CORPO DO E-MAIL', max_chars = 5000, placeholder = 'Digite o corpo do e-mail', value='', height=340)

    
    with right_column1:
        # Carregar o conteúdo do arquivo TOML
        with open("lista_contatos.toml", "r") as file:
            data = toml.load(file)

        tabelas_principais = list(data.keys())

        col_esq, separador, col_dir = st.columns([1, 0.1, 1])

        assinatura = col_esq.selectbox("ASSINATURA DO E-MAIL", options=['José', 'Rodrigo', 'Vinícius', 'Sammuel'], index=None, help='Selecione a assinatura que deseja utilizar no e-mail.', placeholder='Selecione a assinatura do e-mail')
        
        # Multiselect para selecionar as listas de contatos
        lista_selecionada = col_dir.multiselect(
            "Selecione a(s) lista(s) de contatos",
            options=tabelas_principais,
            default=[],  # Inicialmente vazio
            placeholder="Selecione o(s) contato(s)",
            help="Selecione 1 ou mais listas de contatos para enviar o e-mail."
        )

        st.divider()
        st.markdown('Contatos selecionados:')

        container = st.container(border=True, height=345)
        with container:

            # Exibir a lista de contatos selecionada
            for lista in lista_selecionada:
                st.write(f"{lista}")

                # Verificar se há contatos diretamente na lista
                if "Contatos" in data[lista]:
                    for contato in data[lista]["Contatos"]:
                        st.write(f"{contato['Nome']} - E-mail: {contato['Email']}")
                else:
                    st.write('Nenhum contato encontrado para essa Lista.')

    st.divider()
    # Botão para enviar o e-mail
    if st.button(':blue[SEND-EMAIL :material/send:]', use_container_width=True):

        # Verificar se está tudo preenchido
        if not assunto_email or not saudacao or not corpo_email or not lista_selecionada:
            st.error('Preencha todos os campos antes de enviar o e-mail.')
        else:

            st.toast('Enviando e-mail...', icon='📧')
            
            envio = enviar_email(assunto_email, saudacao, corpo_email, lista_selecionada, assinatura)
            time.sleep(2)
            
            if envio:
                st.toast('E-mail enviado com sucesso!', icon='📧')
            else:
                st.toast(':red[Erro ao enviar e-mail]', icon=':material/priority_high:')

if __name__ == '__main__':
    main()
