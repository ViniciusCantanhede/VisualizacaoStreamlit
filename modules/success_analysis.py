import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from modules.utils import set_plot_style, create_text_area

def show_success_analysis(df):
    """Exibe análise resumida de taxas de sucesso"""
    st.markdown("<h2 class='section-header'>Análise de Taxas de Sucesso</h2>", unsafe_allow_html=True)
    
    # Espaço para explicação sobre análise de sucesso
    success_explanation = create_text_area(
        "sua explicação sobre taxas de sucesso",
        """
        Esta seção analisa as taxas de sucesso das missões espaciais, identificando fatores 
        que podem influenciar o sucesso ou fracasso. Compreender os padrões de sucesso é 
        crucial para melhorar o planejamento e execução de futuras missões.
        """
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Taxa de sucesso por país
        show_success_rate_by_country(df)
    
    with col2:
        # Taxa de sucesso por tipo de missão
        show_success_rate_by_mission_type(df)
    
    # Relação entre orçamento e taxa de sucesso
    show_budget_vs_success(df)
    
    # Evolução da taxa de sucesso ao longo do tempo
    show_success_rate_evolution(df)

def show_success_rate_by_country(df):
    """Exibe taxas de sucesso por país"""
    st.subheader("Taxa de Sucesso por País")
    
    # Calculando taxa de sucesso média por país
    success_by_country = df.groupby('Country')['Success Rate (%)'].agg(['mean', 'count']).reset_index()
    success_by_country.columns = ['País', 'Taxa de Sucesso Média (%)', 'Número de Missões']
    
    # Filtrando para países com pelo menos 10 missões
    filtered_success = success_by_country[success_by_country['Número de Missões'] >= 10]
    
    # Ordenando por taxa de sucesso
    top_countries = filtered_success.sort_values('Taxa de Sucesso Média (%)', ascending=False).head(10)
    
    # Gráfico de barras horizontais
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = sns.barplot(
        y='País', 
        x='Taxa de Sucesso Média (%)', 
        data=top_countries.iloc[::-1],  # Invertendo para melhor visualização
        palette='YlGnBu'
    )
    
    # Adicionando rótulos de porcentagem
    for i, bar in enumerate(bars.patches):
        bars.text(
            bar.get_width() + 1, 
            bar.get_y() + bar.get_height()/2, 
            f"{top_countries.iloc[::-1]['Taxa de Sucesso Média (%)'].iloc[i]:.1f}%", 
            ha='left', 
            va='center'
        )
    
    plt.title('Taxa de Sucesso Média por País (Top 10)', fontsize=14)
    plt.xlabel('Taxa de Sucesso Média (%)')
    plt.ylabel('País')
    plt.xlim(0, 100)  # Limitando o eixo x a 100%
    plt.tight_layout()
    
    st.pyplot(fig)

def show_success_rate_by_mission_type(df):
    """Exibe taxas de sucesso por tipo de missão"""
    st.subheader("Taxa de Sucesso por Tipo de Missão")
    
    # Calculando taxa de sucesso média por tipo de missão
    success_by_type = df.groupby('Mission Type')['Success Rate (%)'].agg(['mean', 'count']).reset_index()
    success_by_type.columns = ['Tipo de Missão', 'Taxa de Sucesso Média (%)', 'Número de Missões']
    
    # Filtrando para tipos com pelo menos 5 missões
    filtered_success = success_by_type[success_by_type['Número de Missões'] >= 5]
    
    # Ordenando por taxa de sucesso
    top_types = filtered_success.sort_values('Taxa de Sucesso Média (%)', ascending=False).head(10)
    
    # Gráfico de barras horizontais
    set_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = sns.barplot(
        y='Tipo de Missão', 
        x='Taxa de Sucesso Média (%)', 
        data=top_types.iloc[::-1],  # Invertendo para melhor visualização
        palette='RdPu'
    )
    
    # Adicionando rótulos de porcentagem
    for i, bar in enumerate(bars.patches):
        bars.text(
            bar.get_width() + 1, 
            bar.get_y() + bar.get_height()/2, 
            f"{top_types.iloc[::-1]['Taxa de Sucesso Média (%)'].iloc[i]:.1f}%", 
            ha='left', 
            va='center'
        )
    
    plt.title('Taxa de Sucesso Média por Tipo de Missão (Top 10)', fontsize=14)
    plt.xlabel('Taxa de Sucesso Média (%)')
    plt.ylabel('Tipo de Missão')
    plt.xlim(0, 100)  # Limitando o eixo x a 100%
    plt.tight_layout()
    
    st.pyplot(fig)

def show_budget_vs_success(df):
    """Exibe a relação entre orçamento e taxa de sucesso"""
    st.subheader("Relação entre Orçamento e Taxa de Sucesso")
    
     # Create budget ranges/bins
    bins = [0, 1, 2, 5, 10, 20, 50, 100]
    labels = ['0-1B', '1-2B', '2-5B', '5-10B', '10-20B', '20-50B', '50-100B']
    
    # Add a budget category column
    df_with_bins = df.copy()
    df_with_bins['Budget Category'] = pd.cut(df['Budget (in Billion $)'], 
                                            bins=bins, 
                                            labels=labels, 
                                            include_lowest=True)
    
    # Create the boxplot
    set_plot_style()
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Boxplot showing distribution of success rates by budget category
    sns.boxplot(x='Budget Category', 
               y='Success Rate (%)', 
               data=df_with_bins,
               palette='viridis')
    
    # Add swarmplot to show individual points (will only show if not too many points)
    if len(df) < 200:
        sns.swarmplot(x='Budget Category', 
                     y='Success Rate (%)', 
                     data=df_with_bins,
                     color='black', 
                     alpha=0.5, 
                     size=4)
    
    plt.title('Distribuição das taxas de sucesso por orçamento', fontsize=14)
    plt.xlabel('Orçamento (Bilhões $)')
    plt.ylabel('Taxa de Sucesso (%)')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    st.markdown("""
    **Observação**: O boxplot mostra a distribuição das taxas de sucesso em diferentes categorias de orçamento.
    A linha central representa a mediana, enquanto os limites da caixa representam o intervalo interquartil (IQR). Neste gráfico, percebemos que missões com orçamentos 
    mais altos nem sempre tendem a ter taxas de sucesso mais altas, embora haja uma grande variação dentro de cada categoria.
    Missões com orçamentos muito baixos podem ter taxas de sucesso variadas, indicando que o orçamento não é o único fator determinante para o sucesso.""")
    # Count number of missions in each category
    category_counts = df_with_bins['Budget Category'].value_counts().sort_index()

def show_success_rate_evolution(df):
    """Exibe a evolução da taxa de sucesso ao longo do tempo"""
    st.subheader("Evolução da Taxa de Sucesso ao Longo do Tempo")
    
    # Calculando taxa de sucesso média por ano
    success_by_year = df.groupby('Year')['Success Rate (%)'].agg(['mean', 'count']).reset_index()
    success_by_year.columns = ['Ano', 'Taxa de Sucesso Média (%)', 'Número de Missões']
    
    # Criando o gráfico
    set_plot_style()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Linha para taxa de sucesso
    color = 'tab:blue'
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Taxa de Sucesso Média (%)', color=color)
    ax1.plot(success_by_year['Ano'], success_by_year['Taxa de Sucesso Média (%)'], color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 100)  # Limitando o eixo y a 100%
    
    # Segundo eixo y para número de missões
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Número de Missões', color=color)
    ax2.bar(success_by_year['Ano'], success_by_year['Número de Missões'], alpha=0.3, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Evolução da Taxa de Sucesso e Volume de Missões ao Longo do Tempo', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)
    
    st.markdown("""
    **Observação**: Este gráfico mostra como a taxa de sucesso das missões espaciais se manteve estável ao longo do tempo,
    junto com o volume de missões realizadas em cada ano. Períodos com aumento significativo no número de missões
    muitas vezes coincidem com mudanças na taxa média de sucesso.
    """)