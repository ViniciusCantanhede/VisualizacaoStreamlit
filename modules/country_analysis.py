import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from modules.utils import set_plot_style, create_text_area

def show_country_analysis(df):
    """Exibe análise resumida por país"""
    st.markdown("<h2 class='section-header'>Análise por País</h2>", unsafe_allow_html=True)
    
    # Espaço para explicação sobre a análise por país
    country_explanation = create_text_area(
        "sua explicação sobre a análise por país",
        """
        Esta seção analisa a participação dos diferentes países na exploração espacial, 
        destacando os líderes em número de missões e investimentos na área. Os dados revelam
        a concentração de atividades espaciais em algumas potências principais e suas estratégias
        de investimento.
        """
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top países por número de missões
        show_top_countries_by_missions(df)
    
    with col2:
        # Top países por investimento
        show_top_countries_by_budget(df)
    
    # Relação entre número de missões e orçamento médio
    show_missions_vs_budget(df)

def show_top_countries_by_missions(df):
    """Exibe os principais países por número de missões"""
    st.subheader("Países com Maior Número de Missões Espaciais")
    
    # Contagem de missões por país
    country_missions = df['Country'].value_counts().reset_index()
    country_missions.columns = ['País', 'Número de Missões']
    top_countries = country_missions.head(10)
    
    # Gráfico de barras horizontais
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Invertendo a ordem para que o maior valor apareça no topo
    sns.barplot(
        y='País', 
        x='Número de Missões', 
        data=top_countries, #iloc[::-1] 
        palette='viridis'
    )
    
    plt.title('Top 10 Países em Número de Missões Espaciais', fontsize=14)
    plt.xlabel('Número de Missões')
    plt.ylabel('País')
    plt.tight_layout()
    
    st.pyplot(fig)

def show_top_countries_by_budget(df):
    """Exibe os principais países por orçamento"""
    st.subheader("Países com Maior Investimento em Exploração Espacial")
    
    # Calculando orçamento total e médio por país
    country_budget = df.groupby('Country')['Budget (in Billion $)'].agg(['sum', 'mean']).reset_index()
    country_budget.columns = ['País', 'Orçamento Total (Bilhões $)', 'Orçamento Médio (Bilhões $)']
    
    # Ordenando por orçamento total
    top_countries_budget = country_budget.sort_values('Orçamento Total (Bilhões $)', ascending=False).head(10)
    
    # Gráfico de barras horizontais
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Invertendo a ordem para que o maior valor apareça no topo
    sns.barplot(
        y='País', 
        x='Orçamento Total (Bilhões $)', 
        data=top_countries_budget,  #iloc[::-1] 
        palette='magma'
    )
    
    plt.title('Top 10 Países em Investimento em Missões Espaciais', fontsize=14)
    plt.xlabel('Orçamento Total (Bilhões $)')
    plt.ylabel('País')
    plt.tight_layout()
    
    st.pyplot(fig)

def show_missions_vs_budget(df):
    """Exibe a relação entre número de missões e orçamento médio"""
    st.subheader("Relação entre Número de Missões e Orçamento Médio por País")
    
    # Preparando os dados agregados
    country_data = df.groupby('Country').agg({
        'Mission Name': 'count',
        'Budget (in Billion $)': 'mean'
    }).reset_index()
    
    country_data.columns = ['País', 'Número de Missões', 'Orçamento Médio (Bilhões $)']
    
    # Filtrando para mostrar apenas países com pelo menos 10 missões (para legibilidade)
    filtered_data = country_data[country_data['Número de Missões'] >= 10].sort_values('Número de Missões', ascending=False)
    
    # Gráfico de dispersão
    set_plot_style()
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter = sns.scatterplot(
        x='Número de Missões', 
        y='Orçamento Médio (Bilhões $)',
        data=filtered_data,
        size='Número de Missões',
        sizes=(100, 700),
        alpha=0.7,
        palette='viridis',
        hue='País'
    )
    
    # Adicionando rótulos para os pontos
    for i, row in filtered_data.iterrows():
        plt.text(
            row['Número de Missões'] + 1, 
            row['Orçamento Médio (Bilhões $)'], 
            row['País'],
            fontsize=9
        )
    
    plt.title('Relação entre Volume de Missões e Orçamento Médio por País', fontsize=14)
    plt.xlabel('Número de Missões')
    plt.ylabel('Orçamento Médio por Missão (Bilhões $)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Removendo a legenda já que os pontos estão rotulados
    plt.legend([],[], frameon=False)
    
    st.pyplot(fig)
    
    st.markdown("""
    **Observação**: Este gráfico mostra a relação entre o volume de missões e o orçamento médio por missão.
    Países no quadrante superior direito têm muitas missões com alto orçamento, enquanto países no quadrante inferior direito 
    têm muitas missões com orçamento menor por missão.
    """)