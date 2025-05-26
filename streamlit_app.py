"""
streamlit_app.py - Entry point para Streamlit Cloud
Coloque este arquivo na RAIZ do repositório GitHub
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Adicionar diretórios ao path
root_path = Path(__file__).parent
sys.path.append(str(root_path))

# Configuração da página (deve vir antes de qualquer st.xxx)
st.set_page_config(
    page_title="Matriz de Risco SESP-PR",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importações necessárias
try:
    from config.database import init_database
    from config.settings import settings
    from scripts.load_initial_data import load_sample_data
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    st.stop()

# Inicializar banco de dados automaticamente no Streamlit Cloud
@st.cache_data
def initialize_app():
    """Inicializa a aplicação apenas uma vez"""
    try:
        # Criar diretório de dados se não existir
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Inicializar banco se não existir
        db_path = Path("data/database.db")
        if not db_path.exists():
            st.info("🔧 Inicializando banco de dados...")
            init_database()
            load_sample_data()
            st.success("✅ Banco inicializado com sucesso!")
        
        return True
    except Exception as e:
        st.error(f"❌ Erro ao inicializar aplicação: {e}")
        return False

def main():
    """Função principal da aplicação"""
    
    # Inicializar aplicação
    if not initialize_app():
        st.stop()
    
    # Título principal
    st.title("🏗️ " + settings.APP_NAME)
    st.markdown("---")
    
    st.markdown("""
    ## Bem-vindo ao Sistema de Matriz de Risco
    
    Este sistema foi desenvolvido para automatizar a criação de matrizes de risco para obras de segurança pública.
    
    ### Como usar:
    1. **📝 Entrada da Obra**: Descreva as características da sua obra
    2. **⚖️ Seleção de Riscos**: Revise e selecione os riscos aplicáveis
    3. **🔧 Customização**: Ajuste probabilidades e impactos conforme necessário
    4. **📊 Exportação**: Gere sua matriz de risco em PDF, Excel ou Word
    
    ### Navegação:
    Use o menu lateral para navegar entre as páginas do sistema.
    
    ---
    
    ### 🚀 Deploy Status
    - **Ambiente:** Streamlit Cloud
    - **Fonte:** GitHub Repository
    - **Status:** ✅ Online
    """)
    
    # Sidebar com informações
    with st.sidebar:
        st.markdown("## 📋 Menu Principal")
        st.markdown("""
        Navegue pelas páginas usando os links acima:
        
        - 📝 **01 Entrada Obra** - Definir características
        - ⚖️ **02 Seleção Riscos** - Escolher riscos aplicáveis
        - 🔧 **03 Customização** - Ajustar probabilidades
        - 📊 **04 Exportação** - Gerar matriz final
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ Informações do Sistema")
        st.markdown(f"**Versão:** 1.0.0")
        st.markdown(f"**Ambiente:** Streamlit Cloud")
        st.markdown(f"**GitHub:** Conectado")
        
        # Status do banco de dados
        try:
            from core.services.risco_service import RiscoService
            riscos = RiscoService.get_all_riscos()
            st.markdown(f"**Riscos Cadastrados:** {len(riscos)}")
        except:
            st.markdown("**Riscos Cadastrados:** Carregando...")
        
        st.markdown("---")
        st.markdown("### 🆘 Suporte")
        st.markdown("Em caso de problemas, contate:")
        st.markdown("**Centro de Engenharia SESP-PR**")

if __name__ == "__main__":
    main()
