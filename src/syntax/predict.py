# -*- coding: utf-8 -*-
"""
predict.py
----------
Cálculo de conjuntos de PREDICCIÓN por producción:
  PREDICT(A→α) = (FIRST(α) - {ε}) ∪ (FOLLOW(A) si ε ∈ FIRST(α))
"""
from typing import Dict, List, Set, Tuple
from .grammar_io import EPS
from .first_follow import first_of_sequence

def compute_predict_sets(
    start: str,
    G: Dict[str, List[List[str]]],
    FIRST: Dict[str, Set[str]],
    FOLLOW: Dict[str, Set[str]],
) -> Dict[Tuple[str, tuple], Set[str]]:
    predict: Dict[Tuple[str, tuple], Set[str]] = {}
    for A, prods in G.items():
        for rhs in prods:
            key = (A, tuple(rhs))
            fa = first_of_sequence(rhs, FIRST, G)
            s = set(fa)
            if EPS in s:
                s.discard(EPS)
                s |= FOLLOW[A]
            predict[key] = s
    return predict
