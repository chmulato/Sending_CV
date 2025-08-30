#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criador de Vaga Organizada - Script auxiliar para criar novas vagas
====================================================================

Este script ajuda a criar uma nova vaga na estrutura organizada do sistema ATS.

USO:
        print("  python core/criar_vaga_organizada.py 'Nome da Vaga' [empresa] [local]")

EXEMPLO:
python core/criar_vaga_organizada.py "Desenvolvedor FullStack" "TechCorp" "São Paulo"
"""

import os
import sys
from datetime import datetime

def criar_vaga_organizada(nome_vaga, empresa="Empresa Exemplo", local="São Paulo, SP"):
    """Cria uma nova vaga na estrutura organizada."""

    # Normalizar nome da vaga para usar como pasta
    nome_pasta = nome_vaga.lower().replace(" ", "_").replace("/", "_")

    # Caminhos
    caminho_vaga = os.path.join("vagas", nome_pasta)
    caminho_curriculos = os.path.join(caminho_vaga, "curriculos")
    arquivo_vaga = os.path.join(caminho_vaga, "vaga.txt")

    print(f"🏗️  Criando vaga organizada: {nome_vaga}")
    print(f"📁 Pasta: {nome_pasta}")

    # Criar pastas
    os.makedirs(caminho_curriculos, exist_ok=True)

    # Template da descrição da vaga
    template_vaga = f"""{nome_vaga.upper()}

Empresa: {empresa}
Local: {local}
Tipo: CLT - Tempo Integral
Data de Criação: {datetime.now().strftime('%d/%m/%Y')}

DESCRIÇÃO DA VAGA:
Procuramos profissional experiente para integrar nossa equipe, contribuindo
com projetos inovadores e desafiadores.

RESPONSABILIDADES:
• Desenvolver e manter aplicações de alta qualidade
• Participar do design e arquitetura de sistemas
• Colaborar com equipe multidisciplinar
• Implementar melhores práticas de desenvolvimento
• Contribuir para a cultura de inovação

REQUISITOS TÉCNICOS:
• Experiência sólida na área ({nome_vaga})
• Conhecimento em metodologias ágeis
• Controle de versão (Git)
• Trabalho em equipe
• Comunicação eficaz

DIFERENCIAIS:
• Experiência em projetos similares
• Conhecimento em cloud computing
• Certificações relevantes
• Inglês avançado
• Participação em comunidades técnicas

OFERECEMOS:
• Salário competitivo
• Plano de saúde e odontológico
• Vale refeição/alimentação
• Auxílio home office
• Ambiente de trabalho colaborativo
• Oportunidades de crescimento profissional

PALAVRAS-CHAVE ATS:
{nome_pasta.replace('_', ' ')} desenvolvimento projeto equipe agil git cloud certificacao"""

    # Criar arquivo de vaga
    with open(arquivo_vaga, 'w', encoding='utf-8') as f:
        f.write(template_vaga)

    print("✅ Vaga criada com sucesso!")
    print(f"📄 Arquivo: {arquivo_vaga}")
    print(f"📁 Currículos: {caminho_curriculos}")
    print("\n📝 PRÓXIMOS PASSOS:")
    print("1. Edite o arquivo vaga.txt com os detalhes específicos")
    print("2. Adicione currículos relevantes na pasta curriculos/")
    print("3. Execute: python main.py organizado")
    print("\n💡 DICAS PARA OTIMIZAÇÃO:")
    print("- Use palavras-chave técnicas relevantes na seção PALAVRAS-CHAVE ATS")
    print("- Seja específico nos requisitos técnicos")
    print("- Inclua informações sobre benefícios e cultura da empresa")
    print("- Mantenha o formato ATS-friendly")

def listar_vagas_organizadas():
    """Lista todas as vagas organizadas existentes."""
    print("\n📋 VAGAS ORGANIZADAS EXISTENTES:")
    print("=" * 50)

    if not os.path.exists("vagas"):
        print("❌ Pasta vagas não encontrada")
        return

    vagas_encontradas = 0

    for item in os.listdir("vagas"):
        caminho_vaga = os.path.join("vagas", item)

        if os.path.isdir(caminho_vaga):
            arquivo_vaga = os.path.join(caminho_vaga, "vaga.txt")
            pasta_curriculos = os.path.join(caminho_vaga, "curriculos")

            if os.path.exists(arquivo_vaga) and os.path.exists(pasta_curriculos):
                # Contar currículos
                curriculos = [f for f in os.listdir(pasta_curriculos)
                            if f.lower().endswith(('.txt', '.docx', '.pdf'))]

                print(f"✅ {item}")
                print(f"   📄 Vaga: {arquivo_vaga}")
                print(f"   📁 Currículos: {len(curriculos)} arquivo(s)")
                vagas_encontradas += 1
            else:
                print(f"⚠️  {item} (estrutura incompleta)")

    if vagas_encontradas == 0:
        print("Nenhuma vaga organizada encontrada")
        print("💡 Use: python core/criar_vaga_organizada.py 'Nome da Vaga'")
    else:
        print(f"\n📊 Total: {vagas_encontradas} vaga(s) organizada(s)")

def main():
    """Função principal."""
    print("🏗️  Criador de Vaga Organizada")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("❌ Uso incorreto!")
        print("\n📖 COMANDOS DISPONÍVEIS:")
        print("  python core/criar_vaga_organizada.py 'Nome da Vaga' [empresa] [local]")
        print("  python core/criar_vaga_organizada.py --listar")
        print("\n📝 EXEMPLOS:")
        print("  python core/criar_vaga_organizada.py 'Desenvolvedor FullStack'")
        print("  python core/criar_vaga_organizada.py 'Analista de Dados' 'TechCorp' 'Rio de Janeiro'")
        print("  python core/criar_vaga_organizada.py --listar")
        return

    comando = sys.argv[1]

    if comando == "--listar":
        listar_vagas_organizadas()
        return

    # Criar nova vaga
    nome_vaga = comando
    empresa = sys.argv[2] if len(sys.argv) > 2 else "Empresa Exemplo"
    local = sys.argv[3] if len(sys.argv) > 3 else "São Paulo, SP"

    criar_vaga_organizada(nome_vaga, empresa, local)

if __name__ == "__main__":
    main()
