import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    """Carrega o conjunto de dados de exploração espacial"""
    try:
        df = pd.read_csv('data/Global_Space_Exploration_Dataset.csv')
        
        # Convertendo tipos de dados para garantir análise correta
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        
        if 'Budget (in Billion $)' in df.columns:
            df['Budget (in Billion $)'] = pd.to_numeric(df['Budget (in Billion $)'], errors='coerce')
            
        if 'Success Rate (%)' in df.columns:
            df['Success Rate (%)'] = pd.to_numeric(df['Success Rate (%)'], errors='coerce')
            
        if 'Duration (in Days)' in df.columns:
            df['Duration (in Days)'] = pd.to_numeric(df['Duration (in Days)'], errors='coerce')
        
        # Traduzindo valores da coluna Mission Type
        if 'Mission Type' in df.columns:
            # Criando um dicionário de mapeamento para tradução
            mission_type_map = {
                'Unmanned': 'Não tripulada',
                'Manned': 'Tripulada'
            }
            
            # Aplicando a tradução
            df['Mission Type'] = df['Mission Type'].replace(mission_type_map)
            
            # Verificando se existem outros valores além dos traduzidos
            unique_values = df['Mission Type'].unique()
            for value in unique_values:
                if value not in mission_type_map.values() and value not in mission_type_map.keys():
                    # Para valores que não são 'Manned' ou 'Unmanned', mantemos o original
                    pass
            
        return df
    except FileNotFoundError:
        st.error("Arquivo 'Global_Space_Exploration_Dataset.csv' não encontrado.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None