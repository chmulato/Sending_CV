#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Completo do Sistema Sending_CV
====================================

Script abrangente para testar todas as funcionalidades do sistema:
- Carregamento de dados        dependencies = [
            'pandas',
            'streamlit',
            'yagmail',
            'pdfplumber',
            ('docx', 'python-docx'),
            ('yaml', 'PyYAML'),
            'plotly',
            'nltk'
        ]

        for dep in dependencies:
            try:
                if isinstance(dep, tuple):
                    # Para dependências que podem ter nomes diferentes
                    module_name, package_name = dep
                    __import__(module_name)
                    self.log_result("Dependência", "PASS", f"{package_name} importado com sucesso")
                else:
                    __import__(dep)
                    self.log_result("Dependência", "PASS", f"{dep} importado com sucesso")
            except ImportError:
                if isinstance(dep, tuple):
                    self.log_result("Dependência", "FAIL", f"{dep[1]} não encontrado")
                else:
                    self.log_result("Dependência", "FAIL", f"{dep} não encontrado")
            except Exception as e:
                if isinstance(dep, tuple):
                    self.log_result("Dependência", "WARN", f"{dep[1]} erro ao importar: {e}")
                else:
                    self.log_result("Dependência", "WARN", f"{dep} erro ao importar: {e}") Estrutura de arquivos
- Conversão de documentos (PDF, DOCX)
- Funcionalidades ATS
- Conectividade de email
- Dashboard
- Dependências

