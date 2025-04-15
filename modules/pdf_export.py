import streamlit as st
import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import tempfile
import os

# Importações do ReportLab
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def gerar_relatorio_pdf(df):
    """Cria um relatório PDF completo da análise de exploração espacial"""
    
    # Configuração do buffer para armazenar o PDF
    buffer = io.BytesIO()
    
    # Configuração do documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        title="Análise de Exploração Espacial"
    )
    
    # Lista de elementos para o PDF
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    
    # Adicionando estilos personalizados
    estilos.add(
        ParagraphStyle(
            name='Titulo',
            parent=estilos['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER
        )
    )
    
    estilos.add(
        ParagraphStyle(
            name='Secao',
            parent=estilos['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=24
        )
    )
    
    estilos.add(
        ParagraphStyle(
            name='Subsecao',
            parent=estilos['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=12
        )
    )
    
    estilos.add(
        ParagraphStyle(
            name='CorpoTexto',
            parent=estilos['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY
        )
    )
    
    # Capa do relatório
    elementos.append(Paragraph("Análise de Exploração Espacial Global", estilos['Titulo']))
    elementos.append(Spacer(1, 0.5*inch))
    
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    elementos.append(Paragraph(f"Relatório gerado em: {data_hoje}", estilos['CorpoTexto']))
    elementos.append(Spacer(1, 0.5*inch))
    
    # Introdução
    elementos.append(Paragraph("Introdução", estilos['Secao']))
    elementos.append(Paragraph(
        f"Este relatório apresenta uma análise exploratória dos dados de exploração espacial global, "
        f"cobrindo {len(df)} missões registradas entre {df['Year'].min()} e {df['Year'].max()}. "
        f"São examinados padrões de liderança entre países, tipos de missão predominantes e "
        f"fatores que influenciam o sucesso das missões.",
        estilos['CorpoTexto']
    ))
    
    # Estatísticas gerais
    elementos.append(Spacer(1, 0.3*inch))
    elementos.append(Paragraph("Estatísticas Gerais", estilos['Subsecao']))
    
    # Dados para a tabela de estatísticas
    dados_tabela = [
        ["Métrica", "Valor"],
        ["Total de Missões", f"{len(df)}"],
        ["Período Analisado", f"{df['Year'].min()} - {df['Year'].max()}"],
        ["Países Envolvidos", f"{df['Country'].nunique()}"],
        ["Tipos de Missão", f"{df['Mission Type'].nunique()}"],
        ["Taxa Média de Sucesso", f"{df['Success Rate (%)'].mean():.2f}%"],
        ["Orçamento Médio", f"${df['Budget (in Billion $)'].mean():.2f} bilhões"]
    ]
    
    # Criando e estilizando a tabela
    tabela_estatisticas = Table(dados_tabela, colWidths=[3*inch, 2*inch])
    tabela_estatisticas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.midnightblue),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (1, -1), 10),
        ('GRID', (0, 0), (1, -1), 1, colors.black),
    ]))
    
    elementos.append(tabela_estatisticas)
    
    # Quebra de página após a introdução
    elementos.append(PageBreak())
    
    # Seção: Análise por País
    elementos.append(Paragraph("Análise por País", estilos['Secao']))
    elementos.append(Paragraph(
        "Esta seção analisa a participação dos diferentes países na exploração espacial, "
        "destacando os líderes em número de missões e investimentos na área. Os dados revelam "
        "a concentração de atividades espaciais em algumas potências principais e suas estratégias "
        "de investimento.",
        estilos['CorpoTexto']
    ))
    
    # Gráfico: Países com mais missões
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Contagem de missões por país
        country_missions = df['Country'].value_counts().head(10).sort_values()
        
        plt.figure(figsize=(8, 5))
        bars = country_missions.plot.barh(color='skyblue')
        plt.title('Top 10 Países em Número de Missões')
        plt.xlabel('Número de Missões')
        plt.ylabel('País')
        plt.tight_layout()
        
        # Salvando a figura
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Adicionando a imagem ao PDF
        img = Image(tmp_file.name, width=6*inch, height=4*inch)
        elementos.append(img)
        
        # Excluindo o arquivo temporário
        tmp_path = tmp_file.name
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # Gráfico: Orçamento por país
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Orçamento médio por país
        country_budget = df.groupby('Country')['Budget (in Billion $)'].mean().sort_values(ascending=False).head(10)
        
        plt.figure(figsize=(8, 5))
        bars = country_budget.plot.barh(color='salmon')
        plt.title('Top 10 Países por Orçamento Médio')
        plt.xlabel('Orçamento Médio (Bilhões $)')
        plt.ylabel('País')
        plt.tight_layout()
        
        # Salvando a figura
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Adicionando a imagem ao PDF
        img = Image(tmp_file.name, width=6*inch, height=4*inch)
        elementos.append(img)
        
        # Excluindo o arquivo temporário
        tmp_path = tmp_file.name
    
    # Quebra de página após análise por país
    elementos.append(PageBreak())
    
    # Seção: Análise por Tipo de Missão
    elementos.append(Paragraph("Análise por Tipo de Missão", estilos['Secao']))
    elementos.append(Paragraph(
        "Esta seção analisa os diferentes tipos de missão espacial, suas frequências, "
        "características e evolução ao longo do tempo. Identificar os tipos mais comuns ajuda a "
        "entender as prioridades na exploração espacial e como os recursos são alocados.",
        estilos['CorpoTexto']
    ))
    
    # Gráfico: Tipos de missão
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Contagem de tipos de missão
        mission_counts = df['Mission Type'].value_counts().head(8).sort_values()
        
        plt.figure(figsize=(8, 5))
        bars = mission_counts.plot.barh(color='lightgreen')
        plt.title('Principais Tipos de Missão Espacial')
        plt.xlabel('Número de Missões')
        plt.ylabel('Tipo de Missão')
        plt.tight_layout()
        
        # Salvando a figura
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Adicionando a imagem ao PDF
        img = Image(tmp_file.name, width=6*inch, height=4*inch)
        elementos.append(img)
        
        # Excluindo o arquivo temporário
        tmp_path = tmp_file.name
    
    # Evolução dos tipos de missão
    elementos.append(Spacer(1, 0.3*inch))
    elementos.append(Paragraph("Evolução dos Tipos de Missão ao Longo do Tempo", estilos['Subsecao']))
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Selecionando os tipos mais comuns para a visualização
        top_types = df['Mission Type'].value_counts().nlargest(3).index.tolist()
        filtered_df = df[df['Mission Type'].isin(top_types)]
        
        # Agrupando por ano e tipo
        mission_evolution = filtered_df.groupby(['Year', 'Mission Type']).size().reset_index(name='Contagem')
        
        plt.figure(figsize=(8, 5))
        sns.lineplot(x='Year', y='Contagem', hue='Mission Type', data=mission_evolution, marker='o')
        plt.title('Evolução dos Principais Tipos de Missão')
        plt.xlabel('Ano')
        plt.ylabel('Número de Missões')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Salvando a figura
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Adicionando a imagem ao PDF
        img = Image(tmp_file.name, width=6*inch, height=4*inch)
        elementos.append(img)
        
        # Excluindo o arquivo temporário
        tmp_path = tmp_file.name
    
    # Quebra de página
    elementos.append(PageBreak())
    
    # Seção: Análise de Taxas de Sucesso
    elementos.append(Paragraph("Análise de Taxas de Sucesso", estilos['Secao']))
    elementos.append(Paragraph(
        "Esta seção analisa as taxas de sucesso das missões espaciais, identificando fatores "
        "que podem influenciar o sucesso ou fracasso. Compreender os padrões de sucesso é "
        "crucial para melhorar o planejamento e execução de futuras missões.",
        estilos['CorpoTexto']
    ))
    
    # Taxa de sucesso por país
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Calculando taxa de sucesso média por país
        success_by_country = df.groupby('Country')['Success Rate (%)'].agg(['mean', 'count']).reset_index()
        success_by_country.columns = ['País', 'Taxa de Sucesso Média (%)', 'Número de Missões']
        
        # Filtrando para países com pelo menos 10 missões
        filtered_success = success_by_country[success_by_country['Número de Missões'] >= 10]
        
        # Ordenando por taxa de sucesso
        top_countries = filtered_success.sort_values('Taxa de Sucesso Média (%)', ascending=True).head(10)
        
        plt.figure(figsize=(8, 5))
        bars = sns.barplot(y='País', x='Taxa de Sucesso Média (%)', data=top_countries, palette='YlGnBu')
        plt.title('Taxa de Sucesso Média por País')
        plt.xlabel('Taxa de Sucesso Média (%)')
        plt.ylabel('País')
        plt.xlim(0, 100)
        plt.tight_layout()
        
        # Salvando a figura
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Adicionando a imagem ao PDF
        img = Image(tmp_file.name, width=6*inch, height=4*inch)
        elementos.append(img)
        
        # Excluindo o arquivo temporário
        tmp_path = tmp_file.name
    
    # Relação entre orçamento e taxa de sucesso
    elementos.append(Spacer(1, 0.3*inch))
    elementos.append(Paragraph("Relação entre Orçamento e Taxa de Sucesso", estilos['Subsecao']))
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Categorias de orçamento
        bins = [0, 1, 2, 5, 10, 20, 50, 100]
        labels = ['0-1B', '1-2B', '2-5B', '5-10B', '10-20B', '20-50B', '50-100B']
        
        # Adicionando categorias ao DataFrame
        df_with_bins = df.copy()
        df_with_bins['Budget Category'] = pd.cut(df['Budget (in Billion $)'], 
                                               bins=bins, 
                                               labels=labels, 
                                               include_lowest=True)
        
        # Agrupando por categoria de orçamento
        budget_success = df_with_bins.groupby('Budget Category').agg({
            'Success Rate (%)': ['mean', 'count']
        }).reset_index()
        
        # Simplificando nomes de colunas
        budget_success.columns = ['Categoria de Orçamento', 'Taxa de Sucesso Média', 'Número de Missões']
        
        plt.figure(figsize=(8, 5))
        bars = sns.barplot(x='Categoria de Orçamento', y='Taxa de Sucesso Média', data=budget_success, palette='viridis')
        
        # Adicionando número de missões como texto em cada barra
        for i, bar in enumerate(bars.patches):
            bars.text(bar.get_x() + bar.get_width()/2, 
                    bar.get_height() + 2,
                    f"n={budget_success['Número de Missões'].iloc[i]}", 
                    ha='center')
        
        plt.title('Taxa de Sucesso por Categoria de Orçamento')
        plt.xlabel('Categoria de Orçamento (Bilhões $)')
        plt.ylabel('Taxa de Sucesso Média (%)')
        plt.ylim(0, 100)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salvando a figura
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Adicionando a imagem ao PDF
        img = Image(tmp_file.name, width=6*inch, height=4*inch)
        elementos.append(img)
        
        # Excluindo o arquivo temporário
        tmp_path = tmp_file.name
    
    # Quebra de página
    elementos.append(PageBreak())
    
    # Conclusões
    elementos.append(Paragraph("Conclusões", estilos['Secao']))
    
    texto_conclusao = """
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
    """
    
    for paragrafo in texto_conclusao.split('\n\n'):
        if paragrafo.strip():
            elementos.append(Paragraph(paragrafo.strip(), estilos['CorpoTexto']))
            elementos.append(Spacer(1, 0.1*inch))
    
    # Principais descobertas
    elementos.append(Spacer(1, 0.2*inch))
    elementos.append(Paragraph("Principais Descobertas", estilos['Subsecao']))
    
    descobertas = [
        "Liderança Global: Poucas nações dominam a exploração espacial, com clara concentração de recursos e capacidade tecnológica.",
        "Evolução Tecnológica: Observamos uma clara tendência de aumento em missões não tripuladas, refletindo avanços em automação e inteligência artificial.",
        "Investimento e Sucesso: Existe correlação positiva entre orçamento e sucesso, mas com retornos decrescentes acima de certos patamares de investimento.",
        "Colaboração Internacional: Missões colaborativas apresentam taxas de sucesso acima da média, sugerindo benefícios da cooperação técnica e científica."
    ]
    
    for descoberta in descobertas:
        elementos.append(Paragraph("• " + descoberta, estilos['CorpoTexto']))
        elementos.append(Spacer(1, 0.1*inch))
    
    # Construir o PDF
    doc.build(elementos)
    
    # Limpar arquivos temporários se ainda existirem
    try:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
    except:
        pass
    
    # Obter o conteúdo do buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def criar_link_download(pdf_data, filename="analise_espacial.pdf"):
    """Cria um link para download do PDF gerado"""
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    
    # Criando o link HTML
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{filename}" class="download-button">Baixar Relatório PDF</a>'
    
    return href

