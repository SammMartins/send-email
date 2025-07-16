import streamlit as st
import toml
import re
import time 
from pages import menu_lateral
from email_service import enviar_email

def create_email():
    left_column1, separador, right_column1 = st.columns([1, 0.1, 1])

    assunto_email = left_column1.text_input('ASSUNTO DO E-MAIL', placeholder = 'Digite o assunto do e-mail', value = '', autocomplete="")

    saudacao = left_column1.text_input(
            'SAUDAÇÃO DO E-MAIL', 
            placeholder = 'Utilize "{Nome}" para ser substituido pelo nome do contato', 
            value = 'Olá, {Nome}. Bom dia!', 
            autocomplete="", 
            max_chars = 30,
            help='Exemplo de uso: "Olá, {Nome}. Bom dia!" Nesse caso, "{Nome}" será substituido pelo nome do contato.'
        )

    corpo_email = left_column1.text_area(
            'CORPO DO E-MAIL',
            max_chars = 5000, 
            placeholder = 'Digite o corpo do e-mail...', 
            value='', 
            height=340,
            help='Utilize ** ** para negrito e __ __ para itálico. Para listas, utilize * ou 1. antes do texto para criar listas não ordenadas ou ordenadas, respectivamente.'
        )


    with right_column1:
        # Carregar o conteúdo do arquivo TOML
        with open("lista_contatos.toml", "r") as file:
            data = toml.load(file)

        tabelas_principais = list(data.keys())

        col_esq, separador, col_dir = st.columns([1, 0.1, 1])

        assinatura = col_esq.selectbox("ASSINATURA DO E-MAIL", options=['Atendimento','José', 'Rodrigo', 'Vinícius', 'Sammuel'], index=None, help='Selecione a assinatura que deseja utilizar no e-mail.', placeholder='Selecione a assinatura do e-mail')
        
        # Multiselect para selecionar as listas de contatos
        lista_selecionada = col_dir.multiselect(
            "SELECIONE O(S) CONTATO(S)",
            options=tabelas_principais,
            default=[],  # Inicialmente vazio
            placeholder="Selecione O(s) Contato(s)",
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
            match_variavel_invalida = re.search(r'{(?!Nome\b)[^}]+}', saudacao)
            if match_variavel_invalida:
                variavel_encontrada = match_variavel_invalida.group()
                st.error(
                    f'A saudação contém uma variável inválida: {variavel_encontrada}. '
                    'Use apenas {{Nome}} para ser substituído pelo nome do contato. '
                    'Exemplo de uso incorreto: {{nome}}, {{NOME}}, {{Prezados}}.'
                )
            else:
                # Se não encontrou variável inválida, prossegue com o envio
                st.toast('Enviando e-mail...', icon='📧')
                
                envio = enviar_email(assunto_email, saudacao, corpo_email, lista_selecionada, assinatura)
                time.sleep(2)
                
                if envio:
                    st.toast('E-mail enviado com sucesso!', icon='📧')
                else:
                    st.toast(':red[Erro ao enviar e-mail]', icon=':material/priority_high:')

def informativo_atualizacao():
    left_column1, separador, right_column1 = st.columns([1, 0.1, 1])

    assunto_email = left_column1.text_input('ASSUNTO DO E-MAIL', placeholder = 'Digite o assunto do e-mail', value = 'Informativo de Atualização do Sistema eTrânsito Desktop', autocomplete="")

    saudacao = left_column1.text_input(
            'SAUDAÇÃO DO E-MAIL', 
            placeholder = 'Utilize "{Nome}" para ser substituido pelo nome do contato', 
            value = '{Nome}, bom dia!', 
            autocomplete="", 
            max_chars = 30,
            help='Exemplo de uso: "{Nome}, bom dia!" Nesse caso, "{Nome}" será substituido pelo nome do contato.'
        )

    corpo_email = left_column1.text_area(
        'CORPO DO E-MAIL',
        max_chars = 5000, 
        placeholder = 'Digite o corpo do e-mail...', 
        value=
            'Aqui estão as descrições dos novos recursos e ajustes do sistema eTransito DESKTOP, organizadas conforme solicitado: \n\n'
            '**NOVOS RECURSOS:** \n'
            '1. **Recurso 1:** Descrição do recurso 1. \n\n'
            '**RECURSOS AJUSTADOS:** \n'
            '1. **Recurso 1 Ajustado:** Descrição do recurso 1 ajustado. \n\n'
            '**Feliz em ajudar, estamos a disposição para tirar quaisquer dúvidas.** \n\n'
            '__Atenciosamente,__ \n',
        height=340,
        help='Utilize ** ** para negrito e __ __ para itálico. Para listas, utilize * ou 1. antes do texto para criar listas não ordenadas ou ordenadas, respectivamente.'
    )

    with right_column1:
        # Carregar o conteúdo do arquivo TOML
        with open("lista_contatos.toml", "r") as file:
            data = toml.load(file)

        tabelas_principais = list(data.keys())

        col_esq, separador, col_dir = st.columns([1, 0.1, 1])

        assinatura = col_esq.selectbox("ASSINATURA DO E-MAIL", options=['Atendimento','José', 'Rodrigo', 'Vinícius', 'Sammuel'], index=0, help='Selecione a assinatura que deseja utilizar no e-mail.', placeholder='Selecione a assinatura do e-mail')
        
        # Multiselect para selecionar as listas de contatos
        lista_selecionada = col_dir.multiselect(
            "SELECIONE O(S) CONTATO(S)",
            options=tabelas_principais,
            default=['Clientes_Desktop'],  # Inicialmente vazio
            placeholder="Selecione O(s) Contato(s)",
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
        elif re.search(r'{(?!Nome\b)[^}]+}', saudacao):
            st.error(f'A saudação contém uma variável inválida: {re.search(r"{(?!Nome\b)[^}]+}", saudacao).group()}. Use apenas {{Nome}} para ser substituído pelo nome do contato. Exemplo de uso incorreto: {{nome}}, {{NOME}}, {{Prezados}}.')
        else:

            st.toast('Enviando e-mail...', icon='📧')
            
            envio = enviar_email(assunto_email, saudacao, corpo_email, lista_selecionada, assinatura)
            time.sleep(2)
            
            if envio:
                st.toast('E-mail enviado com sucesso!', icon='📧')
            else:
                st.toast(':red[Erro ao enviar e-mail]', icon=':material/priority_high:')    

def informativo_indisponibilidade():
    left_column1, separador, right_column1 = st.columns([1, 0.1, 1])

    assunto_email = left_column1.text_input('ASSUNTO DO E-MAIL', placeholder = 'Digite o assunto do e-mail', value = 'Informativo de Indisponibilidade do Sistema [NOME DO SISTEMA]', autocomplete="")

    saudacao = left_column1.text_input(
            'SAUDAÇÃO DO E-MAIL', 
            placeholder = 'Utilize "{Nome}" para ser substituido pelo nome do contato', 
            value = 'Olá, {Nome}. Boa tarde!', 
            autocomplete="", 
            max_chars = 30,
            help='Exemplo de uso: "Olá, {Nome}. Bom dia!" Nesse caso, "{Nome}" será substituido pelo nome do contato.'
        )

    corpo_email = left_column1.text_area(
            'CORPO DO E-MAIL',
            max_chars = 5000, 
            placeholder = 'Digite o corpo do e-mail...', 
            value=
                'Informamos que o **sistema [NOME DO SISTEMA] estará indisponível** para atualização / manutenção, hoje, às [HORÁRIO DE INÍCIO]. \n\n'
                '**A previsão para retornar à normalidade é de [TEMPO DE INDISPONIBILIDADE] à [TEMPO DE INDISPONIBILIDADE].** \n\n'
                'Agradecemos a compreensão e estamos à disposição para quaisquer dúvidas. \n\n'
                '__Atenciosamente,__ \n',
            height=340,
            help='Utilize ** ** para negrito e __ __ para itálico. Para listas, utilize * ou 1. antes do texto para criar listas não ordenadas ou ordenadas, respectivamente.'
        )


    with right_column1:
        # Carregar o conteúdo do arquivo TOML
        with open("lista_contatos.toml", "r") as file:
            data = toml.load(file)

        tabelas_principais = list(data.keys())

        col_esq, separador, col_dir = st.columns([1, 0.1, 1])

        assinatura = col_esq.selectbox("ASSINATURA DO E-MAIL", options=['Atendimento','José', 'Rodrigo', 'Vinícius', 'Sammuel'], index=0, help='Selecione a assinatura que deseja utilizar no e-mail.', placeholder='Selecione a assinatura do e-mail')
        
        # Multiselect para selecionar as listas de contatos
        lista_selecionada = col_dir.multiselect(
            "SELECIONE O(S) CONTATO(S)",
            options=tabelas_principais,
            default=[],  # Inicialmente vazio
            placeholder="Selecione O(s) Contato(s)",
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
        elif re.search(r'{(?!Nome\b)[^}]+}', saudacao):
            st.error(f'A saudação contém uma variável inválida: {re.search(r"{(?!Nome\b)[^}]+}", saudacao).group()}. Use apenas {{Nome}} para ser substituído pelo nome do contato. Exemplo de uso incorreto: {{nome}}, {{NOME}}, {{Prezados}}.')
        else:

            st.toast('Enviando e-mail...', icon='📧')
            
            envio = enviar_email(assunto_email, saudacao, corpo_email, lista_selecionada, assinatura)
            time.sleep(2)
            
            if envio:
                st.toast('E-mail enviado com sucesso!', icon='📧')
            else:
                st.toast(':red[Erro ao enviar e-mail]', icon=':material/priority_high:')
    

def notificacao():
    left_column1, separador, right_column1 = st.columns([1, 0.1, 1])

    assunto_email = left_column1.text_input('ASSUNTO DO E-MAIL', placeholder = 'Digite o assunto do e-mail', value = 'Notificações de [NOME DA CIDADE OU SIGLA]', autocomplete="")

    saudacao = left_column1.text_input(
            'SAUDAÇÃO DO E-MAIL', 
            placeholder = 'Utilize "{Nome}" para ser substituido pelo nome do contato', 
            value = 'Olá, boa tarde!', 
            autocomplete="", 
            max_chars = 30,
            help='Exemplo de uso: "Olá, {Nome}. Bom dia!" Nesse caso, "{Nome}" será substituido pelo nome do contato.'
        )

    corpo_email = left_column1.text_area(
            'CORPO DO E-MAIL',
            max_chars = 5000, 
            placeholder = 'Digite o corpo do e-mail...', 
            value=
                'Segue as **notificações (NA e NP)** da cidade de [NOME DA CIDADE]. \n\n'
                '__Atenciosamente,__ \n',
            height=340,
            help='Utilize ** ** para negrito e __ __ para itálico. Para listas, utilize * ou 1. antes do texto para criar listas não ordenadas ou ordenadas, respectivamente.'
        )


    with right_column1:
        # Carregar o conteúdo do arquivo TOML
        with open("lista_contatos.toml", "r") as file:
            data = toml.load(file)

        tabelas_principais = list(data.keys())

        col_esq, separador, col_dir = st.columns([1, 0.1, 1])

        assinatura = col_esq.selectbox("ASSINATURA DO E-MAIL", options=['Atendimento','José', 'Rodrigo', 'Vinícius', 'Sammuel'], index=0, help='Selecione a assinatura que deseja utilizar no e-mail.', placeholder='Selecione a assinatura do e-mail')
        
        # Multiselect para selecionar as listas de contatos
        lista_selecionada = col_dir.multiselect(
            "SELECIONE O(S) CONTATO(S)",
            options=tabelas_principais,
            default=['Impressao'],
            placeholder="Selecione O(s) Contato(s)",
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

        # Se corpo do do e-mail contiver esse texto em alguma parte [NOME DA CIDADE] deve avisar que não preenchido corretamente
        if '[NOME DA CIDADE]' in corpo_email or '[NOME DA CIDADE OU SIGLA]' in assunto_email:
            st.error('Substitua o campo [NOME DA CIDADE] e [NOME DA CIDADE OU SIGLA] pelo nome da cidade.')
        else:
            # Verificar se está tudo preenchido
            if not assunto_email or not saudacao or not corpo_email or not lista_selecionada:
                st.error('Preencha todos os campos antes de enviar o e-mail.')
            elif re.search(r'{(?!Nome\b)[^}]+}', saudacao):
                st.error(f'A saudação contém uma variável inválida: {re.search(r"{(?!Nome\b)[^}]+}", saudacao).group()}. Use apenas {{Nome}} para ser substituído pelo nome do contato. Exemplo de uso incorreto: {{nome}}, {{NOME}}, {{Prezados}}.')
            else:

                st.toast('Enviando e-mail...', icon='📧')
                
                envio = enviar_email(assunto_email, saudacao, corpo_email, lista_selecionada, assinatura)
                time.sleep(2)
                
                if envio:
                    st.toast('E-mail enviado com sucesso!', icon='📧')
                else:
                    st.toast(':red[Erro ao enviar e-mail]', icon=':material/priority_high:')        