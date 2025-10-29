#!/bin/bash
# ------------------------------------------------------------
# Script: run_lex.sh
# Descripción:
# Ejecuta el analizador léxico con una entrada .py y muestra tokens.
# ------------------------------------------------------------

INPUT=${1:-examples/python/ok/mini.py}
echo "== Analizador Léxico =="
python -m src.main --mode lex --input "$INPUT"
