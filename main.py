#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sending_CV - Sistema Integrado de Análise ATS e Envio de Currículos
===================================================================

DESCRIÇÃO GERAL:
Sistema completo para análise de currículos usando tecnologia ATS (Applicant Tracking System)
e envio automatizado de emails para empresas, com integração inteligente entre análise e envio.

MODOS DE FUNCIONAMENTO:

1. MODO ANÁLISE (python main.py analise):
   - Análise ATS completa de currículos
   - Comparação com vagas disponíveis
   - Geração de relatórios de compatibilidade
   - Recomendações de otimização

2. MODO ENVIO (python main.py envio):
   - Análise ATS pré-envio
   - Filtragem automática (≥70% de pontuação)
   - Envio de emails apenas para currículos aprovados
   - Registro de pontuações no log

3. MODO PADRÃO (python main.py):
   - Análise ATS básica
   - Sem envio de emails

LÓGICA DE FUNCIONAMENTO:

1. DETECÇÃO E CONVERSÃO DE ARQUIVOS:
   - Detecta automaticamente arquivos .txt, .docx e .pdf nas pastas curriculos/ e vagas/
   - Converte .docx para .txt usando python-docx
   - Converte .pdf para .txt usando pdfplumber
   - Salva versões .txt para processamento futuro

2. ANÁLISE DE TEXTO E TOKENIZAÇÃO:
   - Remove acentos e caracteres especiais
   - Converte para minúsculas
   - Remove stopwords (palavras comuns: de, a, e, o, etc.)
   - Separa o texto em palavras relevantes (tokens)

3. CÁLCULO DE FREQUÊNCIA E PONTUAÇÃO:
   - Conta frequência relativa de cada palavra em currículos e vagas
   - Calcula similaridade baseada na presença de palavras-chave
   - Pontuação = média das presenças das palavras-chave da vaga no currículo
   - Meta: atingir ≥70% de pontuação para aprovação no modo envio

4. INTEGRAÇÃO COM ENVIO DE EMAILS:
   - No modo envio: só envia emails para currículos com ≥70%
   - Registra pontuação ATS na planilha de log
   - Anexa versão otimizada do currículo
   - Personaliza mensagem com status ATS

5. GERAÇÃO DE RECOMENDAÇÕES:
   - Identifica palavras-chave faltantes
   - Sugere adições ao currículo
   - Salva versão ajustada do currículo quando necessário

FORMATOS SUPORTADOS:
- .txt: Texto plano (processamento direto)
- .docx: Documentos Word (conversão automática)
- .pdf: Documentos PDF (conversão automática)

METODOLOGIA ATS:
- Análise baseada em frequência de termos
- Foco em palavras-chave técnicas e comportamentais
- Comparação quantitativa e qualitativa
- Recomendações personalizadas por candidato

EXEMPLO DE SAÍDA:
==================================================
Analisando vaga: analista_dados.txt
Currículo: joao_silva.docx (convertido de .docx)
Pontuação ATS: 85.2%
Pontuacao acima do minimo (70.0%). Email enviado!

==================================================

COMANDOS DISPONÍVEIS:
python main.py              # Análise básica
python main.py analise      # Análise completa
python main.py organizado   # Sistema organizado por vaga
python main.py envio        # Análise + envio integrado

Autor: Cara Core Informática
Data: 2025
Licença: MIT
"""

from core import ats_analyzer
from core import ats_email_integration
from core import ats_organizer
import sys

def main():
    print("Sistema ATS - Cara Core Informatica")
    print("=" * 50)

    if len(sys.argv) > 1:
        modo = sys.argv[1].lower()

        if modo == "analise":
            print("MODO: Analise ATS apenas")
            print("Analisando curriculos e vagas...\n")
            ats_analyzer.main()

        elif modo == "organizado":
            print("MODO: Sistema Organizado por Vaga")
            print("Analisando estrutura organizada de vagas...\n")
            organizer = ats_organizer.ATSOrganizer()
            organizer.executar_analise_organizada()
            organizer.gerar_relatorios_por_vaga()
            organizer.exportar_resultados_csv()

        elif modo == "envio":
            print("MODO: Analise ATS + Envio de Emails")
            print("Executando analise e envio integrado...\n")
            integracao = ats_email_integration.ATSEmailIntegration()
            integracao.executar_fluxo_completo()

        else:
            print("❌ Modo não reconhecido. Use:")
            print("   python main.py analise      # Analise basica")
            print("   python main.py organizado   # Sistema organizado por vaga")
            print("   python main.py envio        # Analise + envio integrado")
            return
    else:
        print("🔍 MODO PADRÃO: Análise ATS apenas")
        print("Analisando currículos e vagas...")
        print("Arquivos .docx e .pdf serão automaticamente convertidos para .txt\n")

        ats_analyzer.main()

    print("\n" + "=" * 50)
    print("Processo concluido!")
    print("Verifique se a pontuacao ATS atingiu 70% ou mais.")
    print("Siga as recomendacoes para otimizar seu curriculo.")

if __name__ == "__main__":
    main()
