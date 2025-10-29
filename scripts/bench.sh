#!/bin/bash
# ------------------------------------------------------------
# Script: bench.sh
# Descripción:
# Ejecuta pruebas de rendimiento sobre el analizador LL(1)
# usando diferentes entradas del proyecto.
# ------------------------------------------------------------

GRAMMAR="grammars/ejemplo_p6.g"
INPUTS=("examples/python/ok/expresion1.txt" "examples/python/ok/expresion2.txt")

echo "== Benchmark de Analizador LL(1) =="
for INPUT in "${INPUTS[@]}"; do
  echo "Probando con: $INPUT"
  /usr/bin/time -f "Tiempo total: %E (%S cpu)" python -m src.main \
    --mode parse \
    --grammar "$GRAMMAR" \
    --input "$INPUT" \
    > /dev/null
done
