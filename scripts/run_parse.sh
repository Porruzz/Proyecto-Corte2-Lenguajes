#!/bin/bash
# ------------------------------------------------------------
# Script: run_parse.sh
# Descripción:
# Corre el analizador sintáctico LL(1) sobre los ejemplos válidos e inválidos.
# ------------------------------------------------------------

GRAMMAR="grammars/python_subset.g"

echo "== Pruebas de Parsing =="
for FILE in examples/python/ok/*.py; do
  echo "[OK] Probando $FILE"
  python -m src.main --mode parse --grammar "$GRAMMAR" --input "$FILE"
done

for FILE in examples/python/bad/*.py; do
  echo "[BAD] Probando $FILE"
  python -m src.main --mode parse --grammar "$GRAMMAR" --input "$FILE"
done
