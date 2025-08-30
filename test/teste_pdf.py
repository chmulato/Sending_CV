#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Conversão PDF para TXT
==============================

Este script testa a conversão de PDF para TXT usando pdfplumber.

Uso: python teste_pdf.py
"""

import os
import pdfplumber

def test_pdf_conversion(pdf_file):
    """Testa conversão de PDF para texto."""
    try:
        text = []
        with pdfplumber.open(pdf_file) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text.append(f"=== Página {i+1} ===\n{page_text}")
                else:
                    print(f"Aviso: Página {i+1} não contém texto extraível")

        full_text = '\n\n'.join(text)
        print("✅ PDF convertido com sucesso!")
        print(f"Total de páginas processadas: {len(pdf.pages)}")
        print(f"Total de caracteres extraídos: {len(full_text)}")
        print("\n=== Preview do texto extraído ===")
        print(full_text[:500] + "..." if len(full_text) > 500 else full_text)

        return full_text

    except Exception as e:
        print(f"❌ Erro ao processar PDF: {e}")
        return None

def main():
    print("🧪 Teste de Conversão PDF")
    print("=" * 30)

    # Procurar arquivos PDF na pasta curriculos
    curriculos_dir = 'curriculos'
    pdf_files = [f for f in os.listdir(curriculos_dir) if f.endswith('.pdf')]

    if not pdf_files:
        print("❌ Nenhum arquivo PDF encontrado em curriculos/")
        print("💡 Coloque um arquivo .pdf na pasta curriculos/ para testar")
        return

    print(f"Encontrados {len(pdf_files)} arquivo(s) PDF:")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file}")

    print("\nTestando conversão...")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(curriculos_dir, pdf_file)
        print(f"\n📄 Testando: {pdf_file}")
        test_pdf_conversion(pdf_path)

if __name__ == "__main__":
    main()