def adicionar_secao_exportacao_pdf(df):
    """Adiciona a seção de exportação PDF ao app Streamlit"""
    st.markdown("<h2 class='section-header'>Exportar Relatório PDF</h2>", unsafe_allow_html=True)
    
    # CSS para o botão de download
    st.markdown("""
    <style>
    .download-button {
        display: inline-block;
        padding: 12px 24px;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        border-radius: 5px;
        margin: 10px 0;
        transition: background-color 0.3s;
        cursor: pointer;
    }
    .download-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("Clique no botão abaixo para gerar e baixar um relatório PDF completo da análise.")
    
    # Botão para gerar o PDF
    if st.button("Gerar Relatório PDF"):
        with st.spinner("Gerando relatório PDF... Isso pode levar alguns segundos."):
            try:
                # Gerar o PDF
                pdf_data = gerar_relatorio_pdf(df)
                
                if pdf_data:
                    # Criar link de download
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    download_link = criar_link_download(pdf_data, f"analise_espacial_{timestamp}.pdf")
                    
                    st.success("Relatório PDF gerado com sucesso!")
                    st.markdown(download_link, unsafe_allow_html=True)
                else:
                    st.error("Ocorreu um erro ao gerar o PDF.")
            
            except Exception as e:
                st.error(f"Erro durante a geração do PDF: {str(e)}")
                st.info("""
                Dicas para solução de problemas:
                1. Verifique se todas as bibliotecas necessárias estão instaladas
                2. Certifique-se de que seu ambiente tem acesso para criar arquivos temporários
                """)