#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATS Organizer - Sistema Organizado de Análise ATS por Vaga
==========================================================

DESCRIÇÃO:
Este módulo implementa um sistema organizado de análise ATS onde cada vaga
tem sua própria pasta com currículos específicos, garantindo análise direcionada
e eficiente.

ESTRUTURA ORGANIZADA:
vagas/
├── desenvolvedor_python/
│   ├── vaga.txt              # Descrição da vaga
│   └── curriculos/           # Currículos específicos para esta vaga
│       ├── joao_silva.pdf
│       └── maria_santos.docx
├── analista_dados/
│   ├── vaga.txt
│   └── curriculos/
│       ├── pedro_oliveira.pdf
│       └── ana_costa.docx
└── devops_engineer/
    ├── vaga.txt
    └── curriculos/
        ├── carlos_souza.pdf
        └── lucia_fernandes.docx

LÓGICA DE FUNCIONAMENTO:

1. DETECÇÃO ESTRUTURADA:
   - Escaneia automaticamente todas as pastas de vagas
   - Identifica arquivos de vaga (vaga.txt) e pasta de currículos
   - Processa apenas currículos relevantes para cada vaga

2. ANÁLISE DIRECIONADA:
   - Cada vaga analisa apenas seus currículos específicos
   - Evita análise cruzada desnecessária
   - Foco em compatibilidade real

3. RELATÓRIOS POR VAGA:
   - Gera relatório individual para cada vaga
   - Mostra ranking de currículos por pontuação
   - Recomendações específicas por candidato

4. INTEGRAÇÃO COM SISTEMA PRINCIPAL:
   - Compatível com sistema de email existente
   - Mantém estrutura de log unificada
   - Suporte a múltiplos formatos (PDF, DOCX, TXT)

VANTAGENS DA ESTRUTURA ORGANIZADA:
- ✅ Análise mais rápida e eficiente
- ✅ Resultados mais precisos e relevantes
- ✅ Melhor organização de currículos
- ✅ Fácil manutenção e atualização
- ✅ Escalabilidade para múltiplas vagas

DEPENDÊNCIAS:
- core.ats_analyzer: Para análise técnica ATS
- os, shutil: Para manipulação de arquivos e pastas
- pandas: Para relatórios estruturados

EXEMPLO DE USO:
organizer = ATSOrganizer()
organizer.executar_analise_organizada()
organizer.gerar_relatorios_por_vaga()

