# -*- coding: utf-8 -*-
"""
grammar_io.py
-------------
Carga una gramática LL(1) desde un archivo de texto con el formato:

  NoTerminal -> simbolo simbolo ... | simbolo ... | ε

- Separador de producciones: '|'
- El símbolo de vacío es: ε
- Se asume que la primera línea define el símbolo inicial.
- Se ignoran líneas vacías y comentarios que comiencen con '#'.

La gramática se devuelve como:
- start: str
- G: dict[str, list[list[str]]], donde cada NoTerminal (clave) mapea a una lista
     de producciones; cada producción es una lista de símbolos (termin.) o 'ε'.
"""
from typing import Dict, List, Tuple

EPS = "ε"

def load_grammar(path: str) -> Tuple[str, Dict[str, List[List[str]]]]:
    G: Dict[str, List[List[str]]] = {}
    start: str | None = None

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            # Normalizar separador: aceptar ->, →, ::=
            if "->" not in line and "→" in line:
                line = line.replace("→", "->")
            if "->" not in line and "::=" in line:
                line = line.replace("::=", "->")

            if "->" not in line:
                raise ValueError(f"Gramática: línea inválida (falta '->'): {line}")

            lhs, rhs = [x.strip() for x in line.split("->", 1)]
            if start is None:
                start = lhs
            alts = [alt.strip() for alt in rhs.split("|")]
            prods: List[List[str]] = []
            for alt in alts:
                if alt == EPS:
                    prods.append([EPS])
                else:
                    prods.append(alt.split())
            G.setdefault(lhs, []).extend(prods)

    if start is None or not G:
        raise ValueError("Gramática vacía o sin producciones válidas.")
    return start, G

