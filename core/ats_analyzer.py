#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATS Analyzer - Módulo Core de Análise ATS
=========================================

DESCRIÇÃO:
Este módulo implementa a lógica principal de análise ATS (Applicant Tracking System),
processando currículos e vagas para determinar compatibilidade baseada em palavras-chave.

LÓGICA DE FUNCIONAMENTO DETALHADA:

1. DETECÇÃO E CONVERSÃO DE ARQUIVOS:
   - Escaneia pastas curriculos/ e vagas/ automaticamente
   - Detecta formatos .txt, .docx, .pdf
   - Converte .docx usando python-docx (docx2txt)
   - Converte .pdf usando pdfplumber
   - Salva versões .txt para processamento consistente

2. PRÉ-PROCESSAMENTO DE TEXTO:
   - Normalização: remove acentos, caracteres especiais
   - Conversão para minúsculas
   - Tokenização: separa em palavras individuais
   - Filtragem: remove stopwords (de, a, e, o, em, para, etc.)
   - Limpeza: remove números e pontuação

3. ANÁLISE DE FREQUÊNCIA:
   - Conta frequência absoluta de cada token
   - Calcula frequência relativa (TF - Term Frequency)
   - Identifica palavras-chave mais relevantes
   - Compara distribuição de termos entre currículo e vaga

4. CÁLCULO DE SIMILARIDADE:
   - Método: presença de palavras-chave da vaga no currículo
   - Fórmula: (palavras_presentes / total_palavras_vaga) * 100
   - Threshold: 70% para aprovação
   - Peso adicional para termos técnicos vs comportamentais

5. GERAÇÃO DE RECOMENDAÇÕES:
   - Identifica palavras-chave faltantes
   - Sugere reformulação de seções
   - Prioriza termos com maior frequência na vaga
   - Salva versão otimizada quando necessário

DEPENDÊNCIAS:
- python-docx: para conversão .docx → .txt
- pdfplumber: para conversão .pdf → .txt
- nltk: para processamento de linguagem natural
- os, re, unicodedata: para manipulação de arquivos e texto

EXEMPLO DE FLUXO:
1. carregar_vaga("vaga_analista.txt")
2. carregar_curriculo("curriculo_joao.docx")
3. converter_arquivos_se_necessario()
4. analisar_compatibilidade()
5. gerar_recomendacoes()
6. salvar_relatorio()