Autor: Cara Core Informática
Data: 2025
Licença: MIT
"""

import os
import shutil
import pandas as pd
from datetime import datetime
from core import ats_analyzer

class ATSOrganizer:
    """Classe principal para sistema organizado de análise ATS."""

    def __init__(self, pasta_base='vagas'):
        """Inicializa o organizador com a pasta base."""
        self.pasta_base = pasta_base
        self.resultados_por_vaga = {}
        self.relatorios = {}

    def detectar_estrutura_vagas(self):
        """Detecta todas as vagas e suas estruturas."""
        print("🔍 Detectando estrutura organizada de vagas...")

        if not os.path.exists(self.pasta_base):
            print(f"❌ Pasta base '{self.pasta_base}' não encontrada")
            return []

        vagas_encontradas = []

        for item in os.listdir(self.pasta_base):
            caminho_vaga = os.path.join(self.pasta_base, item)

            if os.path.isdir(caminho_vaga):
                # Verifica se tem arquivo de vaga
                arquivo_vaga = os.path.join(caminho_vaga, 'vaga.txt')
                pasta_curriculos = os.path.join(caminho_vaga, 'curriculos')

                if os.path.exists(arquivo_vaga) and os.path.exists(pasta_curriculos):
                    vagas_encontradas.append({
                        'nome': item,
                        'caminho': caminho_vaga,
                        'arquivo_vaga': arquivo_vaga,
                        'pasta_curriculos': pasta_curriculos
                    })
                    print(f"   ✅ Vaga detectada: {item}")
                else:
                    print(f"   ⚠️  Estrutura incompleta: {item}")

        print(f"\n📊 Total de vagas organizadas encontradas: {len(vagas_encontradas)}")
        return vagas_encontradas

    def analisar_vaga_organizada(self, vaga_info):
        """Analisa uma vaga específica com seus currículos."""
        nome_vaga = vaga_info['nome']
        arquivo_vaga = vaga_info['arquivo_vaga']
        pasta_curriculos = vaga_info['pasta_curriculos']

        print(f"\n🔍 Analisando vaga organizada: {nome_vaga}")
        print("=" * 60)

        # Carrega descrição da vaga
        try:
            with open(arquivo_vaga, 'r', encoding='utf-8') as f:
                texto_vaga = f.read()
        except Exception as e:
            print(f"❌ Erro ao carregar vaga {nome_vaga}: {e}")
            return None

        # Tokeniza a vaga
        tokens_vaga = ats_analyzer.tokenizar(texto_vaga)
        print(f"📊 Palavras-chave na vaga: {len(tokens_vaga)}")

        # Lista currículos da vaga
        arquivos_curriculos = [f for f in os.listdir(pasta_curriculos)
                              if f.lower().endswith(('.txt', '.docx', '.pdf'))]

        if not arquivos_curriculos:
            print(f"⚠️  Nenhum currículo encontrado para {nome_vaga}")
            return None

        print(f"📄 Currículos encontrados: {len(arquivos_curriculos)}")

        # Analisa cada currículo
        resultados_curriculos = []

        for curriculo_file in arquivos_curriculos:
            caminho_curriculo = os.path.join(pasta_curriculos, curriculo_file)
            nome_base = os.path.splitext(curriculo_file)[0]

            print(f"\n   👤 Analisando: {curriculo_file}")

            # Carrega e converte currículo se necessário
            texto_curriculo = ats_analyzer.carregar_arquivo(caminho_curriculo)
            if not texto_curriculo:
                continue

            tokens_curriculo = ats_analyzer.tokenizar(texto_curriculo)
            print(f"      📊 Palavras no currículo: {len(tokens_curriculo)}")

            # Calcula pontuação
            pontuacao, palavras_faltantes = ats_analyzer.analisar_compatibilidade(
                tokens_curriculo, tokens_vaga
            )

            print(f"      🎯 Pontuação ATS: {pontuacao}%")

            # Gera recomendações
            recomendacoes = ats_analyzer.gerar_recomendacoes(palavras_faltantes, pontuacao)

            # Armazena resultado
            resultado = {
                'curriculo': nome_base,
                'arquivo': curriculo_file,
                'caminho': caminho_curriculo,
                'pontuacao': pontuacao,
                'palavras_faltantes': palavras_faltantes,
                'recomendacoes': recomendacoes,
                'tokens_curriculo': len(tokens_curriculo),
                'tokens_vaga': len(tokens_vaga)
            }

            resultados_curriculos.append(resultado)

        # Ordena por pontuação (maior para menor)
        resultados_curriculos.sort(key=lambda x: x['pontuacao'], reverse=True)

        # Armazena resultados da vaga
        resultado_vaga = {
            'nome_vaga': nome_vaga,
            'tokens_vaga': len(tokens_vaga),
            'total_curriculos': len(resultados_curriculos),
            'curriculos': resultados_curriculos,
            'data_analise': datetime.now()
        }

        return resultado_vaga

    def executar_analise_organizada(self):
        """Executa análise completa do sistema organizado."""
        print("🚀 Iniciando análise organizada ATS")
        print("=" * 60)

        # Detecta estrutura
        vagas = self.detectar_estrutura_vagas()

        if not vagas:
            print("❌ Nenhuma vaga organizada encontrada")
            return False

        # Analisa cada vaga
        for vaga_info in vagas:
            resultado = self.analisar_vaga_organizada(vaga_info)
            if resultado:
                self.resultados_por_vaga[vaga_info['nome']] = resultado

        print("\n" + "=" * 60)
        print("✅ Análise organizada concluída!")
        return True

    def gerar_relatorio_vaga(self, nome_vaga, resultado_vaga):
        """Gera relatório detalhado para uma vaga específica."""
        print(f"\n📊 RELATÓRIO DA VAGA: {nome_vaga}")
        print("=" * 60)

        print(f"📈 Estatísticas Gerais:")
        print(f"   • Total de currículos analisados: {resultado_vaga['total_curriculos']}")
        print(f"   • Palavras-chave na vaga: {resultado_vaga['tokens_vaga']}")
        print(f"   • Data da análise: {resultado_vaga['data_analise'].strftime('%d/%m/%Y %H:%M')}")

        if resultado_vaga['curriculos']:
            print(f"\n🏆 RANKING DE CURRÍCULOS:")

            for i, curriculo in enumerate(resultado_vaga['curriculos'], 1):
                status = "✅ APROVADO" if curriculo['pontuacao'] >= 70 else "❌ REPROVADO"
                print(f"\n   {i}º LUGAR - {curriculo['curriculo']}")
                print(f"      Pontuação ATS: {curriculo['pontuacao']}% - {status}")
                print(f"      Arquivo: {curriculo['arquivo']}")
                print(f"      Palavras no currículo: {curriculo['tokens_curriculo']}")

                if curriculo['recomendacoes']:
                    print("      💡 Recomendações:")
                    for rec in curriculo['recomendacoes']:
                        print(f"         • {rec}")

        # Estatísticas de aprovação
        aprovados = len([c for c in resultado_vaga['curriculos'] if c['pontuacao'] >= 70])
        reprovados = resultado_vaga['total_curriculos'] - aprovados

        print(f"\n📊 RESUMO DA VAGA:")
        print(f"   ✅ Aprovados (≥70%): {aprovados}")
        print(f"   ❌ Reprovados (<70%): {reprovados}")
        if resultado_vaga['total_curriculos'] > 0:
            taxa_aprovacao = (aprovados / resultado_vaga['total_curriculos']) * 100
            print(f"   📈 Taxa de aprovação: {taxa_aprovacao:.1f}%")

    def gerar_relatorios_por_vaga(self):
        """Gera relatórios para todas as vagas analisadas."""
        print("\n📋 GERANDO RELATÓRIOS POR VAGA")
        print("=" * 60)

        if not self.resultados_por_vaga:
            print("❌ Nenhum resultado para gerar relatório")
            return

        for nome_vaga, resultado in self.resultados_por_vaga.items():
            self.gerar_relatorio_vaga(nome_vaga, resultado)

        # Relatório geral
        self.gerar_relatorio_geral()

    def gerar_relatorio_geral(self):
        """Gera relatório geral de todas as vagas."""
        print(f"\n🌟 RELATÓRIO GERAL - SISTEMA ORGANIZADO")
        print("=" * 60)

        total_vagas = len(self.resultados_por_vaga)
        total_curriculos = sum(r['total_curriculos'] for r in self.resultados_por_vaga.values())
        total_aprovados = 0

        for resultado in self.resultados_por_vaga.values():
            total_aprovados += len([c for c in resultado['curriculos'] if c['pontuacao'] >= 70])

        print(f"📊 Estatísticas Gerais:")
        print(f"   • Total de vagas analisadas: {total_vagas}")
        print(f"   • Total de currículos processados: {total_curriculos}")
        print(f"   • Total de aprovações: {total_aprovados}")

        if total_curriculos > 0:
            taxa_geral = (total_aprovados / total_curriculos) * 100
            print(f"   • Taxa de aprovação geral: {taxa_geral:.1f}%")

        print(f"\n🏆 VAGAS ANALISADAS:")
        for nome_vaga, resultado in self.resultados_por_vaga.items():
            aprovados_vaga = len([c for c in resultado['curriculos'] if c['pontuacao'] >= 70])
            print(f"   • {nome_vaga}: {resultado['total_curriculos']} currículos, {aprovados_vaga} aprovados")

    def exportar_resultados_csv(self, arquivo_saida='log/resultados_ats_organizado.csv'):
        """Exporta todos os resultados para CSV."""
        print(f"\n💾 Exportando resultados para {arquivo_saida}...")

        dados_exportacao = []

        for nome_vaga, resultado in self.resultados_por_vaga.items():
            for curriculo in resultado['curriculos']:
                dados_exportacao.append({
                    'vaga': nome_vaga,
                    'curriculo': curriculo['curriculo'],
                    'arquivo': curriculo['arquivo'],
                    'pontuacao_ats': curriculo['pontuacao'],
                    'aprovado': 'Sim' if curriculo['pontuacao'] >= 70 else 'Não',
                    'palavras_curriculo': curriculo['tokens_curriculo'],
                    'palavras_vaga': curriculo['tokens_vaga'],
                    'data_analise': resultado['data_analise']
                })

        if dados_exportacao:
            df = pd.DataFrame(dados_exportacao)
            df.to_csv(arquivo_saida, index=False, encoding='utf-8')
            print(f"✅ Resultados exportados com sucesso: {len(dados_exportacao)} registros")
        else:
            print("❌ Nenhum dado para exportar")

    def criar_exemplo_estrutura(self):
        """Cria estrutura de exemplo para demonstração."""
        print("🏗️  Criando estrutura de exemplo...")

        # Cria pastas de exemplo
        exemplos = [
            'vagas/desenvolvedor_frontend/curriculos',
            'vagas/desenvolvedor_fullstack/curriculos',
            'vagas/engenheiro_software/curriculos'
        ]

        for exemplo in exemplos:
            os.makedirs(exemplo, exist_ok=True)

        # Cria arquivo de vaga de exemplo
        vaga_exemplo = """DESENVOLVEDOR FRONTEND SÊNIOR

