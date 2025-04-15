import streamlit as st
from modules.config import setup_page_config
from modules.data_loader import load_data
from modules.country_analysis import show_country_analysis
from modules.mission_analysis import show_mission_analysis
from modules.success_analysis import show_success_analysis
from modules.pdf_export import adicionar_secao_exportacao_pdf  # Nova importação

# Configuração da página
setup_page_config()

# Título principal
st.markdown("<h1 class='main-header'>🚀 Análise de Dados de Exploração Espacial Global</h1>", unsafe_allow_html=True)

# Carregar dados
df = load_data()

if df is not None:
    # Visão geral do dataset
    st.markdown("<h2 class='section-header'>Visão Geral dos Dados</h2>", unsafe_allow_html=True)
    st.write(f"**Total de registros:** {len(df)}")
    st.write(f"**Período analisado:** {df['Year'].min()} a {df['Year'].max()}")
    
    # Exibir as primeiras linhas para referência
    with st.expander("Visualizar amostra dos dados"):
        st.dataframe(df.head())
    
    # Análises principais
    show_country_analysis(df)
    show_mission_analysis(df)
    show_success_analysis(df)
    
    # Conclusão
    st.markdown("<h2 class='section-header'>Conclusões</h2>", unsafe_allow_html=True)
    st.markdown("""
    A análise exploratória dos dados de exploração espacial global revelou padrões significativos 
    que nos permitem compreender melhor este campo estratégico. As evidências apresentadas 
    fornecem insights valiosos sobre a dinâmica entre países, investimentos, tipos de missão 
    e sucesso no desenvolvimento espacial.

    Nossa análise destaca que a exploração espacial continua sendo um campo dominado por um número 
    relativamente pequeno de nações, com investimentos substanciais concentrados em potências tradicionais. 
    A distribuição desigual de missões e orçamentos reflete as realidades geopolíticas e econômicas 
    que moldam a corrida espacial moderna.

    O exame da relação entre orçamento e taxa de sucesso demonstrou que, embora exista uma correlação 
    positiva entre investimento e resultado bem-sucedido, esta relação não é linear nem universal. 
    Observamos que missões de menor orçamento podem alcançar taxas de sucesso comparáveis às de alto 
    custo quando executadas com expertise adequada e tecnologias maduras.

    A evolução temporal das missões espaciais ilustra claramente a transformação do setor ao longo 
    das décadas. O aumento nas missões não tripuladas reflete uma mudança de paradigma na abordagem 
    da exploração espacial, priorizando eficiência de custos e minimização de riscos humanos, 
    enquanto as missões tripuladas mantêm sua importância simbólica e científica.
    """)
    
    # Adicionar seção de exportação PDF
    adicionar_secao_exportacao_pdf(df)
    
else:
    st.error("Não foi possível carregar os dados. Verifique se o arquivo está no diretório correto.")