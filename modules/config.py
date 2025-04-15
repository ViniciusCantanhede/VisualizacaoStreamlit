import streamlit as st

def setup_page_config():
    """Configura a página do Streamlit e define o CSS global"""
    
    st.set_page_config(
        page_title="Análise de Dados Espaciais",
        page_icon="🚀",
        layout="wide"
    )
    
    # CSS personalizado para melhorar a aparência
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            color: #0a3d62;
            text-align: center;
            margin-bottom: 1rem;
        }
        .section-header {
            font-size: 1.8rem;
            color: #3c6382;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 0.5rem;
        }
        .chart-container {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)