# -*- coding: utf-8 -*-
"""
table.py
--------
Construcción de la tabla LL(1):
  M[A, a] = producción (A→α) para todo a ∈ PREDICT(A→α)

Detecta conflictos si una celda recibe más de una producción.
"""
from typing import Dict, List, Set, Tuple

def build_ll1_table(
    predict: Dict[Tuple[str, tuple], Set[str]]
) -> Dict[Tuple[str, str], List[str]]:
    table: Dict[Tuple[str, str], List[str]] = {}
    for (A, rhs), terms in predict.items():
        prod_str = " ".join(rhs)
        for a in terms:
            key = (A, a)
            table.setdefault(key, []).append(prod_str)
    return table

def has_conflicts(table: Dict[Tuple[str, str], List[str]]) -> int:
    """Devuelve el número de celdas con múltiples producciones (conflictos)."""
    return sum(1 for v in table.values() if len(v) > 1)
