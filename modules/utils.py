import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def set_plot_style():
    """Define o estilo visual para os gráficos"""
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

def create_text_area(title, default_text, height=120, key=None):
    """Cria uma área de texto editável com título"""
    return st.text_area(
        f"Adicione aqui {title} (clique para editar)",
        default_text,
        height=height,
        key=key
    )

def format_large_number(num):
    """Formata grandes números para exibição mais legível"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{num:.0f}"