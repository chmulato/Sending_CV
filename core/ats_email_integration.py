#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATS Email Integration - Integração entre Análise ATS e Envio de Emails
=======================================================================

DESCRIÇÃO:
Este módulo integra a análise ATS com o sistema de envio de emails, garantindo
que apenas currículos com pontuação ATS adequada sejam enviados para as empresas.

LÓGICA DE FUNCIONAMENTO:

1. ANÁLISE PRÉ-ENVIO:
   - Carrega currículos da pasta curriculos/
   - Converte PDF/DOCX para TXT se necessário
   - Executa análise ATS contra todas as vagas disponíveis
   - Calcula pontuação para cada combinação currículo-vaga

2. FILTRAGEM INTELIGENTE:
   - Seleciona a melhor combinação currículo-vaga baseada na pontuação
   - Só permite envio se pontuação ≥ 70%
   - Registra pontuações na planilha de log

3. ENVIO CONDICIONAL:
   - Envia email apenas para combinações aprovadas
   - Anexa currículo convertido (TXT) para compatibilidade ATS
   - Registra status e pontuação no log

4. RELATÓRIOS E MONITORAMENTO:
   - Gera relatório de análise pré-envio
   - Mostra estatísticas de aprovação/reprovação
   - Sugere melhorias nos currículos quando necessário

INTEGRAÇÃO COM SISTEMA EXISTENTE:
- Utiliza ats_analyzer.py para análise técnica
- Mantém compatibilidade com sistema de email atual
- Adiciona coluna 'Pontuacao_ATS' na planilha de log

DEPENDÊNCIAS:
- pandas: manipulação de planilhas
- core.ats_analyzer: análise ATS
- yagmail: envio de emails
- datetime: timestamps

EXEMPLO DE FLUXO:
1. carregar_curriculos_para_analise()
2. executar_analise_ats()
3. filtrar_candidaturas_aprovadas()
4. enviar_emails_aprovados()
5. atualizar_log_com_pontuacoes()

