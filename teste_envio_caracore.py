#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Envio para Caracore
============================

Script para testar o envio de email para o RH da Caracore.
"""

import pandas as pd
import sys
import os
from datetime import datetime
from main import SendingCV

def teste_envio_caracore():
    """
    Testa o envio de email para o RH da Caracore.
    """
    print("=== TESTE DE ENVIO PARA CARACORE ===")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    try:
        # Inicializa o sistema
        cv_sender = SendingCV()
        
        # Dados da Caracore para teste
        empresa_teste = {
            'Empresa': 'Caracore',
            'Vaga': 'Desenvolvedor Python',
            'Email': 'suporte@caracore.com.br'
        }
        
        print(f"Empresa: {empresa_teste['Empresa']}")
        print(f"Vaga: {empresa_teste['Vaga']}")
        print(f"Email: {empresa_teste['Email']}")
        print()
        
        # Verifica se está no horário de funcionamento
        if not cv_sender.verificar_horario_funcionamento():
            print("⚠️  AVISO: Fora do horário de funcionamento configurado")
            resposta = input("Deseja continuar mesmo assim? (s/n): ")
            if resposta.lower() != 's':
                print("Teste cancelado pelo usuário.")
                return
        
        # Conecta ao email
        print("Conectando ao Gmail...")
        if not cv_sender.connect_email():
            print("❌ Erro: Não foi possível conectar ao email.")
            print("Verifique as configurações no arquivo config.yaml")
            return
        
        print("✅ Conexão com Gmail estabelecida!")
        
        # Carrega template
        print("Carregando template de email...")
        template = cv_sender.load_template_email()
        if not template:
            print("❌ Erro: Não foi possível carregar o template de email.")
            return
        
        print("✅ Template carregado!")
        
        # Personaliza email
        print("Personalizando email...")
        email_personalizado = cv_sender.personalizar_email(
            template,
            empresa_teste['Empresa'],
            empresa_teste['Vaga']
        )
        
        print(f"Assunto: {email_personalizado['assunto']}")
        print()
        print("Prévia do corpo do email:")
        print("-" * 50)
        print(email_personalizado['corpo'][:300] + "...")
        print("-" * 50)
        print()
        
        # Confirma envio
        resposta = input("Deseja enviar o email? (s/n): ")
        if resposta.lower() != 's':
            print("Envio cancelado pelo usuário.")
            return
        
        # Verifica se o currículo existe
        curriculo_path = cv_sender.config['arquivos']['curriculo']
        if not os.path.exists(curriculo_path):
            print(f"❌ Erro: Arquivo de currículo '{curriculo_path}' não encontrado!")
            return
        
        print(f"✅ Currículo encontrado: {curriculo_path}")
        
        # Envia email
        print("Enviando email...")
        sucesso = cv_sender.enviar_email(
            empresa_teste['Email'],
            email_personalizado['assunto'],
            email_personalizado['corpo']
        )
        
        if sucesso:
            print("✅ Email enviado com sucesso!")
            
            # Registra no log
            print("Registrando no log...")
            df_log = cv_sender.load_log_respostas()
            
            novo_registro = {
                'Empresa': empresa_teste['Empresa'],
                'Vaga': empresa_teste['Vaga'],
                'Email': empresa_teste['Email'],
                'Data_Envio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Data_Seguimento': '',
                'Status': 'Enviado - Teste',
                'Observações': 'Teste de envio manual',
                'Numero_Followup': 0
            }
            
            df_log = pd.concat([df_log, pd.DataFrame([novo_registro])], ignore_index=True)
            cv_sender.save_log_respostas(df_log)
            
            print("✅ Registro salvo no log!")
            print()
            print("=== TESTE CONCLUÍDO COM SUCESSO! ===")
            
        else:
            print("❌ Falha no envio do email!")
            print("Verifique os logs para mais detalhes.")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_envio_caracore()
