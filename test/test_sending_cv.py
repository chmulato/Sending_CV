#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sending_CV
==================

Script para testar o funcionamento do sistema sem enviar emails reais.
"""

import pandas as pd
import yaml
from datetime import datetime
import os
import sys

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_load_data():
    """Testa o carregamento dos dados."""
    print("=== Teste 1: Carregamento de Dados ===")
    
    try:
        # Testar empresas.xlsx
        if os.path.exists('empresas.xlsx'):
            df_empresas = pd.read_excel('empresas.xlsx')
            print(f"✅ empresas.xlsx carregado: {len(df_empresas)} empresas")
            print(f"Colunas: {list(df_empresas.columns)}")
            print(f"Primeiras 3 empresas: {df_empresas['Empresa'].head(3).tolist()}")
        else:
            print("❌ empresas.xlsx não encontrado")
            
        # Testar log_respostas.xlsx
        if os.path.exists('log_respostas.xlsx'):
            df_log = pd.read_excel('log_respostas.xlsx')
            print(f"✅ log_respostas.xlsx carregado: {len(df_log)} registros")
            print(f"Status únicos: {df_log['Status'].unique().tolist()}")
        else:
            print("❌ log_respostas.xlsx não encontrado")
            
    except Exception as e:
        print(f"❌ Erro no carregamento: {e}")

def test_config():
    """Testa o carregamento da configuração."""
    print("\n=== Teste 2: Configuração ===")
    
    try:
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        print("✅ config.yaml carregado com sucesso")
        print(f"Delay entre emails: {config['envio']['delay_entre_emails']}s")
        print(f"Max envios/dia: {config['envio']['max_envios_por_dia']}")
        print(f"Horário: {config['envio']['horario_funcionamento']['inicio']} - {config['envio']['horario_funcionamento']['fim']}")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")

def test_template():
    """Testa o template de email."""
    print("\n=== Teste 3: Template de Email ===")
    
    try:
        template_path = os.path.join('templates', 'mensagem_email.txt')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as file:
                template = file.read()
            print("✅ Template carregado com sucesso")
            print(f"Tamanho do template: {len(template)} caracteres")
            
            # Testar substituição de variáveis
            test_data = {
                'empresa': 'TechCorp',
                'vaga': 'Desenvolvedor Python',
                'seu_nome': 'João Silva'
            }
            
            template_personalizado = template
            for key, value in test_data.items():
                template_personalizado = template_personalizado.replace(f'{{{key}}}', value)
            
            print("✅ Personalização de template funcionando")
        else:
            print("❌ Template não encontrado")
            
    except Exception as e:
        print(f"❌ Erro no template: {e}")

def test_file_structure():
    """Testa a estrutura de arquivos."""
    print("\n=== Teste 4: Estrutura de Arquivos ===")
    
    required_files = [
        'main.py',
        'dashboard.py', 
        'config.yaml',
        'requirements.txt',
        'empresas.xlsx',
        'log_respostas.xlsx',
        os.path.join('templates', 'mensagem_email.txt'),
        os.path.join('test', 'test_sending_cv.py')
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - AUSENTE")

def test_dependencies():
    """Testa se as dependências estão instaladas."""
    print("\n=== Teste 5: Dependências ===")
    
    dependencies = [
        'pandas',
        'openpyxl', 
        'yagmail',
        'schedule',
        'yaml',
        'streamlit',
        'plotly'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NÃO INSTALADO")

def simulate_email_sending():
    """Simula o processo de envio de emails."""
    print("\n=== Teste 6: Simulação de Envio ===")
    
    try:
        df_empresas = pd.read_excel('empresas.xlsx')
        df_log = pd.read_excel('log_respostas.xlsx')
        
        # Encontrar empresas ainda não contatadas
        emails_enviados = df_log['Email'].tolist()
        empresas_pendentes = df_empresas[~df_empresas['Email'].isin(emails_enviados)]
        
        print(f"📊 Total de empresas: {len(df_empresas)}")
        print(f"📧 Emails já enviados: {len(emails_enviados)}")
        print(f"⏳ Empresas pendentes: {len(empresas_pendentes)}")
        
        if len(empresas_pendentes) > 0:
            print(f"📤 Próximas empresas para contato:")
            for i, row in empresas_pendentes.head(3).iterrows():
                print(f"  - {row['Empresa']} ({row['Vaga']})")
        else:
            print("✅ Todas as empresas já foram contatadas!")
            
    except Exception as e:
        print(f"❌ Erro na simulação: {e}")

def test_dashboard_data():
    """Testa os dados do dashboard."""
    print("\n=== Teste 7: Dados do Dashboard ===")
    
    try:
        df_log = pd.read_excel('log_respostas.xlsx')
        
        # Métricas
        total_envios = len(df_log)
        total_respostas = len(df_log[df_log['Status'].isin(['Entrevista', 'Respondido'])])
        taxa_resposta = (total_respostas / total_envios * 100) if total_envios > 0 else 0
        followups_pendentes = len(df_log[df_log['Status'] == 'Sem Retorno'])
        
        print(f"📧 Total de envios: {total_envios}")
        print(f"✅ Respostas recebidas: {total_respostas}")
        print(f"📊 Taxa de resposta: {taxa_resposta:.1f}%")
        print(f"⏰ Follow-ups pendentes: {followups_pendentes}")
        
        # Status distribution
        print(f"📈 Distribuição por status:")
        status_counts = df_log['Status'].value_counts()
        for status, count in status_counts.items():
            print(f"  - {status}: {count}")
            
    except Exception as e:
        print(f"❌ Erro nos dados do dashboard: {e}")

def main():
    """Executa todos os testes."""
    print("🧪 INICIANDO TESTES DO SENDING_CV")
    print("=" * 50)
    
    # Mudar para o diretório pai para acessar os arquivos
    original_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    print(f"📂 Diretório atual: {original_dir}")
    print(f"📂 Diretório do script: {script_dir}")
    print(f"📂 Diretório pai: {parent_dir}")
    
    os.chdir(parent_dir)
    
    try:
        test_file_structure()
        test_dependencies()
        test_config()
        test_load_data()
        test_template()
        simulate_email_sending()
        test_dashboard_data()
        
        print("\n" + "=" * 50)
        print("🏁 TESTES CONCLUÍDOS")
        print("\n💡 Para testar o dashboard, execute:")
        print("   streamlit run dashboard.py")
        print("\n📧 Para configurar emails reais:")
        print("   1. Edite config.yaml com suas credenciais Gmail")
        print("   2. Execute: python main.py")
        print("\n🧪 Para executar os testes novamente:")
        print("   python test/test_sending_cv.py")
        
    finally:
        # Voltar ao diretório original
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
