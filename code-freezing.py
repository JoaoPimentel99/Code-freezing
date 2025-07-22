# Importa módulos padrão do Python
import datetime  # Para trabalhar com datas
import logging   # Para gerar mensagens de log (informações, erros, etc)
import os        # Para acessar variáveis de ambiente
import sys       # Para encerrar o programa com códigos de saída

# Importa o PyYAML para ler arquivos YAML
import yaml

# Define o nome do arquivo de configuração
CONFIG_FILE = "config.yml"
# Pega o login do usuário GitLab a partir de uma variável de ambiente
GITLAB_USER_LOGIN = os.getenv("GITLAB_USER_LOGIN")

# Configura o sistema de logs
# Formato: [data] [nível] - mensagem
# Exemplo: [10-25-2024 03:30:45] [INFO] - Usuário autorizado
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%m-%d-%Y %I:%M:%S",  # Formato da data no log (MM-DD-AAAA HH:MM:SS)
    level=logging.DEBUG  # Mostra todos os níveis de log (DEBUG, INFO, WARNING, ERROR)
)

def get_config(filename: str) -> dict:
    """Lê o arquivo YAML de configuração e retorna como um dicionário."""
    with open(filename) as f:
        return yaml.safe_load(f)  # Carrega o conteúdo do arquivo YAML com segurança

def unpack_config(config: dict) -> tuple:
    """Extrai os valores 'bypass_group' e 'freezing_dates' do config."""
    try:
        bypass_group = config["bypass_group"]  # Lista de usuários isentos
        freezing_dates = config["freezing_dates"]  # Períodos de congelamento de código
    except KeyError as e:
        # Se alguma chave estiver faltando no YAML, mostra erro e encerra
        logging.error(f"Campo ausente no arquivo '{CONFIG_FILE}': 'bypass_group' ou 'freezing_dates'")
        sys.exit(1)
    return (bypass_group, freezing_dates)  # Retorna os dois valores

def is_user_in_bypass_group(username: str, bypass_group: list) -> bool:
    """Verifica se o usuário está na lista de bypass (isento)."""
    return username in bypass_group  # Retorna True se o usuário for isento

def is_today_within_freezing_date(date_from: datetime.date, date_to: datetime.date) -> bool:
    """Verifica se a data atual está dentro do período de congelamento."""
    date_today = datetime.date.today()  # Data de hoje
    return date_from <= date_today <= date_to  # Verifica se hoje está entre 'from' e 'to'

def main():
    """Função principal que executa a lógica do script."""
    # Lê o arquivo de configuração
    config = get_config(CONFIG_FILE)
    # Extrai os dados necessários
    bypass_group, freezing_dates = unpack_config(config)

    # Verifica se o usuário está isento
    if is_user_in_bypass_group(GITLAB_USER_LOGIN, bypass_group):
        logging.info(f"{GITLAB_USER_LOGIN} está no grupo de bypass, liberado. Saindo.")
        sys.exit(0)  # Permite continuar (CI/CD pode prosseguir)
    else:
        # Verifica cada período de congelamento definido
        for period, date in freezing_dates.items():
            date_from = date.get("from")  # Data de início (ex: 2024-12-01)
            date_to = date.get("to")      # Data de fim (ex: 2024-12-31)
            logging.info(f"Verificando período: {period} ({date_from} até {date_to})")
            # Converte strings para objetos date, se necessário
            if isinstance(date_from, str):
                date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            if isinstance(date_to, str):
                date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            # Verifica se hoje está dentro do período
            if is_today_within_freezing_date(date_from, date_to):
                logging.warning(f"🚫 Hoje está no período '{period}'. Congelamento ativo. Bloqueando deploy.")
                sys.exit(1)  # Bloqueia (útil em CI/CD)

# Executa o script apenas se for chamado diretamente
if __name__ == '__main__':
    main()