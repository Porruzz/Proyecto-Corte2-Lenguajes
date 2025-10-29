# -*- coding: utf-8 -*-
"""
parser_ll1.py
-------------
Parser predictivo LL(1) con pila.

Entrada:
- start: símbolo inicial
- G: gramática
- table: tabla LL(1)  (M[A,a] -> producción como texto "X Y Z" o "ε")
- tokens: lista de tuplas (ttype, lex, line, col) producidas por el lexer

Adaptación de tokens -> terminales de la gramática:
- Si el terminal del grammar es un literal como '+','*','(',')', se compara con el lexema del token.
- Si el terminal es 'id', se acepta token tipo 'identificador'.
- Si el terminal es 'NUM', se acepta token tipo 'tk_entero'.
- Si el terminal coincide con una palabra reservada (p.ej. 'print'), el lexer entrega tipo == 'print'.
- Para otras coincidencias, probamos por tipo y por lexema de forma directa.

Salida:
- True si acepta; sino, False y un mensaje de error formateado.
"""
from typing import Dict, List, Tuple
from .grammar_io import EPS

Token = Tuple[str, str, int, int]  # (tipo, lexema, linea, col)

def token_to_symbol(term: str, tok: Token) -> bool:
    """Regla de equivalencia terminal-del-grammar vs token del lexer."""
    ttype, lex, *_ = tok

    # Lógicos por nombre común
    if term == "id" and ttype == "identificador":
        return True
    if term == "NUM" and ttype == "tk_entero":
        return True

    # Símbolos de 1 o 2 chars: comparamos con el lexema literal del archivo
    if term in {"+", "-", "*", "/", "(", ")", "[", "]", "{", "}", ",", ".", ":", ";", "==", "!=", "<=", ">=", "<", ">", "="}:
        return lex == term

    # Palabras reservadas: el tipo del token es el propio lexema (p.ej. 'print', 'if', 'def')
    if term == ttype == lex:
        return True

    # Igualdad directa por tipo
    if term == ttype:
        return True

    # Igualdad directa por lexema (fallback conservador)
    if term == lex:
        return True

    return False

def format_expected_from_row(table, A: str) -> List[str]:
    """Devuelve los terminales válidos (columnas) para el no-terminal A (útil en mensajes de error)."""
    cols = []
    for (nt, a), _ in table.items():
        if nt == A:
            cols.append(a)
    # ordenar para mensaje estable
    return sorted(set(cols))

def parse_ll1(start: str, G, table, tokens: List[Token], show_derivations: bool = False) -> Tuple[bool, str]:
    """Parser predictivo con pila. Retorna (ok, mensaje)."""
    # Pila inicial: S, $
    stack: List[str] = ["$", start]
    # flujo de entrada: tokens normal + $ marcador
    input_tokens = list(tokens) + [("EOF", "$", tokens[-1][2] if tokens else 1, tokens[-1][3] if tokens else 1)]

    i = 0
    deriv_steps: List[str] = []

    while stack:
        X = stack.pop()
        ttype, lex, line, col = input_tokens[i]

        if X == "$":
            if lex == "$":
                return True, "El analisis sintactico ha finalizado exitosamente."
            else:
                return False, f"<{line},{col}> Error sintactico: se encontro: \"{lex}\"; se esperaba fin de entrada"

        # X es terminal
        if X not in G and X != EPS:
            if token_to_symbol(X, input_tokens[i]):
                i += 1  # consumir
                continue
            else:
                return False, f"<{line},{col}> Error sintactico: se encontro: \"{lex}\"; se esperaba: \"{X}\""

        # X es no-terminal
        a = lex  # símbolo “visible” (usamos lex como columna; token_to_symbol hará el mapeo)
        # buscamos alguna columna “a” que sea compatible con el token actual:
        # Recorremos todas las columnas de X y probamos si alguna coincide con el token actual
        chosen_prod: List[str] | None = None

        # Caso rápido: si existe una columna exactamente con 'lex'
        if (X, a) in table:
            # Puede haber varias por conflictos; elegimos la primera
            chosen_prod = table[(X, a)][0].split()
        else:
            # Plan B: probar todas las columnas válidas de X y usar token_to_symbol
            for (nt, colterm), prods in table.items():
                if nt != X:
                    continue
                if token_to_symbol(colterm, input_tokens[i]):
                    chosen_prod = prods[0].split()
                    break

        if chosen_prod is None:
            # Sin entrada en la tabla LL(1) -> error con esperado
            esperados = format_expected_from_row(table, X)
            esperados_str = "\", \"".join(esperados) if esperados else "—"
            return False, f"<{line},{col}> Error sintactico: se encontro: \"{lex}\"; se esperaba: \"{esperados_str}\""

        # Aplicar producción
        if show_derivations:
            deriv_steps.append(f"{X} -> {' '.join(chosen_prod)}")

        if chosen_prod == [EPS]:
            # no apila nada
            continue

        # apilar RHS en orden inverso
        for sym in reversed(chosen_prod):
            stack.append(sym)

    # Si salimos sin devolver ok: error genérico
    last = input_tokens[i] if i < len(input_tokens) else ("EOF", "$", 1, 1)
    return False, f"<{last[2]},{last[3]}> Error sintactico: entrada no consumida"
