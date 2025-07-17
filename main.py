#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sending_CV - Automação de Envio de Currículos
=============================================

Este script automatiza o processo de envio de currículos para empresas,
incluindo controle de follow-up e logging detalhado das interações.

Autor: Cara Core Informática - Automação
Data: Campo Largo, PR, quarta-feira, 16 de Julho 2025.
"""

import pandas as pd
import yagmail
import yaml
import schedule
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

class SendingCV:
    """
    Classe principal para automação de envio de currículos.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Inicializa a classe com as configurações.
        
        Args:
            config_path: Caminho para o arquivo de configuração YAML
        """
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.yag = None
        
    def _load_config(self, config_path: str) -> Dict:
        """Carrega as configurações do arquivo YAML."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de configuração '{config_path}' não encontrado!")
        except yaml.YAMLError as e:
            raise ValueError(f"Erro ao ler arquivo YAML: {e}")
    
    def setup_logging(self):
        """Configura o sistema de logging."""
        # Cria a pasta log se não existir
        log_dir = 'log'
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'sending_cv.log'), encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def connect_email(self) -> bool:
        """
        Estabelece conexão com o servidor de email.
        
        Returns:
            bool: True se a conexão foi bem-sucedida
        """
        try:
            email_config = self.config['email']
            self.yag = yagmail.SMTP(
                user=email_config['usuario'],
                password=email_config['senha_app'],
                host=email_config['servidor_smtp'],
                port=email_config['porta'],
                smtp_starttls=True,
                smtp_ssl=False
            )
            self.logger.info("Conexão com email estabelecida com sucesso!")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao conectar com email: {e}")
            return False
    
    def load_empresas(self) -> pd.DataFrame:
        """
        Carrega a lista de empresas do arquivo Excel.
        
        Returns:
            DataFrame com os dados das empresas
        """
        try:
            arquivo_empresas = self.config['arquivos']['empresas']
            df = pd.read_excel(arquivo_empresas)
            self.logger.info(f"Carregadas {len(df)} empresas da lista")
            return df
        except Exception as e:
            self.logger.error(f"Erro ao carregar arquivo de empresas: {e}")
            return pd.DataFrame()
    
    def load_log_respostas(self) -> pd.DataFrame:
        """
        Carrega o log de respostas, criando um novo se não existir.
        
        Returns:
            DataFrame com o histórico de envios
        """
        arquivo_log = self.config['arquivos']['log_respostas']
        
        if os.path.exists(arquivo_log):
            try:
                return pd.read_excel(arquivo_log)
            except Exception as e:
                self.logger.warning(f"Erro ao carregar log existente: {e}")
        
        # Cria um novo DataFrame se o arquivo não existir
        colunas = ['Empresa', 'Vaga', 'Email', 'Data_Envio', 'Data_Seguimento', 
                  'Status', 'Observações', 'Numero_Followup']
        df_log = pd.DataFrame(columns=colunas)
        self.save_log_respostas(df_log)
        self.logger.info("Novo arquivo de log criado")
        return df_log
    
    def save_log_respostas(self, df: pd.DataFrame):
        """
        Salva o log de respostas no arquivo Excel.
        
        Args:
            df: DataFrame com os dados a serem salvos
        """
        try:
            arquivo_log = self.config['arquivos']['log_respostas']
            df.to_excel(arquivo_log, index=False)
            self.logger.info("Log de respostas salvo com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao salvar log: {e}")
    
    def load_template_email(self) -> str:
        """
        Carrega o template de email.
        
        Returns:
            String com o conteúdo do template
        """
        try:
            arquivo_template = self.config['arquivos']['template_email']
            with open(arquivo_template, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"Erro ao carregar template: {e}")
            return ""
    
    def personalizar_email(self, template: str, empresa: str, vaga: str) -> Dict[str, str]:
        """
        Personaliza o template de email com os dados da empresa.
        
        Args:
            template: Template base do email
            empresa: Nome da empresa
            vaga: Nome da vaga
            
        Returns:
            Dicionário com assunto e corpo do email
        """
        # Dados pessoais (configure conforme necessário)
        dados_pessoais = {
            'empresa': empresa,
            'vaga': vaga,
            'anos_experiencia': '3',  # Configure conforme sua experiência
            'tecnologias_principais': 'Python, JavaScript, React, Node.js'  # Configure suas skills
        }
        
        corpo_email = template.format(**dados_pessoais)
        
        # Extrair assunto do template (primeira linha)
        linhas = corpo_email.split('\n')
        assunto = linhas[0].replace('Assunto: ', '') if linhas[0].startswith('Assunto: ') else f"Candidatura para vaga de {vaga} - {empresa}"
        corpo = '\n'.join(linhas[2:])  # Remove linha do assunto e linha vazia
        
        return {
            'assunto': assunto,
            'corpo': corpo
        }
    
    def enviar_email(self, destinatario: str, assunto: str, corpo: str) -> bool:
        """
        Envia o email com o currículo anexado.
        
        Args:
            destinatario: Email de destino
            assunto: Assunto do email
            corpo: Corpo do email
            
        Returns:
            bool: True se o envio foi bem-sucedido
        """
        try:
            anexo = self.config['arquivos']['curriculo']
            
            if not os.path.exists(anexo):
                self.logger.error(f"Arquivo de currículo '{anexo}' não encontrado!")
                return False
            
            self.yag.send(
                to=destinatario,
                subject=assunto,
                contents=corpo,
                attachments=anexo
            )
            
            self.logger.info(f"Email enviado com sucesso para {destinatario}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar email para {destinatario}: {e}")
            return False
    
    def verificar_horario_funcionamento(self) -> bool:
        """
        Verifica se está dentro do horário de funcionamento configurado.
        
        Returns:
            bool: True se estiver no horário de funcionamento
        """
        agora = datetime.now().time()
        config_horario = self.config['envio']['horario_funcionamento']
        
        inicio = datetime.strptime(config_horario['inicio'], '%H:%M').time()
        fim = datetime.strptime(config_horario['fim'], '%H:%M').time()
        
        return inicio <= agora <= fim
    
    def processar_envios(self):
        """
        Processa a lista de empresas e envia emails conforme necessário.
        """
        if not self.verificar_horario_funcionamento():
            self.logger.info("Fora do horário de funcionamento. Aguardando...")
            return
        
        if not self.connect_email():
            self.logger.error("Não foi possível conectar ao email. Abortando...")
            return
        
        # Carrega dados
        df_empresas = self.load_empresas()
        df_log = self.load_log_respostas()
        template = self.load_template_email()
        
        if df_empresas.empty or not template:
            self.logger.error("Dados insuficientes para processar envios")
            return
        
        # Filtra empresas que ainda não foram contatadas
        empresas_contatadas = df_log['Email'].tolist() if not df_log.empty else []
        empresas_pendentes = df_empresas[~df_empresas['Email'].isin(empresas_contatadas)]
        
        max_envios = self.config['envio']['max_envios_por_dia']
        delay = self.config['envio']['delay_entre_emails']
        
        contador_envios = 0
        
        for _, empresa in empresas_pendentes.iterrows():
            if contador_envios >= max_envios:
                self.logger.info(f"Limite diário de {max_envios} envios atingido")
                break
            
            # Personaliza email
            email_personalizado = self.personalizar_email(
                template, 
                empresa['Empresa'], 
                empresa['Vaga']
            )
            
            # Envia email
            sucesso = self.enviar_email(
                empresa['Email'],
                email_personalizado['assunto'],
                email_personalizado['corpo']
            )
            
            if sucesso:
                # Adiciona ao log
                novo_registro = {
                    'Empresa': empresa['Empresa'],
                    'Vaga': empresa['Vaga'],
                    'Email': empresa['Email'],
                    'Data_Envio': datetime.now().strftime('%Y-%m-%d'),
                    'Data_Seguimento': (datetime.now() + timedelta(days=self.config['followup']['dias_para_seguimento'])).strftime('%Y-%m-%d'),
                    'Status': 'Enviado',
                    'Observações': 'Envio automático',
                    'Numero_Followup': 0
                }
                
                df_log = pd.concat([df_log, pd.DataFrame([novo_registro])], ignore_index=True)
                contador_envios += 1
                
                # Delay entre envios
                if contador_envios < max_envios and contador_envios < len(empresas_pendentes):
                    self.logger.info(f"Aguardando {delay} segundos antes do próximo envio...")
                    time.sleep(delay)
        
        # Salva log atualizado
        self.save_log_respostas(df_log)
        self.logger.info(f"Processamento concluído. {contador_envios} emails enviados.")
    
    def verificar_followups(self):
        """
        Verifica e processa follow-ups necessários.
        """
        df_log = self.load_log_respostas()
        
        if df_log.empty:
            return
        
        hoje = datetime.now().date()
        
        # Filtra registros que precisam de follow-up
        df_log['Data_Seguimento'] = pd.to_datetime(df_log['Data_Seguimento']).dt.date
        
        followups_pendentes = df_log[
            (df_log['Data_Seguimento'] <= hoje) & 
            (df_log['Status'] == 'Enviado') &
            (df_log['Numero_Followup'] < self.config['followup']['max_followups'])
        ]
        
        if not followups_pendentes.empty:
            self.logger.info(f"{len(followups_pendentes)} follow-ups identificados para hoje")
            # Aqui você pode implementar a lógica de follow-up
            # Por simplicidade, apenas logamos por enquanto
            for _, registro in followups_pendentes.iterrows():
                self.logger.info(f"Follow-up pendente: {registro['Empresa']} - {registro['Vaga']}")
    
    def executar_agendamento(self):
        """
        Configura e executa o agendamento das tarefas.
        """
        # Agenda processamento de envios
        schedule.every().day.at("09:00").do(self.processar_envios)
        schedule.every().day.at("14:00").do(self.processar_envios)
        
        # Agenda verificação de follow-ups
        schedule.every().day.at("10:00").do(self.verificar_followups)
        
        self.logger.info("Agendamento configurado. Sistema iniciado!")
        self.logger.info("Pressione Ctrl+C para parar")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
        except KeyboardInterrupt:
            self.logger.info("Sistema interrompido pelo usuário")

def main():
    """
    Função principal do programa.
    """
    print("🚀 Sending_CV - Automação de Envio de Currículos")
    print("=" * 50)
    
    try:
        sender = SendingCV()
        
        # Menu simples
        while True:
            print("\nOpções:")
            print("1. Processar envios agora")
            print("2. Verificar follow-ups")
            print("3. Iniciar modo agendado")
            print("4. Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                sender.processar_envios()
            elif opcao == "2":
                sender.verificar_followups()
            elif opcao == "3":
                sender.executar_agendamento()
            elif opcao == "4":
                print("Encerrando programa...")
                break
            else:
                print("Opção inválida!")
                
    except Exception as e:
        print(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()