Uso: python test/test_complete.py
"""

import os
import sys
import pandas as pd
import yaml
from datetime import datetime
import pdfplumber
import subprocess
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SendingCVTester:
    """Classe para testar todas as funcionalidades do Sending_CV."""

    def __init__(self):
        self.results = []
        self.errors = []

    def log_result(self, test_name, status, message=""):
        """Registra resultado de um teste."""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        self.results.append(result)

        status_icon = "[PASS]" if status == "PASS" else "[FAIL]" if status == "FAIL" else "[WARN]"
        print(f"{status_icon} {test_name}: {message}")

        if status == "FAIL":
            self.errors.append(result)

    def test_project_structure(self):
        """Testa a estrutura básica do projeto."""
        print("\n[ESTRUTURA] Testando Estrutura do Projeto")
        print("=" * 40)

        # Arquivos essenciais
        required_files = [
            'main.py',
            'config.yaml',
            'requirements.txt',
            'empresas.xlsx',
            'README.md'
        ]

        for file in required_files:
            if os.path.exists(file):
                self.log_result("Arquivo essencial", "PASS", f"{file} encontrado")
            else:
                self.log_result("Arquivo essencial", "FAIL", f"{file} não encontrado")

        # Pastas essenciais
        required_dirs = ['core', 'curriculos', 'log', 'templates', 'test', 'img']
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                self.log_result("Pasta essencial", "PASS", f"pasta {dir_name}/ encontrada")
            else:
                self.log_result("Pasta essencial", "FAIL", f"pasta {dir_name}/ não encontrada")

    def test_configurations(self):
        """Testa carregamento das configurações."""
        print("\n[CONFIG] Testando Configuracoes")
        print("=" * 40)

        # Testar config.yaml
        try:
            if os.path.exists('config.yaml'):
                with open('config.yaml', 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)

                # Verificar seções obrigatórias
                required_sections = ['email', 'envio']
                for section in required_sections:
                    if section in config:
                        self.log_result("Configuração", "PASS", f"seção {section} encontrada")
                    else:
                        self.log_result("Configuração", "FAIL", f"seção {section} não encontrada")

                # Verificar configurações de email
                if 'email' in config:
                    email_config = config['email']
                    required_email_keys = ['usuario', 'senha_app', 'servidor_smtp', 'porta']
                    for key in required_email_keys:
                        if key in email_config and email_config[key]:
                            self.log_result("Configuração email", "PASS", f"{key} configurado")
                        else:
                            self.log_result("Configuração email", "WARN", f"{key} não configurado")

                self.log_result("Arquivo de configuração", "PASS", "config.yaml carregado com sucesso")
            else:
                self.log_result("Arquivo de configuração", "FAIL", "config.yaml não encontrado")

        except Exception as e:
            self.log_result("Arquivo de configuração", "FAIL", f"erro ao carregar config.yaml: {e}")

    def test_data_files(self):
        """Testa arquivos de dados."""
        print("\n[DADOS] Testando Arquivos de Dados")
        print("=" * 40)

        # Testar empresas.xlsx
        try:
            if os.path.exists('empresas.xlsx'):
                df = pd.read_excel('empresas.xlsx')
                self.log_result("Arquivo empresas.xlsx", "PASS", f"{len(df)} empresas carregadas")

                # Verificar colunas obrigatórias
                required_cols = ['Empresa', 'Vaga', 'Email']
                for col in required_cols:
                    if col in df.columns:
                        self.log_result("Coluna empresas.xlsx", "PASS", f"coluna {col} encontrada")
                    else:
                        self.log_result("Coluna empresas.xlsx", "FAIL", f"coluna {col} não encontrada")
            else:
                self.log_result("Arquivo empresas.xlsx", "FAIL", "arquivo não encontrado")

        except Exception as e:
            self.log_result("Arquivo empresas.xlsx", "FAIL", f"erro ao carregar: {e}")

        # Testar template de email
        try:
            template_path = os.path.join('templates', 'mensagem_email.txt')
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template = f.read()
                self.log_result("Template de email", "PASS", f"{len(template)} caracteres carregados")

                # Verificar variáveis no template
                template_vars = ['{empresa}', '{vaga}', '{seu_nome}', '{seu_contato}']
                found_vars = 0
                for var in template_vars:
                    if var in template:
                        found_vars += 1
                        self.log_result("Variável template", "PASS", f"variável {var} encontrada")
                    else:
                        self.log_result("Variável template", "WARN", f"variável {var} não encontrada")

                if found_vars >= 2:
                    self.log_result("Template completo", "PASS", f"{found_vars}/{len(template_vars)} variáveis encontradas")
                else:
                    self.log_result("Template completo", "WARN", f"apenas {found_vars}/{len(template_vars)} variáveis encontradas")
            else:
                self.log_result("Template de email", "FAIL", "arquivo não encontrado")

        except Exception as e:
            self.log_result("Template de email", "FAIL", f"erro ao carregar: {e}")

    def test_document_conversion(self):
        """Testa conversão de documentos."""
        print("\n[DOCUMENTOS] Testando Conversao de Documentos")
        print("=" * 40)

        # Testar PDF
        curriculos_dir = 'curriculos'
        if os.path.exists(curriculos_dir):
            pdf_files = [f for f in os.listdir(curriculos_dir) if f.endswith('.pdf')]

            if pdf_files:
                for pdf_file in pdf_files[:1]:  # Testar apenas o primeiro
                    pdf_path = os.path.join(curriculos_dir, pdf_file)
                    try:
                        with pdfplumber.open(pdf_path) as pdf:
                            text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text

                            if text.strip():
                                self.log_result("Conversão PDF", "PASS", f"{pdf_file}: {len(text)} caracteres extraídos")
                            else:
                                self.log_result("Conversão PDF", "WARN", f"{pdf_file}: texto vazio extraído")
                    except Exception as e:
                        self.log_result("Conversão PDF", "FAIL", f"{pdf_file}: erro - {e}")
            else:
                self.log_result("Conversão PDF", "WARN", "nenhum arquivo PDF encontrado em curriculos/")
        else:
            self.log_result("Conversão PDF", "FAIL", "pasta curriculos/ não encontrada")

        # Testar DOCX
        docx_files = [f for f in os.listdir(curriculos_dir) if f.endswith('.docx')] if os.path.exists(curriculos_dir) else []

        if docx_files:
            for docx_file in docx_files[:1]:  # Testar apenas o primeiro
                docx_path = os.path.join(curriculos_dir, docx_file)
                try:
                    from docx import Document
                    doc = Document(docx_path)
                    text = ""
                    for paragraph in doc.paragraphs:
                        text += paragraph.text + "\n"

                    if text.strip():
                        self.log_result("Conversão DOCX", "PASS", f"{docx_file}: {len(text)} caracteres extraídos")
                    else:
                        self.log_result("Conversão DOCX", "WARN", f"{docx_file}: texto vazio extraído")
                except ImportError:
                    self.log_result("Conversão DOCX", "WARN", "python-docx não instalado")
                except Exception as e:
                    self.log_result("Conversão DOCX", "FAIL", f"{docx_file}: erro - {e}")
        else:
            self.log_result("Conversão DOCX", "WARN", "nenhum arquivo DOCX encontrado")

    def test_dependencies(self):
        """Testa dependências Python."""
        print("\n[DEPENDENCIAS] Testando Dependencias Python")
        print("=" * 40)

        dependencies = [
            'pandas',
            'streamlit',
            'yagmail',
            'pdfplumber',
            'python-docx',
            'PyYAML',
            'plotly',
            'nltk'
        ]

        for dep in dependencies:
            try:
                __import__(dep.replace('-', '_'))
                self.log_result("Dependência", "PASS", f"{dep} importado com sucesso")
            except ImportError:
                self.log_result("Dependência", "FAIL", f"{dep} não encontrado")
            except Exception as e:
                self.log_result("Dependência", "WARN", f"{dep} erro ao importar: {e}")

    def test_core_modules(self):
        """Testa módulos principais."""
        print("\n[MODULOS] Testando Modulos Principais")
        print("=" * 40)

        core_modules = [
            'core.ats_analyzer',
            'core.ats_email_integration',
            'core.ats_organizer',
            'core.dashboard'
        ]

        for module in core_modules:
            try:
                __import__(module)
                self.log_result("Módulo core", "PASS", f"{module} importado com sucesso")
            except ImportError as e:
                self.log_result("Módulo core", "FAIL", f"{module} erro ao importar: {e}")
            except Exception as e:
                self.log_result("Módulo core", "WARN", f"{module} erro: {e}")

    def test_main_execution(self):
        """Testa execução básica do main.py."""
        print("\n[EXECUCAO] Testando Execucao Principal")
        print("=" * 40)

        try:
            # Importar main.py
            import main
            self.log_result("Execução principal", "PASS", "main.py importado com sucesso")

            # Verificar se há classes ou funções principais
            main_classes = ['SendingCV', 'ATSOrganizer', 'ATSEmailIntegration']
            found_classes = []

            for class_name in main_classes:
                if hasattr(main, class_name):
                    found_classes.append(class_name)

            if found_classes:
                self.log_result("Classe principal", "PASS", f"Classes encontradas: {', '.join(found_classes)}")
            else:
                # Verificar funções principais
                main_functions = ['main', 'analisar_curriculos', 'enviar_emails']
                found_functions = []

                for func_name in main_functions:
                    if hasattr(main, func_name):
                        found_functions.append(func_name)

                if found_functions:
                    self.log_result("Função principal", "PASS", f"Funções encontradas: {', '.join(found_functions)}")
                else:
                    self.log_result("Estrutura principal", "WARN", "nenhuma classe ou função principal encontrada")

        except ImportError as e:
            self.log_result("Execução principal", "FAIL", f"erro ao importar main.py: {e}")
        except Exception as e:
            self.log_result("Execução principal", "WARN", f"erro inesperado: {e}")

    def test_email_connectivity(self):
        """Testa conectividade de email (sem enviar emails reais)."""
        print("\n[EMAIL] Testando Conectividade de Email")
        print("=" * 40)

        try:
            # Verificar configurações de email
            if not os.path.exists('config.yaml'):
                self.log_result("Conectividade email", "FAIL", "config.yaml não encontrado")
                return

            with open('config.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            email_config = config.get('email', {})

            # Verificar campos obrigatórios
            required_fields = ['usuario', 'senha_app', 'servidor_smtp', 'porta']
            missing_fields = []

            for field in required_fields:
                if not email_config.get(field):
                    missing_fields.append(field)

            if missing_fields:
                self.log_result("Configuração email", "FAIL", f"campos obrigatórios não configurados: {', '.join(missing_fields)}")
                return

            # Testar importação do yagmail
            try:
                import yagmail
                self.log_result("Importação yagmail", "PASS", "yagmail importado com sucesso")
            except ImportError:
                self.log_result("Importação yagmail", "FAIL", "yagmail não instalado")
                return

            # Testar conexão SMTP (sem enviar email)
            try:
                # Criar conexão SMTP com configurações SSL/TLS adequadas para Gmail
                yag = yagmail.SMTP(
                    email_config['usuario'],
                    email_config['senha_app'],
                    host=email_config['servidor_smtp'],
                    port=email_config['porta'],
                    smtp_ssl=False,  # Não usar SSL direto
                    smtp_starttls=True,  # Usar STARTTLS
                    smtp_skip_login=False
                )

                # Testar conexão
                yag.connection  # Acessar propriedade para verificar conexão

                self.log_result("Conexão SMTP", "PASS", f"conectado ao {email_config['servidor_smtp']}:{email_config['porta']}")

                # Fechar conexão
                yag.close()

            except Exception as e:
                self.log_result("Conexão SMTP", "FAIL", f"falha na conexão: {str(e)}")

            # Verificar template de email
            try:
                template_path = os.path.join('templates', 'mensagem_email.txt')
                if os.path.exists(template_path):
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template = f.read()

                    if len(template.strip()) > 0:
                        self.log_result("Template de email", "PASS", f"template válido ({len(template)} caracteres)")
                    else:
                        self.log_result("Template de email", "WARN", "template vazio")
                else:
                    self.log_result("Template de email", "FAIL", "arquivo não encontrado")
            except Exception as e:
                self.log_result("Template de email", "FAIL", f"erro ao carregar: {e}")

            # Verificar empresas.xlsx para emails
            try:
                if os.path.exists('empresas.xlsx'):
                    df = pd.read_excel('empresas.xlsx')

                    if 'Email' in df.columns:
                        valid_emails = df['Email'].dropna()
                        if len(valid_emails) > 0:
                            self.log_result("Lista de emails", "PASS", f"{len(valid_emails)} emails válidos encontrados")
                        else:
                            self.log_result("Lista de emails", "WARN", "nenhum email encontrado")
                    else:
                        self.log_result("Lista de emails", "FAIL", "coluna 'Email' não encontrada")
                else:
                    self.log_result("Lista de emails", "FAIL", "empresas.xlsx não encontrado")
            except Exception as e:
                self.log_result("Lista de emails", "FAIL", f"erro ao carregar: {e}")

        except Exception as e:
            self.log_result("Teste de email", "FAIL", f"erro geral: {e}")

    def test_email_simulation(self):
        """Simula envio de email sem realmente enviar."""
        print("\n[EMAIL-SIM] Testando Simulacao de Envio de Email")
        print("=" * 40)

        try:
            # Verificar se temos dados suficientes para simulação
            if not os.path.exists('empresas.xlsx'):
                self.log_result("Simulação email", "FAIL", "empresas.xlsx não encontrado")
                return

            df = pd.read_excel('empresas.xlsx')

            if len(df) == 0:
                self.log_result("Simulação email", "FAIL", "nenhuma empresa cadastrada")
                return

            # Verificar template
            template_path = os.path.join('templates', 'mensagem_email.txt')
            if not os.path.exists(template_path):
                self.log_result("Simulação email", "FAIL", "template de email não encontrado")
                return

            # Simular processamento de uma empresa
            empresa_teste = df.iloc[0]  # Primeira empresa
            empresa_nome = empresa_teste['Empresa']
            empresa_email = empresa_teste['Email']
            vaga_nome = empresa_teste['Vaga']

            # Carregar template
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            # Simular personalização
            mensagem_personalizada = template.replace('{empresa}', empresa_nome)
            mensagem_personalizada = mensagem_personalizada.replace('{vaga}', vaga_nome)

            # Verificar se personalização funcionou
            if '{empresa}' not in mensagem_personalizada and '{vaga}' not in mensagem_personalizada:
                self.log_result("Personalização email", "PASS", "template personalizado com sucesso")
            else:
                self.log_result("Personalização email", "WARN", "algumas variáveis não foram substituídas")

            # Simular validação de email
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, str(empresa_email)):
                self.log_result("Validação email", "PASS", f"email válido: {empresa_email}")
            else:
                self.log_result("Validação email", "FAIL", f"email inválido: {empresa_email}")

            # Simular verificação de horário
            from datetime import datetime
            now = datetime.now()
            current_hour = now.hour

            if 9 <= current_hour <= 17:
                self.log_result("Horário comercial", "PASS", f"horário válido: {current_hour}h")
            else:
                self.log_result("Horário comercial", "WARN", f"fora do horário comercial: {current_hour}h")

            self.log_result("Simulação email", "PASS", "simulação concluída com sucesso")

        except Exception as e:
            self.log_result("Simulação email", "FAIL", f"erro na simulação: {e}")

    def test_email_simulation_chmulato(self):
        """Simula envio específico para chmulato@hotmail.com."""
        print("\n[EMAIL-CHMULATO] Simulação de Envio para chmulato@hotmail.com")
        print("=" * 50)

        try:
            # Destinatário específico
            destinatario = "chmulato@hotmail.com"
            empresa_nome = "Empresa Teste"
            vaga_nome = "Desenvolvedor Python"

            print(f"📧 Destinatário: {destinatario}")
            print(f"🏢 Empresa: {empresa_nome}")
            print(f"💼 Vaga: {vaga_nome}")
            print()

            # Verificar template
            template_path = os.path.join('templates', 'mensagem_email.txt')
            if not os.path.exists(template_path):
                self.log_result("Simulação chmulato", "FAIL", "template de email não encontrado")
                return

            # Carregar template
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            print("📝 TEMPLATE ORIGINAL:")
            print("-" * 30)
            print(template[:200] + "..." if len(template) > 200 else template)
            print()

            # Simular personalização
            mensagem_personalizada = template.replace('{empresa}', empresa_nome)
            mensagem_personalizada = mensagem_personalizada.replace('{vaga}', vaga_nome)

            # Substituir outras variáveis se existirem
            mensagem_personalizada = mensagem_personalizada.replace('{seu_nome}', 'Seu Nome')
            mensagem_personalizada = mensagem_personalizada.replace('{seu_contato}', 'seu.email@exemplo.com')

            print("✨ MENSAGEM PERSONALIZADA:")
            print("-" * 30)
            print(mensagem_personalizada[:300] + "..." if len(mensagem_personalizada) > 300 else mensagem_personalizada)
            print()

            # Simular validação de email
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, destinatario):
                self.log_result("Validação email chmulato", "PASS", f"email válido: {destinatario}")
            else:
                self.log_result("Validação email chmulato", "FAIL", f"email inválido: {destinatario}")
                return

            # Simular verificação de horário comercial
            from datetime import datetime
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute
            current_time = current_hour * 60 + current_minute

            # Carregar configuração de horário
            config = {}
            try:
                with open('config.yaml', 'r', encoding='utf-8') as f:
                    import yaml
                    config = yaml.safe_load(f)
            except:
                pass

            horario_config = config.get('envio', {}).get('horario_funcionamento', {})
            start_hour = horario_config.get('inicio', '09:00').split(':')[0]
            start_minute = horario_config.get('inicio', '09:00').split(':')[1]
            end_hour = horario_config.get('fim', '17:00').split(':')[0]
            end_minute = horario_config.get('fim', '17:00').split(':')[1]

            start_time = int(start_hour) * 60 + int(start_minute)
            end_time = int(end_hour) * 60 + int(end_minute)

            if start_time <= current_time <= end_time:
                self.log_result("Horário comercial chmulato", "PASS", f"horário válido: {current_hour:02d}:{current_minute:02d}")
            else:
                self.log_result("Horário comercial chmulato", "WARN", f"fora do horário: {current_hour:02d}:{current_minute:02d} (permitido: {start_hour}:{start_minute}-{end_hour}:{end_minute})")

            # Simular anexo de currículo
            curriculo_path = os.path.join('curriculos', 'currículo.pdf')
            if os.path.exists(curriculo_path):
                file_size = os.path.getsize(curriculo_path)
                self.log_result("Anexo currículo", "PASS", f"currículos/currículo.pdf ({file_size} bytes) pronto para anexar")
            else:
                self.log_result("Anexo currículo", "FAIL", "currículos/currículo.pdf não encontrado")

            # Simular envio (sem realmente enviar)
            print("🚀 SIMULAÇÃO DE ENVIO:")
            print("-" * 30)
            print(f"📤 De: chmulato@gmail.com")
            print(f"📥 Para: {destinatario}")
            print(f"📧 Assunto: Candidatura - {vaga_nome} - {empresa_nome}")
            print(f"📎 Anexo: currículo.pdf")
            print(f"📄 Tamanho mensagem: {len(mensagem_personalizada)} caracteres")
            print()

            # Simular delay de processamento
            import time
            print("⏳ Processando envio...")
            time.sleep(1)
            print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
            print(f"💡 O email seria enviado para {destinatario} se estivesse em modo real")
            print()

            self.log_result("Simulação chmulato", "PASS", f"simulação completa para {destinatario}")

        except Exception as e:
            self.log_result("Simulação chmulato", "FAIL", f"erro na simulação: {e}")

    def generate_report(self):
        """Gera relatório final dos testes."""
        print("\n📋 RELATÓRIO FINAL DOS TESTES")
        print("=" * 50)

        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.results if r['status'] == 'FAIL'])
        warn_tests = len([r for r in self.results if r['status'] == 'WARN'])

        print(f"Total de testes executados: {total_tests}")
        print(f"✅ Aprovados: {passed_tests}")
        print(f"❌ Falhas: {failed_tests}")
        print(f"⚠️ Avisos: {warn_tests}")

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"Taxa de sucesso: {success_rate:.1f}%")

        if failed_tests > 0:
            print("\n[ERRO] TESTES COM FALHA:")
            for error in self.errors:
                print(f"  - {error['test']}: {error['message']}")

        if success_rate >= 80:
            print("\n[SUCESSO] SISTEMA PRONTO PARA USO!")
        elif success_rate >= 60:
            print("\n[AVISO] SISTEMA FUNCIONAL MAS COM ALGUMAS QUESTOES")
        else:
            print("\n[ERRO] SISTEMA PRECISA DE AJUSTES ANTES DO USO")

        return success_rate >= 80

def main():
    """Função principal do teste."""
    print("[TESTE] TESTE COMPLETO DO SISTEMA SENDING_CV")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Diretório: {os.getcwd()}")
    print()

    tester = SendingCVTester()

    # Executar todos os testes
    tester.test_project_structure()
    tester.test_configurations()
    tester.test_data_files()
    tester.test_document_conversion()
    tester.test_dependencies()
    tester.test_core_modules()
    tester.test_main_execution()
    tester.test_email_connectivity()
    tester.test_email_simulation()
    tester.test_email_simulation_chmulato()

    # Gerar relatório final
    success = tester.generate_report()

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
