# -*- coding: utf-8 -*-
"""
Scanner/tokenizer del subconjunto de Python.
- Implementa longest-match para operadores de 2 y 1 carácter
- Usa rules.py para identificadores, enteros y cadenas
- Reporta posición (línea, columna) 1-indexed
- En error léxico: lanza ValueError("Error léxico(linea:X,posicion:Y)")
"""
from typing import List, Tuple
from .token_defs import RESERVED, TOKENS, WHITESPACE, NEWLINE, COMMENT_START
from .rules import match_identifier, match_integer, match_string

Token = Tuple[str, str, int, int]  # (tipo, lexema, linea, col)

def _two_char_ops_starting() -> set:
    """Conjunto de primeros caracteres de operadores de 2 símbolos (para optimizar)."""
    return {op[0] for op in TOKENS.keys() if len(op) == 2}

FIRST2 = _two_char_ops_starting()

def tokenize(src: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    line = 1
    col = 1
    n = len(src)

    def advance(ch: str):
        nonlocal line, col
        if ch in NEWLINE:
            line += 1
            col = 1
        else:
            col += 1

    while i < n:
        ch = src[i]

        # Saltar espacios y tabs
        if ch in WHITESPACE:
            advance(ch)
            i += 1
            continue

        # Saltar comentarios hasta fin de línea
        if ch == COMMENT_START:
            # consumir hasta \n o fin
            while i < n and src[i] not in NEWLINE:
                advance(src[i])
                i += 1
            continue

        # Nueva línea
        if ch in NEWLINE:
            advance(ch)
            i += 1
            continue

        start_line, start_col = line, col

        # Longest-match para operadores de dos caracteres
        if ch in FIRST2 and i + 1 < n:
            op2 = src[i:i+2]
            if op2 in TOKENS:
                tok_type = TOKENS[op2]
                tokens.append((tok_type, op2, start_line, start_col))
                # avanzar 2
                advance(op2[0]); advance(op2[1])
                i += 2
                continue

        # Operadores/símbolos de un caracter
        if ch in TOKENS:
            tok_type = TOKENS[ch]
            tokens.append((tok_type, ch, start_line, start_col))
            advance(ch)
            i += 1
            continue

        # Identificador o palabra reservada
        j = match_identifier(src, i)
        if j > i:
            lex = src[i:j]
            if lex in RESERVED:
                # Palabra reservada: se reporta por su lexema como tipo
                tokens.append((lex, lex, start_line, start_col))
            else:
                tokens.append(("identificador", lex, start_line, start_col))
            # avanzar
            for k in range(i, j):
                advance(src[k])
            i = j
            continue

        # Entero (con signo si aplica)
        j = match_integer(src, i)
        if j > i:
            lex = src[i:j]
            tokens.append(("tk_entero", lex, start_line, start_col))
            for k in range(i, j):
                advance(src[k])
            i = j
            continue

        # Cadena "..." o '...'
        j = match_string(src, i)
        if j > i:
            lex = src[i:j]
            tokens.append(("tk_cadena", lex, start_line, start_col))
            for k in range(i, j):
                advance(src[k])
            i = j
            continue

        # Si llegamos aquí, es un carácter inválido para este subconjunto
        raise ValueError(f"Error léxico(linea:{start_line},posicion:{start_col})")

    return tokens