Autor: Cara Core Informática
Data: 2025
Licença: MIT
"""

import os
import pandas as pd
from datetime import datetime
import time
import yagmail
import yaml
from core import ats_analyzer

class ATSEmailIntegration:
    """Classe principal para integração ATS + Email."""

    def __init__(self, config_path='config.yaml'):
        """Inicializa a integração com configurações."""
        self.config = self.carregar_config(config_path)
        self.df_empresas = None
        self.df_log = None
        self.resultados_ats = {}

    def carregar_config(self, config_path):
        """Carrega configurações do arquivo YAML."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            return {}

    def carregar_dados(self):
        """Carrega dados das planilhas."""
        try:
            self.df_empresas = pd.read_excel('empresas.xlsx')
            self.df_log = pd.read_excel('log/log_respostas.xlsx')
            print(f"✅ Dados carregados: {len(self.df_empresas)} empresas, {len(self.df_log)} registros de log")
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
        return True

    def preparar_pasta_curriculos(self):
        """Garante que a pasta de currículos existe."""
        pasta_curriculos = 'curriculos'
        if not os.path.exists(pasta_curriculos):
            os.makedirs(pasta_curriculos)
            print(f"📁 Pasta criada: {pasta_curriculos}")
        return pasta_curriculos

    def analisar_curriculos_ats(self):
        """Executa análise ATS para todos os currículos disponíveis."""
        print("\n🔍 Iniciando análise ATS pré-envio...")

        pasta_curriculos = self.preparar_pasta_curriculos()
        pasta_vagas = 'vagas'

        # Verifica se há arquivos para analisar
        arquivos_curriculos = [f for f in os.listdir(pasta_curriculos)
                              if f.lower().endswith(('.txt', '.docx', '.pdf'))]

        if not arquivos_curriculos:
            print("⚠️  Nenhum currículo encontrado na pasta curriculos/")
            print("💡 Adicione seus currículos na pasta curriculos/ antes de executar")
            return False

        print(f"📄 Encontrados {len(arquivos_curriculos)} currículo(s) para análise")

        # Executa análise ATS
        try:
            # Chama a função de análise do ats_analyzer
            resultados = self.executar_analise_ats_batch(pasta_curriculos, pasta_vagas)
            self.resultados_ats = resultados
            return True
        except Exception as e:
            print(f"Erro na análise ATS: {e}")
            return False

    def executar_analise_ats_batch(self, pasta_curriculos, pasta_vagas):
        """Executa análise ATS em lote para todos os currículos."""
        resultados = {}

        # Lista arquivos de currículos
        arquivos_curriculos = [f for f in os.listdir(pasta_curriculos)
                              if f.lower().endswith(('.txt', '.docx', '.pdf'))]

        # Lista arquivos de vagas
        arquivos_vagas = [f for f in os.listdir(pasta_vagas)
                         if f.lower().endswith(('.txt', '.docx', '.pdf'))] if os.path.exists(pasta_vagas) else []

        if not arquivos_vagas:
            print("⚠️  Nenhuma vaga encontrada para análise")
            return resultados

        print(f"🎯 Analisando {len(arquivos_curriculos)} currículo(s) contra {len(arquivos_vagas)} vaga(s)")

        for curriculo_file in arquivos_curriculos:
            caminho_curriculo = os.path.join(pasta_curriculos, curriculo_file)
            nome_base = os.path.splitext(curriculo_file)[0]

            print(f"\n👤 Analisando currículo: {curriculo_file}")

            # Carrega e converte currículo se necessário
            texto_curriculo = ats_analyzer.carregar_arquivo(caminho_curriculo)
            if not texto_curriculo:
                continue

            tokens_curriculo = ats_analyzer.tokenizar(texto_curriculo)
            melhores_resultados = []

            # Analisa contra cada vaga
            for vaga_file in arquivos_vagas:
                caminho_vaga = os.path.join(pasta_vagas, vaga_file)
                nome_vaga = os.path.splitext(vaga_file)[0]

                # Carrega vaga
                texto_vaga = ats_analyzer.carregar_arquivo(caminho_vaga)
                if not texto_vaga:
                    continue

                tokens_vaga = ats_analyzer.tokenizar(texto_vaga)

                # Calcula pontuação
                pontuacao, palavras_faltantes = ats_analyzer.analisar_compatibilidade(
                    tokens_curriculo, tokens_vaga
                )

                melhores_resultados.append({
                    'vaga': nome_vaga,
                    'pontuacao': pontuacao,
                    'palavras_faltantes': palavras_faltantes,
                    'caminho_curriculo': caminho_curriculo
                })

                print(f"   🎯 Vaga '{nome_vaga}': {pontuacao}%")

            # Ordena por pontuação e pega o melhor resultado
            if melhores_resultados:
                melhores_resultados.sort(key=lambda x: x['pontuacao'], reverse=True)
                melhor = melhores_resultados[0]
                resultados[nome_base] = melhor

                print(f"   ✅ Melhor compatibilidade: {melhor['vaga']} ({melhor['pontuacao']}%)")

        return resultados

    def filtrar_candidaturas_aprovadas(self):
        """Filtra apenas candidaturas com pontuação ATS ≥ 70%."""
        print("\n🎯 Filtrando candidaturas aprovadas (≥70%)...")

        aprovadas = {}
        reprovadas = {}

        for nome_curriculo, resultado in self.resultados_ats.items():
            if resultado['pontuacao'] >= 70:
                aprovadas[nome_curriculo] = resultado
                print(f"   ✅ APROVADO: {nome_curriculo} - {resultado['pontuacao']}%")
            else:
                reprovadas[nome_curriculo] = resultado
                print(f"   ❌ REPROVADO: {nome_curriculo} - {resultado['pontuacao']}%")

        print(f"\n📊 Resumo da análise:")
        print(f"   ✅ Aprovados: {len(aprovadas)}")
        print(f"   ❌ Reprovados: {len(reprovadas)}")
        print(f"   📈 Taxa de aprovação: {(len(aprovadas)/(len(aprovadas)+len(reprovadas))*100):.1f}%")

        return aprovadas, reprovadas

    def preparar_email_personalizado(self, empresa, vaga, pontuacao_ats):
        """Prepara conteúdo personalizado do email baseado na análise ATS."""
        try:
            with open('templates/mensagem_email.txt', 'r', encoding='utf-8') as f:
                template = f.read()
        except:
            template = "Assunto: Candidatura para {vaga} - {empresa}\n\nPrezados,\n\nInteressado na vaga de {vaga}."

        # Substitui placeholders
        mensagem = template.replace('{empresa}', empresa)
        mensagem = template.replace('{vaga}', vaga)

        # Adiciona informação sobre pontuação ATS
        if pontuacao_ats >= 70:
            status_ats = f"✅ Currículo otimizado para ATS ({pontuacao_ats}%)"
        else:
            status_ats = f"⚠️  Currículo precisa de ajustes ({pontuacao_ats}%)"

        # Adiciona status ATS ao final da mensagem
        mensagem += f"\n\n{status_ats}"

        return mensagem

    def enviar_emails_aprovados(self, candidaturas_aprovadas):
        """Envia emails apenas para candidaturas aprovadas."""
        if not candidaturas_aprovadas:
            print("⚠️  Nenhuma candidatura aprovada para envio")
            return

        print(f"\n📧 Enviando emails para {len(candidaturas_aprovadas)} candidatura(s) aprovada(s)...")

        # Configuração do email
        email_config = self.config.get('email', {})
        yag = yagmail.SMTP(email_config.get('usuario'), email_config.get('senha_app'))

        delay = self.config.get('envio', {}).get('delay_entre_emails', 30)

        emails_enviados = 0

        for nome_curriculo, dados in candidaturas_aprovadas.items():
            try:
                # Encontra empresa correspondente à vaga
                vaga_nome = dados['vaga']
                empresas_vaga = self.df_empresas[self.df_empresas['Vaga'].str.contains(vaga_nome, case=False, na=False)]

                if empresas_vaga.empty:
                    print(f"   ⚠️  Nenhuma empresa encontrada para vaga '{vaga_nome}'")
                    continue

                # Envia para todas as empresas da vaga
                for _, empresa in empresas_vaga.iterrows():
                    empresa_nome = empresa['Empresa']
                    empresa_email = empresa['Email']

                    # Verifica se já foi enviado
                    ja_enviado = ((self.df_log['Email'] == empresa_email) &
                                (self.df_log['Vaga'] == empresa['Vaga'])).any()

                    if ja_enviado:
                        print(f"   ⏭️  Já enviado para {empresa_nome} ({empresa_email})")
                        continue

                    # Prepara email
                    assunto, corpo = self.preparar_email_personalizado(
                        empresa_nome, empresa['Vaga'], dados['pontuacao']
                    ).split('\n', 1)

                    # Anexa currículo (versão TXT para melhor compatibilidade ATS)
                    anexos = [dados['caminho_curriculo']]

                    print(f"   📧 Enviando para {empresa_nome} ({empresa_email})...")

                    # Envia email
                    yag.send(
                        to=empresa_email,
                        subject=assunto,
                        contents=corpo,
                        attachments=anexos
                    )

                    # Registra no log
                    self.registrar_envio_log(
                        empresa_nome, empresa['Vaga'], empresa_email,
                        dados['pontuacao'], "Enviado com análise ATS"
                    )

                    emails_enviados += 1
                    print(f"   ✅ Email enviado com sucesso!")

                    # Delay entre envios
                    if delay > 0:
                        print(f"   ⏱️  Aguardando {delay}s...")
                        time.sleep(delay)

            except Exception as e:
                print(f"   ❌ Erro ao enviar para {nome_curriculo}: {e}")

        print(f"\n📊 Total de emails enviados: {emails_enviados}")

    def registrar_envio_log(self, empresa, vaga, email, pontuacao_ats, observacoes):
        """Registra envio no log com pontuação ATS."""
        novo_registro = {
            'Empresa': empresa,
            'Vaga': vaga,
            'Email': email,
            'Data_Envio': datetime.now(),
            'Data_Seguimento': None,
            'Status': 'Enviado',
            'Observações': f"{observacoes} | Pontuação ATS: {pontuacao_ats}%",
            'Numero_Followup': 0,
            'Pontuacao_ATS': pontuacao_ats
        }

        # Adiciona nova linha ao DataFrame
        self.df_log = pd.concat([self.df_log, pd.DataFrame([novo_registro])], ignore_index=True)

        # Salva no arquivo
        self.df_log.to_excel('log/log_respostas.xlsx', index=False)

    def gerar_relatorio_analise(self, aprovadas, reprovadas):
        """Gera relatório completo da análise ATS."""
        print("\n📊 RELATÓRIO DE ANÁLISE ATS PRÉ-ENVIO")
        print("=" * 50)

        total_analisados = len(aprovadas) + len(reprovadas)

        if total_analisados == 0:
            print("Nenhum currículo foi analisado.")
            return

        taxa_aprovacao = (len(aprovadas) / total_analisados) * 100

        print(f"📄 Currículos analisados: {total_analisados}")
        print(f"✅ Aprovados (≥70%): {len(aprovadas)}")
        print(f"❌ Reprovados (<70%): {len(reprovadas)}")
        print(f"📈 Taxa de aprovação: {taxa_aprovacao:.1f}%")

        if aprovadas:
            print(f"\n🏆 CANDIDATURAS APROVADAS:")
            for nome, dados in aprovadas.items():
                print(f"   • {nome}: {dados['pontuacao']}% - Vaga: {dados['vaga']}")

        if reprovadas:
            print(f"\n⚠️  CANDIDATURAS QUE PRECISAM DE AJUSTES:")
            for nome, dados in reprovadas.items():
                print(f"   • {nome}: {dados['pontuacao']}% - Vaga: {dados['vaga']}")
                if dados['palavras_faltantes']:
                    faltantes = dados['palavras_faltantes'][:5]  # Top 5
                    print(f"      Palavras-chave sugeridas: {', '.join(faltantes)}")

    def executar_fluxo_completo(self):
        """Executa o fluxo completo: análise ATS → filtragem → envio."""
        print("🚀 Iniciando fluxo integrado ATS + Email")
        print("=" * 60)

        # 1. Carrega dados
        if not self.carregar_dados():
            return False

        # 2. Executa análise ATS
        if not self.analisar_curriculos_ats():
            return False

        # 3. Filtra candidaturas aprovadas
        aprovadas, reprovadas = self.filtrar_candidaturas_aprovadas()

        # 4. Gera relatório
        self.gerar_relatorio_analise(aprovadas, reprovadas)

        # 5. Envia emails aprovados
        if aprovadas:
            self.enviar_emails_aprovados(aprovadas)
        else:
            print("\n⚠️  Nenhum currículo atingiu a pontuação mínima de 70%")
            print("💡 Otimize seus currículos antes de enviar")

        print("\n" + "=" * 60)
        print("✅ Fluxo integrado concluído!")
        return True

def main():
    """Função principal do módulo de integração."""
    integracao = ATSEmailIntegration()
    integracao.executar_fluxo_completo()

if __name__ == "__main__":
    main()