Empresa: TechCorp
Local: São Paulo, SP
Tipo: CLT - Tempo Integral

DESCRIÇÃO DA VAGA:
Procuramos Desenvolvedor Frontend experiente para integrar nossa equipe.

REQUISITOS TÉCNICOS:
• React.js avançado (2+ anos)
• JavaScript/TypeScript
• HTML5, CSS3, SASS
• Git e controle de versão
• Metodologias ágeis
• Testes automatizados

DIFERENCIAIS:
• Next.js
• Vue.js
• GraphQL
• Docker
• AWS

OFERECEMOS:
• Salário competitivo
• Vale refeição
• Plano de saúde
• Home office
• Crescimento profissional"""

        with open('vagas/desenvolvedor_frontend/vaga.txt', 'w', encoding='utf-8') as f:
            f.write(vaga_exemplo)

        print("✅ Estrutura de exemplo criada!")
        print("💡 Adicione currículos na pasta curriculos/ de cada vaga")

def main():
    """Função principal do organizador ATS."""
    organizer = ATSOrganizer()

    # Executa análise organizada
    if organizer.executar_analise_organizada():
        # Gera relatórios
        organizer.gerar_relatorios_por_vaga()

        # Exporta resultados
        organizer.exportar_resultados_csv()

    print("\n" + "=" * 60)
    print("🎯 Sistema organizado concluído!")
    print("💡 Use a estrutura de pastas para melhor organização")

if __name__ == "__main__":
    main()
