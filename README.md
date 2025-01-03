# send-email

Este repositório contém um projeto para automatização do envio de e-mails para o setor de Suporte da empresa TIVIC.

## Novidades
1. Implementada funcionalidade de templates de e-mails mais ultilizados

## Tecnologias Utilizadas
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![STREAMLIT](https://img.shields.io/badge/streamlit-%23D42029.svg?style=for-the-badge&logo=streamlit&logoColor=white)

## Como Usar

### Pré-requisitos

- Python 3.x instalado
- Dependências necessárias listadas em `requirements.txt`

### Passos para Executar

1. Clone o repositório:
    ```bash
    git clone https://github.com/SammMartins/send-email.git
    cd send-email
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    python -m venv env
    source env/bin/activate  # No Windows use `env\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure suas credenciais de email no arquivo de configuração (ex: `.env`).

5. Execute o script de envio de email:
    ```bash
    streamlit run app.py
    ```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.