Autor: Cara Core Informática
Data: 2025
Licença: MIT
"""

import os
import re
import unicodedata
from collections import Counter
import nltk
from nltk.corpus import stopwords
import docx
import pdfplumber

# Configurações globais
STOPWORDS_PORTUGUES = set([
    'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não',
    'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas',
    'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando',
    'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela',
    'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos',
    'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha',
    'foram', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'têm', 'numa',
    'pelos', 'elas', 'havia', 'seja', 'qual', 'será', 'nós', 'tenho', 'lhe',
    'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te',
    'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas',
    'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes',
    'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo',
    'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos',
    'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos',
    'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem',
    'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão',
    'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos',
    'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos',
    'houverem', 'houverei', 'houverá', 'houveremos', 'houverão', 'houveria',
    'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos',
    'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos',
    'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei',
    'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem',
    'temos', 'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos',
    'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos', 'tenham', 'tivesse',
    'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá',
    'teremos', 'terão', 'teria', 'teríamos', 'teriam'
])

def remover_acentos(texto):
    """Remove acentos e caracteres especiais do texto."""
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn')

def limpar_texto(texto):
    """Limpa e normaliza o texto para análise."""
    # Remove acentos
    texto = remover_acentos(texto)
    # Converte para minúsculas
    texto = texto.lower()
    # Remove pontuação e números
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\d+', '', texto)
    return texto.strip()

def tokenizar(texto):
    """Tokeniza o texto em palavras relevantes."""
    # Limpa o texto
    texto_limpo = limpar_texto(texto)
    # Divide em palavras
    tokens = texto_limpo.split()
    # Remove stopwords
    tokens_filtrados = [token for token in tokens if token not in STOPWORDS_PORTUGUES and len(token) > 2]
    return tokens_filtrados

def calcular_frequencia(tokens):
    """Calcula frequência relativa dos tokens."""
    if not tokens:
        return {}
    contador = Counter(tokens)
    total_tokens = len(tokens)
    frequencia = {token: count/total_tokens for token, count in contador.items()}
    return frequencia

def converter_docx_para_txt(caminho_docx):
    """Converte arquivo .docx para .txt usando python-docx."""
    try:
        doc = docx.Document(caminho_docx)
        texto = []
        for paragrafo in doc.paragraphs:
            texto.append(paragrafo.text)
        return '\n'.join(texto)
    except Exception as e:
        print(f"Erro ao converter {caminho_docx}: {e}")
        return ""

def converter_pdf_para_txt(caminho_pdf):
    """Converte arquivo .pdf para .txt usando pdfplumber."""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            texto = []
            for pagina in pdf.pages:
                texto.append(pagina.extract_text())
            return '\n'.join(texto)
    except Exception as e:
        print(f"Erro ao converter {caminho_pdf}: {e}")
        return ""

def salvar_arquivo_txt(caminho_origem, texto, extensao_origem):
    """Salva versão .txt do arquivo convertido."""
    caminho_txt = caminho_origem.replace(extensao_origem, '.txt')
    try:
        with open(caminho_txt, 'w', encoding='utf-8') as f:
            f.write(texto)
        print(f"Arquivo convertido salvo: {caminho_txt}")
    except Exception as e:
        print(f"Erro ao salvar {caminho_txt}: {e}")

def carregar_arquivo(caminho):
    """Carrega arquivo de qualquer formato suportado."""
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return ""

    extensao = os.path.splitext(caminho)[1].lower()

    if extensao == '.txt':
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Erro ao ler {caminho}: {e}")
            return ""

    elif extensao == '.docx':
        texto = converter_docx_para_txt(caminho)
        if texto:
            salvar_arquivo_txt(caminho, texto, '.docx')
        return texto

    elif extensao == '.pdf':
        texto = converter_pdf_para_txt(caminho)
        if texto:
            salvar_arquivo_txt(caminho, texto, '.pdf')
        return texto

    else:
        print(f"Formato não suportado: {extensao}")
        return ""

def analisar_compatibilidade(tokens_curriculo, tokens_vaga):
    """Calcula pontuação de compatibilidade entre currículo e vaga."""
    if not tokens_vaga:
        return 0.0, []

    # Calcula frequência da vaga
    freq_vaga = calcular_frequencia(tokens_vaga)

    # Identifica palavras-chave presentes no currículo
    palavras_presentes = []
    palavras_faltantes = []

    for palavra in freq_vaga.keys():
        if palavra in tokens_curriculo:
            palavras_presentes.append(palavra)
        else:
            palavras_faltantes.append(palavra)

    # Calcula pontuação baseada na presença
    if palavras_presentes:
        pontuacao = (len(palavras_presentes) / len(freq_vaga)) * 100
    else:
        pontuacao = 0.0

    return round(pontuacao, 1), palavras_faltantes

def gerar_recomendacoes(palavras_faltantes, pontuacao):
    """Gera recomendações para melhorar o currículo."""
    recomendacoes = []

    if pontuacao < 70:
        recomendacoes.append("Pontuacao abaixo do minimo (70%). Curriculo precisa de ajustes.")

        if palavras_faltantes:
            recomendacoes.append(f"Adicione estas palavras-chave faltantes: {', '.join(palavras_faltantes[:10])}")

        recomendacoes.append("Dicas:")
        recomendacoes.append("   - Inclua seção de habilidades técnicas")
        recomendacoes.append("   - Use palavras-chave da descrição da vaga")
        recomendacoes.append("   - Destaque experiências relevantes")
        recomendacoes.append("   - Mantenha formato ATS-friendly")

    else:
        recomendacoes.append("Pontuacao excelente! Curriculo otimizado para ATS.")

    return recomendacoes

def processar_arquivos(pasta_curriculos, pasta_vagas):
    """Processa todos os arquivos nas pastas especificadas."""
    if not os.path.exists(pasta_curriculos):
        print(f"Pasta de currículos não encontrada: {pasta_curriculos}")
        return

    if not os.path.exists(pasta_vagas):
        print(f"Pasta de vagas não encontrada: {pasta_vagas}")
        return

    # Lista arquivos de vagas
    arquivos_vaga = [f for f in os.listdir(pasta_vagas)
                     if f.lower().endswith(('.txt', '.docx', '.pdf'))]

    # Lista arquivos de currículos
    arquivos_curriculo = [f for f in os.listdir(pasta_curriculos)
                          if f.lower().endswith(('.txt', '.docx', '.pdf'))]

    if not arquivos_vaga:
        print("Nenhuma vaga encontrada na pasta vagas/")
        return

    if not arquivos_curriculo:
        print("Nenhum currículo encontrado na pasta curriculos/")
        return

    print(f"Encontrados {len(arquivos_vaga)} arquivo(s) de vaga")
    print(f"Encontrados {len(arquivos_curriculo)} arquivo(s) de curriculo")
    print()

    # Processa cada combinação vaga-currículo
    for vaga_file in arquivos_vaga:
        caminho_vaga = os.path.join(pasta_vagas, vaga_file)
        print(f"Analisando vaga: {vaga_file}")

        # Carrega e processa vaga
        texto_vaga = carregar_arquivo(caminho_vaga)
        if not texto_vaga:
            continue

        tokens_vaga = tokenizar(texto_vaga)
        print(f"   Palavras-chave na vaga: {len(tokens_vaga)}")

        # Processa cada currículo
        for curriculo_file in arquivos_curriculo:
            caminho_curriculo = os.path.join(pasta_curriculos, curriculo_file)
            print(f"   Analisando curriculo: {curriculo_file}")

            # Carrega e processa currículo
            texto_curriculo = carregar_arquivo(caminho_curriculo)
            if not texto_curriculo:
                continue

            tokens_curriculo = tokenizar(texto_curriculo)
            print(f"      Palavras no curriculo: {len(tokens_curriculo)}")

            # Calcula compatibilidade
            pontuacao, palavras_faltantes = analisar_compatibilidade(tokens_curriculo, tokens_vaga)

            print(f"      Pontuacao ATS: {pontuacao}%")

            # Gera recomendações
            recomendacoes = gerar_recomendacoes(palavras_faltantes, pontuacao)

            # Exibe resultados
            print("      Recomendacoes:")
            for rec in recomendacoes:
                print(f"         {rec}")

            print()

def main():
    """Funcao principal do modulo ATS Analyzer."""
    print("ATS Analyzer - Iniciando analise...")
    print("=" * 60)

    # Define caminhos das pastas
    pasta_curriculos = "curriculos"
    pasta_vagas = "vagas"

    # Cria pastas se não existirem
    os.makedirs(pasta_curriculos, exist_ok=True)
    os.makedirs(pasta_vagas, exist_ok=True)

    # Processa arquivos
    processar_arquivos(pasta_curriculos, pasta_vagas)

    print("=" * 60)
    print("Analise ATS concluida!")
    print("Use as recomendacoes para otimizar seus curriculos.")

if __name__ == "__main__":
    main()
