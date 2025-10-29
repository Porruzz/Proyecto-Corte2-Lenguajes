# -*- coding: utf-8 -*-
"""
Utilidades de salida para el modo léxico.
"""
from typing import List, Tuple

Token = Tuple[str, str, int, int]

def print_tokens(tokens: List[Token]) -> None:
    for ttype, lex, line, col in tokens:
        if ttype in {"identificador", "tk_entero", "tk_cadena"}:
            print(f"<{ttype}, {lex}, {line}, {col}>")
        else:
            # Reservadas o símbolos (ya traen nombre estándar)
            if ttype.startswith("tk_"):
                print(f"<{ttype}, {line}, {col}>")
            else:
                # reservadas: tipo = lexema
                print(f"<{ttype}, {line}, {col}>")
