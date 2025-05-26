# config/settings.py - Configurações otimizadas para Streamlit Cloud
import os
import streamlit as st
from pathlib import Path

class Settings:
    # Configurações básicas
    APP_NAME = "Matriz de Risco SESP-PR"
    VERSION = "1.0.0"
    
    # Detectar ambiente
    IS_STREAMLIT_CLOUD = "STREAMLIT_SHARING" in os.environ or "STREAMLIT_CLOUD" in os.environ
    DEBUG = not IS_STREAMLIT_CLOUD
    
    # Configurações de banco
    if IS_STREAMLIT_CLOUD:
        # No Streamlit Cloud, usar path relativo
        DATABASE_URL = "sqlite:///data/database.db"
    else:
        # Local, usar path absoluto
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database.db")
    
    # Diretórios
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    EXPORT_DIR = BASE_DIR / "exports" / "output"
    TEMPLATE_DIR = BASE_DIR / "exports" / "templates"
    
    # Criar diretórios se não existirem
    DATA_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Configurações de export
    EXPORT_PATH = str(EXPORT_DIR)
    TEMPLATE_PATH = str(TEMPLATE_DIR)
    
    # Configurações de UI
    PAGE_CONFIG = {
        "page_title": APP_NAME,
        "page_icon": "🏗️",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # Informações do desenvolvedor
    DEVELOPER_INFO = {
        "organization": "Centro de Engenharia e Arquitetura",
        "department": "Secretaria de Segurança Pública do Paraná",
        "contact": "engenharia@sesp.pr.gov.br"
    }
    
    @classmethod
    def get_db_path(cls):
        """Retorna o caminho do banco de dados"""
        return cls.DATA_DIR / "database.db"
    
    @classmethod
    def is_first_run(cls):
        """Verifica se é a primeira execução (banco não existe)"""
        return not cls.get_db_path().exists()
    
    @classmethod
    def get_environment_info(cls):
        """Retorna informações do ambiente atual"""
        return {
            "environment": "Streamlit Cloud" if cls.IS_STREAMLIT_CLOUD else "Local",
            "debug": cls.DEBUG,
            "database_path": str(cls.get_db_path()),
            "base_directory": str(cls.BASE_DIR)
        }

# Instância global das configurações
settings = Settings()

# Função para configurar streamlit (para compatibilidade com Cloud)
def configure_streamlit():
    """Configura o Streamlit com as configurações padrão"""
    if not hasattr(st, '_is_configured'):
        # Aplicar configurações apenas uma vez
        try:
            st.set_page_config(**settings.PAGE_CONFIG)
            st._is_configured = True
        except st.errors.StreamlitAPIException:
            # Page config já foi definido
            pass
