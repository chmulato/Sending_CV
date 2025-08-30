#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Streamlit para Sending_CV
===================================

Interface web para monitoramento e controle do sistema de envio de currículos.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configuração da página
st.set_page_config(
    page_title="Sending_CV Dashboard",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Carrega os dados dos arquivos Excel."""
    try:
        log_path = os.path.join('log', 'log_respostas.xlsx')
        if os.path.exists(log_path):
            df_log = pd.read_excel(log_path)
        else:
            df_log = pd.DataFrame()
            
        if os.path.exists('empresas.xlsx'):
            df_empresas = pd.read_excel('empresas.xlsx')
        else:
            df_empresas = pd.DataFrame()
            
        return df_log, df_empresas
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

def main():
    """Função principal do dashboard."""
    
    # Header
    st.title("Sending_CV Dashboard")
    st.markdown("**Sistema de Automação de Envio de Currículos**")
    st.divider()
    
    # Carrega dados
    df_log, df_empresas = load_data()
    
    # Sidebar
    st.sidebar.header("Controles")
    
    # Filtros
    if not df_log.empty:
        status_options = ['Todos'] + df_log['Status'].unique().tolist()
        status_filter = st.sidebar.selectbox("Filtrar por Status:", status_options)
        
        if status_filter != 'Todos':
            df_filtered = df_log[df_log['Status'] == status_filter]
        else:
            df_filtered = df_log
    else:
        df_filtered = df_log
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    if not df_log.empty:
        total_envios = len(df_log)
        total_respostas = len(df_log[df_log['Status'].isin(['Entrevista', 'Respondido'])])
        taxa_resposta = (total_respostas / total_envios * 100) if total_envios > 0 else 0
        followups_pendentes = len(df_log[df_log['Status'] == 'Sem Retorno'])
    else:
        total_envios = total_respostas = taxa_resposta = followups_pendentes = 0
    
    total_empresas = len(df_empresas) if not df_empresas.empty else 0
    empresas_restantes = total_empresas - total_envios
    
    with col1:
        st.metric("Total de Envios", total_envios)
    
    with col2:
        st.metric("Respostas Recebidas", total_respostas)
    
    with col3:
        st.metric("Taxa de Resposta", f"{taxa_resposta:.1f}%")
    
    with col4:
        st.metric("Follow-ups Pendentes", followups_pendentes)
    
    st.divider()
    
    # Gráficos
    if not df_log.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Status dos Envios")
            
            # Gráfico de pizza para status
            status_counts = df_log['Status'].value_counts()
            fig_pie = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Distribuição por Status"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Envios por Data")
            
            # Converter Data_Envio para datetime se necessário
            if 'Data_Envio' in df_log.columns:
                df_log['Data_Envio'] = pd.to_datetime(df_log['Data_Envio'])
                envios_por_data = df_log.groupby(df_log['Data_Envio'].dt.date).size()
                
                fig_line = px.line(
                    x=envios_por_data.index,
                    y=envios_por_data.values,
                    title="Histórico de Envios",
                    labels={'x': 'Data', 'y': 'Número de Envios'}
                )
                st.plotly_chart(fig_line, use_container_width=True)
    
    # Tabelas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Log de Respostas")
        if not df_filtered.empty:
            st.dataframe(
                df_filtered[['Empresa', 'Vaga', 'Status', 'Data_Envio', 'Observações']],
                use_container_width=True
            )
        else:
            st.info("Nenhum dado de log disponível")
    
    with col2:
        st.subheader("Empresas Pendentes")
        if not df_empresas.empty and not df_log.empty:
            empresas_contatadas = df_log['Email'].tolist()
            empresas_pendentes = df_empresas[~df_empresas['Email'].isin(empresas_contatadas)]
            
            if not empresas_pendentes.empty:
                st.dataframe(empresas_pendentes, use_container_width=True)
            else:
                st.success("Todas as empresas já foram contatadas!")
        elif not df_empresas.empty:
            st.dataframe(df_empresas, use_container_width=True)
        else:
            st.info("Nenhuma empresa cadastrada")
    
    # Ações rápidas
    st.divider()
    st.subheader("Ações Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Atualizar Dados", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("Processar Envios"):
            st.info("Funcionalidade em desenvolvimento...")
    
    with col3:
        if st.button("Verificar Follow-ups"):
            st.info("Funcionalidade em desenvolvimento...")
    
    with col4:
        if st.button("Gerar Relatório"):
            st.info("Funcionalidade em desenvolvimento...")
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <small>Sending_CV Dashboard v1.0 | Desenvolvido em Python + Streamlit</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
