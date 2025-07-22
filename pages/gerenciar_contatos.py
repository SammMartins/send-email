import streamlit as st
import toml
import os
import pandas as pd
from pages import menu_lateral
from pages.login_state import tela_de_login

def tela_gerenciar_contatos():
    if st.session_state["autenticado"] == False:
        st.warning("Você precisa estar autenticado para acessar esta página.")
        tela_de_login()
        st.stop()
    else:
        menu_lateral()

    st.title(':blue[GERENCIAR CONTATOS :material/contacts:]', anchor=False)
    st.markdown("Gerencie listas de contatos e seus dados de forma simples e intuitiva.")
    
    # Carregar dados do arquivo TOML
    def carregar_contatos():
        try:
            with open("lista_contatos.toml", "r", encoding="utf-8") as file:
                return toml.load(file)
        except FileNotFoundError:
            st.error("Arquivo lista_contatos.toml não encontrado!")
            return {}
        except Exception as e:
            st.error(f"Erro ao carregar arquivo TOML: {str(e)}")
            return {}
    
    # Salvar dados no arquivo TOML
    def salvar_contatos(data):
        try:
            with open("lista_contatos.toml", "w", encoding="utf-8") as file:
                toml.dump(data, file)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar arquivo TOML: {str(e)}")
            return False
    
    # Validar email
    def validar_email(email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    # Carregar dados
    data = carregar_contatos()
    
    if not data:
        st.stop()
    
    # Estatísticas gerais
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        total_listas = len(data.keys())
        total_contatos = sum(len(lista.get('Contatos', [])) for lista in data.values())
        
        col1.metric("📋 Total de Listas", total_listas)
        col2.metric("👥 Total de Contatos", total_contatos)
        
        # Calcular lista com mais contatos
        if data:
            lista_maior = max(data.items(), key=lambda x: len(x[1].get('Contatos', [])))
            col3.metric("📊 Maior Lista", f"{lista_maior[0]}", f"{len(lista_maior[1].get('Contatos', []))} contatos")
            
            # Média de contatos por lista
            media_contatos = total_contatos / total_listas if total_listas > 0 else 0
            col4.metric("📈 Média por Lista", f"{media_contatos:.1f}")
    
    st.divider()
    
    # Tabs principais
    tab_visualizar, tab_adicionar, tab_editar, tab_excluir, tab_exportar = st.tabs([
        ":material/visibility: Visualizar", 
        ":material/add_circle: Adicionar", 
        ":material/edit: Editar", 
        ":material/delete: Excluir",
        ":material/download: Exportar"
    ])
    
    # ======================= TAB VISUALIZAR =======================
    with tab_visualizar:
        st.subheader("📋 Visualizar Contatos")
        
        if data:
            # Selectbox para escolher a lista
            listas_disponiveis = ["Todas as listas"] + list(data.keys())
            lista_selecionada = st.selectbox(
                "Selecione uma lista de contatos:",
                options=listas_disponiveis,
                index=0,
                key="visualizar_lista"
            )
            
            if lista_selecionada == "Todas as listas":
                # Mostrar todas as listas em uma visão resumida
                for nome_lista, conteudo_lista in data.items():
                    with st.expander(f"📁 {nome_lista} ({len(conteudo_lista.get('Contatos', []))} contatos)"):
                        contatos = conteudo_lista.get('Contatos', [])
                        if contatos:
                            df = pd.DataFrame(contatos)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info("Esta lista não possui contatos.")
            
            elif lista_selecionada in data and 'Contatos' in data[lista_selecionada]:
                contatos = data[lista_selecionada]['Contatos']
                
                st.write(f"**Lista:** {lista_selecionada}")
                st.write(f"**Total de contatos:** {len(contatos)}")
                
                # Filtros
                col_filtro1, col_filtro2 = st.columns(2)
                with col_filtro1:
                    filtro_nome = st.text_input("🔍 Filtrar por nome:", key="filtro_nome")
                with col_filtro2:
                    filtro_cidade = st.text_input("🔍 Filtrar por cidade:", key="filtro_cidade")
                
                # Aplicar filtros
                contatos_filtrados = contatos
                if filtro_nome:
                    contatos_filtrados = [c for c in contatos_filtrados if filtro_nome.lower() in c['Nome'].lower()]
                if filtro_cidade:
                    contatos_filtrados = [c for c in contatos_filtrados if 'Cidade' in c and filtro_cidade.lower() in c.get('Cidade', '').lower()]
                
                # Exibir contatos em uma tabela
                if contatos_filtrados:
                    df = pd.DataFrame(contatos_filtrados)
                    st.dataframe(df, use_container_width=True)
                    st.info(f"Mostrando {len(contatos_filtrados)} de {len(contatos)} contatos")
                else:
                    if filtro_nome or filtro_cidade:
                        st.warning("Nenhum contato encontrado com os filtros aplicados.")
                    else:
                        st.info("Esta lista não possui contatos.")
        else:
            st.info("Nenhuma lista de contatos encontrada.")
    
    # ======================= TAB ADICIONAR =======================
    with tab_adicionar:
        st.subheader("➕ Adicionar Contato")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Opção para adicionar em lista existente ou criar nova
            opcao_adicao = st.radio(
                "Escolha uma opção:",
                ["Adicionar à lista existente", "Criar nova lista"],
                key="opcao_adicao"
            )
            
            if opcao_adicao == "Adicionar à lista existente":
                listas_disponiveis = list(data.keys())
                lista_destino = st.selectbox(
                    "Selecione a lista:",
                    options=listas_disponiveis,
                    key="lista_destino_existente"
                )
            else:
                lista_destino = st.text_input(
                    "Nome da nova lista:",
                    placeholder="Ex: Nova_Lista_Clientes",
                    key="nova_lista_nome",
                    help="Use apenas letras, números e underscores. Não use espaços."
                )
                
                # Validar nome da nova lista
                if lista_destino and not lista_destino.replace('_', '').replace('-', '').isalnum():
                    st.warning("⚠️ Use apenas letras, números, hífens e underscores.")
        
        with col2:
            # Campos do contato
            nome_contato = st.text_input("Nome do contato:", key="novo_nome")
            email_contato = st.text_input("Email do contato:", key="novo_email")
            cidade_contato = st.text_input("Cidade (opcional):", key="nova_cidade")
            
            # Validação em tempo real
            if email_contato and not validar_email(email_contato):
                st.error("❌ Email inválido!")
        
        if st.button("💾 Adicionar Contato", type="primary"):
            if not nome_contato or not email_contato:
                st.error("Nome e email são obrigatórios!")
            elif not lista_destino:
                st.error("Selecione ou crie uma lista!")
            elif not validar_email(email_contato):
                st.error("Email inválido!")
            else:
                # Verificar se email já existe na lista
                email_existe = False
                if lista_destino in data and 'Contatos' in data[lista_destino]:
                    for contato in data[lista_destino]['Contatos']:
                        if contato['Email'].lower() == email_contato.lower():
                            email_existe = True
                            break
                
                if email_existe:
                    st.error("Este email já existe na lista selecionada!")
                else:
                    # Determinar próximo ID
                    if lista_destino in data and 'Contatos' in data[lista_destino]:
                        contatos_existentes = data[lista_destino]['Contatos']
                        if contatos_existentes:
                            proximo_id = max([c.get('Id', 0) for c in contatos_existentes]) + 1
                        else:
                            proximo_id = 1
                    else:
                        # Nova lista
                        data[lista_destino] = {'Contatos': []}
                        proximo_id = 1
                    
                    # Criar novo contato
                    novo_contato = {
                        'Id': proximo_id,
                        'Nome': nome_contato.strip(),
                        'Email': email_contato.strip().lower()
                    }
                    
                    if cidade_contato:
                        novo_contato['Cidade'] = cidade_contato.strip()
                    
                    # Adicionar à lista
                    data[lista_destino]['Contatos'].append(novo_contato)
                    
                    # Salvar
                    if salvar_contatos(data):
                        st.success(f"✅ Contato adicionado com sucesso à lista '{lista_destino}'!")
                        st.rerun()
    
    # ======================= TAB EDITAR =======================
    with tab_editar:
        st.subheader("✏️ Editar Contato")
        
        if data:
            col1, col2 = st.columns(2)
            
            with col1:
                # Selecionar lista
                listas_disponiveis = list(data.keys())
                lista_edicao = st.selectbox(
                    "Selecione a lista:",
                    options=listas_disponiveis,
                    key="lista_edicao"
                )
            
            if lista_edicao and 'Contatos' in data[lista_edicao]:
                contatos = data[lista_edicao]['Contatos']
                
                if contatos:
                    with col1:
                        # Criar opções para selectbox
                        opcoes_contatos = [f"ID {c['Id']} - {c['Nome']} ({c['Email']})" for c in contatos]
                        contato_selecionado_str = st.selectbox(
                            "Selecione o contato:",
                            options=opcoes_contatos,
                            key="contato_edicao"
                        )
                        
                        # Extrair ID do contato selecionado
                        if contato_selecionado_str:
                            contato_id = int(contato_selecionado_str.split(' ')[1])
                            contato_atual = next(c for c in contatos if c['Id'] == contato_id)
                            
                            with col2:
                                # Campos de edição
                                novo_nome = st.text_input(
                                    "Nome:", 
                                    value=contato_atual['Nome'], 
                                    key="edit_nome"
                                )
                                novo_email = st.text_input(
                                    "Email:", 
                                    value=contato_atual['Email'], 
                                    key="edit_email"
                                )
                                nova_cidade = st.text_input(
                                    "Cidade:", 
                                    value=contato_atual.get('Cidade', ''), 
                                    key="edit_cidade"
                                )
                                
                                # Validação em tempo real
                                if novo_email and not validar_email(novo_email):
                                    st.error("❌ Email inválido!")
                            
                            if st.button("💾 Salvar Alterações", type="primary"):
                                if not novo_nome or not novo_email:
                                    st.error("Nome e email são obrigatórios!")
                                elif not validar_email(novo_email):
                                    st.error("Email inválido!")
                                else:
                                    # Verificar se email já existe (exceto o atual)
                                    email_existe = False
                                    for contato in contatos:
                                        if contato['Id'] != contato_id and contato['Email'].lower() == novo_email.lower():
                                            email_existe = True
                                            break
                                    
                                    if email_existe:
                                        st.error("Este email já existe em outro contato da lista!")
                                    else:
                                        # Atualizar contato
                                        for i, contato in enumerate(contatos):
                                            if contato['Id'] == contato_id:
                                                data[lista_edicao]['Contatos'][i]['Nome'] = novo_nome.strip()
                                                data[lista_edicao]['Contatos'][i]['Email'] = novo_email.strip().lower()
                                                if nova_cidade:
                                                    data[lista_edicao]['Contatos'][i]['Cidade'] = nova_cidade.strip()
                                                elif 'Cidade' in data[lista_edicao]['Contatos'][i]:
                                                    del data[lista_edicao]['Contatos'][i]['Cidade']
                                                break
                                        
                                        if salvar_contatos(data):
                                            st.success("✅ Contato atualizado com sucesso!")
                                            st.rerun()
                else:
                    st.info("Esta lista não possui contatos para editar.")
        else:
            st.info("Nenhuma lista de contatos encontrada.")
    
    # ======================= TAB EXCLUIR =======================
    with tab_excluir:
        st.subheader("🗑️ Excluir Contato ou Lista")
        
        opcao_exclusao = st.radio(
            "O que deseja excluir?",
            ["Contato específico", "Lista inteira"],
            key="opcao_exclusao"
        )
        
        if opcao_exclusao == "Contato específico":
            col1, col2 = st.columns(2)
            
            with col1:
                listas_disponiveis = list(data.keys())
                lista_exclusao = st.selectbox(
                    "Selecione a lista:",
                    options=listas_disponiveis,
                    key="lista_exclusao_contato"
                )
            
            if lista_exclusao and 'Contatos' in data[lista_exclusao]:
                contatos = data[lista_exclusao]['Contatos']
                
                if contatos:
                    with col1:
                        opcoes_contatos = [f"ID {c['Id']} - {c['Nome']} ({c['Email']})" for c in contatos]
                        contato_excluir_str = st.selectbox(
                            "Selecione o contato:",
                            options=opcoes_contatos,
                            key="contato_exclusao"
                        )
                    
                    if contato_excluir_str:
                        contato_id = int(contato_excluir_str.split(' ')[1])
                        
                        with col2:
                            st.warning("⚠️ Esta ação não pode ser desfeita!")
                            if st.button("🗑️ Excluir Contato", type="secondary"):
                                # Remover contato
                                data[lista_exclusao]['Contatos'] = [
                                    c for c in contatos if c['Id'] != contato_id
                                ]
                                
                                if salvar_contatos(data):
                                    st.success("✅ Contato excluído com sucesso!")
                                    st.rerun()
                else:
                    st.info("Esta lista não possui contatos para excluir.")
        
        else:  # Excluir lista inteira
            listas_disponiveis = list(data.keys())
            lista_excluir = st.selectbox(
                "Selecione a lista para excluir:",
                options=listas_disponiveis,
                key="lista_exclusao_completa"
            )
            
            if lista_excluir:
                num_contatos = len(data[lista_excluir].get('Contatos', []))
                st.warning(f"⚠️ Esta ação irá excluir a lista '{lista_excluir}' com {num_contatos} contatos e não pode ser desfeita!")
                
                # Confirmação dupla
                confirmacao = st.text_input(
                    f"Para confirmar, digite o nome da lista: '{lista_excluir}'",
                    key="confirmacao_exclusao"
                )
                
                if confirmacao == lista_excluir:
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col2:
                        if st.button("🗑️ Excluir Lista Completa", type="secondary"):
                            del data[lista_excluir]
                            
                            if salvar_contatos(data):
                                st.success(f"✅ Lista '{lista_excluir}' excluída com sucesso!")
                                st.rerun()
    
    # ======================= TAB EXPORTAR =======================
    with tab_exportar:
        st.subheader("📤 Exportar Dados")
        
        st.markdown("Exporte seus dados de contatos em diferentes formatos.")
        
        if data:
            # Escolher lista para exportar
            listas_disponiveis = ["Todas as listas"] + list(data.keys())
            lista_exportar = st.selectbox(
                "Selecione a lista para exportar:",
                options=listas_disponiveis,
                key="lista_exportar"
            )
            
            formato_exportacao = st.selectbox(
                "Selecione o formato:",
                ["CSV", "JSON", "Excel"],
                key="formato_exportacao"
            )
            
            if st.button("📥 Gerar Arquivo", type="primary"):
                try:
                    if lista_exportar == "Todas as listas":
                        # Criar um DataFrame com todos os contatos
                        todos_contatos = []
                        for nome_lista, conteudo_lista in data.items():
                            contatos = conteudo_lista.get('Contatos', [])
                            for contato in contatos:
                                contato_com_lista = contato.copy()
                                contato_com_lista['Lista'] = nome_lista
                                todos_contatos.append(contato_com_lista)
                        
                        if todos_contatos:
                            df = pd.DataFrame(todos_contatos)
                            # Reorganizar colunas
                            cols = ['Lista'] + [col for col in df.columns if col != 'Lista']
                            df = df[cols]
                        else:
                            st.warning("Nenhum contato encontrado para exportar.")
                            return
                    else:
                        # Exportar apenas uma lista
                        contatos = data[lista_exportar].get('Contatos', [])
                        if contatos:
                            df = pd.DataFrame(contatos)
                        else:
                            st.warning(f"A lista '{lista_exportar}' não possui contatos para exportar.")
                            return
                    
                    # Gerar arquivo baseado no formato
                    if formato_exportacao == "CSV":
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv_data,
                            file_name=f"contatos_{lista_exportar.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                    elif formato_exportacao == "JSON":
                        json_data = df.to_json(orient='records', indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"contatos_{lista_exportar.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                    elif formato_exportacao == "Excel":
                        # Para Excel, usamos buffer em memória
                        import io
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False, sheet_name='Contatos')
                        
                        st.download_button(
                            label="📥 Download Excel",
                            data=buffer.getvalue(),
                            file_name=f"contatos_{lista_exportar.replace(' ', '_')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    st.success(f"✅ Arquivo {formato_exportacao} gerado com sucesso!")
                    
                except Exception as e:
                    st.error(f"Erro ao gerar arquivo: {str(e)}")
        else:
            st.info("Nenhuma lista de contatos encontrada para exportar.")

if __name__ == "__main__":
    tela_gerenciar_contatos()
