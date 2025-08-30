#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor de Arquivos Markdown para DOCX
========================================

Este script converte arquivos .md para .docx usando Pandoc.

Uso: python converter_md_docx.py
"""

import os
import subprocess

def convert_md_to_docx(md_file, docx_file):
    """Converte arquivo .md para .docx usando Pandoc."""
    try:
        subprocess.run(['pandoc', md_file, '-o', docx_file], check=True)
        print(f"✅ Convertido: {md_file} -> {docx_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao converter {md_file}: {e}")
        return False
    except FileNotFoundError:
        print("❌ Pandoc não encontrado. Instale o Pandoc primeiro.")
        return False

def main():
    print("🔄 Conversor MD para DOCX")
    print("=" * 30)

    # Pasta de currículos
    curriculos_dir = 'curriculos'

    if not os.path.exists(curriculos_dir):
        print(f"❌ Pasta {curriculos_dir} não encontrada!")
        return

    # Procurar arquivos .md
    md_files = [f for f in os.listdir(curriculos_dir) if f.endswith('.md')]

    if not md_files:
        print("❌ Nenhum arquivo .md encontrado na pasta curriculos!")
        return

    print(f"Encontrados {len(md_files)} arquivo(s) .md:")
    for md_file in md_files:
        print(f"  - {md_file}")

    print("\nIniciando conversão...")

    converted = 0
    for md_file in md_files:
        md_path = os.path.join(curriculos_dir, md_file)
        docx_file = md_file.replace('.md', '.docx')
        docx_path = os.path.join(curriculos_dir, docx_file)

        if convert_md_to_docx(md_path, docx_path):
            converted += 1

    print(f"\n✅ Conversão concluída! {converted} arquivo(s) convertido(s).")

if __name__ == "__main__":
    main()
