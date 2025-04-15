import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from modules.utils import set_plot_style, create_text_area

def show_mission_analysis(df):
    """Exibe análise resumida por tipo de missão"""
    st.markdown("<h2 class='section-header'>Análise por Tipo de Missão</h2>", unsafe_allow_html=True)
    
    # Espaço para explicação sobre tipos de missão
    mission_explanation = create_text_area(
        "sua explicação sobre tipos de missão",
        """
        **Observação**: A categoria de missões tripuladas e não tripuladas são fundamentais para saber como os
        diferentes tipos de missões espaciais são distribuídos ao longo do tempo e como isso se relaciona com o sucesso.
        Esta seção analisa os diferentes tipos de missão espacial, suas frequências, 
        características de custo e duração. Identificar os tipos mais comuns ajuda a 
        entender as prioridades na exploração espacial e como os recursos são alocados.
        """
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição de tipos de missão
        show_mission_types_distribution(df)
    
    with col2:
        # Orçamento médio por tipo de missão
        show_budget_by_mission_type(df)
    
    # Evolução dos tipos de missão ao longo do tempo
    show_mission_types_evolution(df)

def show_mission_types_distribution(df):
    """Exibe a distribuição dos tipos de missão"""
    st.subheader("Distribuição de Tipos de Missão")
    
    # Contagem de missões por tipo
    mission_counts = df['Mission Type'].value_counts().reset_index()
    mission_counts.columns = ['Tipo de Missão', 'Contagem']
        
    # Limitando aos 8 principais tipos para legibilidade
    top_mission_types = mission_counts.head(8)
    
    # Verificando se temos dados para mostrar
    if len(top_mission_types) > 0:
        # Gráfico de barras
        set_plot_style()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Usando apenas o barplot básico sem inversão da ordem
        sns.barplot(
            y='Tipo de Missão', 
            x='Contagem', 
            data=top_mission_types,
            palette='coolwarm'
        )
        
        plt.title('Principais Tipos de Missão Espacial', fontsize=14)
        plt.xlabel('Número de Missões')
        plt.ylabel('Tipo de Missão')
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.warning("Não foram encontrados dados para exibir o gráfico.")

def show_budget_by_mission_type(df):
    """Exibe o orçamento médio por tipo de missão"""
    st.subheader("Orçamento Médio por Tipo de Missão")
    
    # Calculando estatísticas de orçamento por tipo de missão
    budget_by_type = df.groupby('Mission Type')['Budget (in Billion $)'].agg(['mean', 'count']).reset_index()
    budget_by_type.columns = ['Tipo de Missão', 'Orçamento Médio (Bilhões $)', 'Contagem']
    
    # Ordenando por contagem para manter consistência com o gráfico anterior
    # e filtrando para tipos com pelo menos 10 missões para relevância estatística
    budget_by_type = budget_by_type[budget_by_type['Contagem'] >= 10].sort_values('Contagem', ascending=False)
    
    # Gráfico de barras
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(
        y='Tipo de Missão', 
        x='Orçamento Médio (Bilhões $)', 
        data=budget_by_type.iloc[::-1],  # Invertendo a ordem
        palette='YlOrRd'
    )
    
    plt.title('Orçamento Médio por Tipo de Missão', fontsize=14)
    plt.xlabel('Orçamento Médio (Bilhões $)')
    plt.ylabel('Tipo de Missão')
    plt.tight_layout()
    
    st.pyplot(fig)

def show_mission_types_evolution(df):
    """Exibe a evolução dos tipos de missão ao longo do tempo"""
    st.subheader("Evolução dos Tipos de Missão ao Longo do Tempo")
    
    # Agrupando dados por ano e tipo de missão
    # Selecionando apenas os 5 tipos de missão mais comuns para legibilidade
    top_types = df['Mission Type'].value_counts().nlargest(5).index.tolist()
    filtered_df = df[df['Mission Type'].isin(top_types)]
    
    mission_evolution = filtered_df.groupby(['Year', 'Mission Type']).size().reset_index(name='Contagem')
    
    # Criando o gráfico de linha
    set_plot_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.lineplot(
        x='Year', 
        y='Contagem', 
        hue='Mission Type', 
        data=mission_evolution, 
        marker='o',
        palette='Set2'
    )
    
    plt.title('Evolução dos Principais Tipos de Missão ao Longo do Tempo', fontsize=14)
    plt.xlabel('Ano')
    plt.ylabel('Número de Missões')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Tipo de Missão')
    plt.tight_layout()
    
    # Ajustando o intervalo do eixo x para melhor visualização
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    
    st.markdown("""
    **Observação**: Este gráfico mostra como a popularidade dos diferentes tipos de missão 
    evoluiu ao longo do tempo. Neste caso, temos missões tripuladas e missões não tripuladas revelando tendências e mudanças de foco na exploração espacial.
    """)