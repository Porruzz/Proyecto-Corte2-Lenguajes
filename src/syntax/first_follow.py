# -*- coding: utf-8 -*-
"""
first_follow.py
---------------
Cálculo de conjuntos FIRST y FOLLOW para una gramática.
- FIRST(X): terminales que pueden iniciar derivaciones desde X (incluye ε si X =>* ε)
- FOLLOW(A): terminales que pueden aparecer inmediatamente a la derecha de A en alguna derivación; $ en FOLLOW(S)

Implementa las reglas estándar (Presentación 6).
"""
from typing import Dict, List, Set, Tuple
from .grammar_io import EPS

def is_terminal(sym: str, G: Dict[str, List[List[str]]]) -> bool:
    """Un símbolo es terminal si NO es un no-terminal definido en la gramática."""
    return sym not in G

def compute_first_sets(G: Dict[str, List[List[str]]]) -> Dict[str, Set[str]]:
    FIRST: Dict[str, Set[str]] = {}

    # Inicializar FIRST para terminals y non-terminals
    for A, prods in G.items():
        FIRST.setdefault(A, set())
        for rhs in prods:
            for a in rhs:
                if is_terminal(a, G):
                    FIRST.setdefault(a, set()).add(a)

    # Cierre iterativo
    changed = True
    while changed:
        changed = False
        for A, prods in G.items():
            for rhs in prods:
                # FIRST(alpha) para alpha=rhs
                nullable_prefix = True
                for a in rhs:
                    # agrega FIRST(a)\{ε}
                    add = set(FIRST.get(a, set()))
                    if EPS in add:
                        add.discard(EPS)
                    if not add.issubset(FIRST[A]):
                        FIRST[A] |= add
                        changed = True
                    # si a NO es anulable, detenemos
                    if EPS not in FIRST.get(a, set()):
                        nullable_prefix = False
                        break
                if nullable_prefix:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
    return FIRST

def first_of_sequence(seq: List[str], FIRST: Dict[str, Set[str]], G: Dict[str, List[List[str]]]) -> Set[str]:
    """FIRST de una secuencia de símbolos (incluye ε si toda la secuencia es anulable)."""
    out: Set[str] = set()
    nullable_prefix = True
    for s in seq:
        sfirst = set(FIRST.get(s, set()))
        if EPS in sfirst:
            sfirst.discard(EPS)
            out |= sfirst
        else:
            out |= sfirst
            nullable_prefix = False
            break
    if nullable_prefix:
        out.add(EPS)
    return out

def compute_follow_sets(start: str, G: Dict[str, List[List[str]]], FIRST: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    FOLLOW: Dict[str, Set[str]] = {A: set() for A in G}
    FOLLOW[start].add("$")  # $ en el inicial

    changed = True
    while changed:
        changed = False
        for A, prods in G.items():
            for rhs in prods:
                # Recorremos B en A -> α B β
                for i, B in enumerate(rhs):
                    if B not in G:
                        continue
                    beta = rhs[i+1:]
                    if beta:
                        fb = first_of_sequence(beta, FIRST, G)
                        # (FIRST(beta) - {ε}) ⊆ FOLLOW(B)
                        moved = fb - {EPS}
                        if not moved.issubset(FOLLOW[B]):
                            FOLLOW[B] |= moved
                            changed = True
                        # si beta =>* ε, FOLLOW(A) ⊆ FOLLOW(B)
                        if EPS in fb and not FOLLOW[A].issubset(FOLLOW[B]):
                            FOLLOW[B] |= FOLLOW[A]
                            changed = True
                    else:
                        # B al final: FOLLOW(A) ⊆ FOLLOW(B)
                        if not FOLLOW[A].issubset(FOLLOW[B]):
                            FOLLOW[B] |= FOLLOW[A]
                            changed = True
    return FOLLOW
