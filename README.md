❄️ Verificador de Code Freezing

O **Verificador de Code Freezing** é uma ferramenta desenvolvida em Python que permite identificar se uma empresa está em período de *code freeze* — ou seja, se o ambiente de produção está bloqueado para novas deploys. Essa verificação auxilia times de desenvolvimento a evitarem envios indevidos de código durante períodos críticos, como finais de ano, black friday, ou qualquer outro intervalo definido pela organização.

 📌 Funcionalidade

- Verifica, com base em regras pré-definidas (datas, arquivos de configuração, APIs, etc.), se o sistema está em período de congelamento de código.

🚀 Como usar

1. Clone o repositório:

   bash
   git clone https://github.com/seuusuario/verificador-code-freezing.git
   cd verificador-code-freezing

2. (Opcional) Crie e ative um ambiente virtual:

    python -m venv venv
    ource venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Instale as dependências:
    
   pip install -r requirements.txt

4. Execute o script:

    python code-freezing.py

