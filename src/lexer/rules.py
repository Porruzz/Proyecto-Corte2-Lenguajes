# -*- coding: utf-8 -*-
"""
Reglas de reconocimiento (longest-match) para el analizador léxico.
Separamos la lógica de "qué es un identificador/entero/cadena" de la
mecánica de escaneo para testear más fácil.
"""
import string

LETRAS = string.ascii_letters + "_"
LETRAS_DIGITOS = string.ascii_letters + string.digits + "_"
DIGITOS = string.digits

def match_identifier(src: str, i: int) -> int:
    """Si en src[i] comienza un identificador, retorna el índice final exclusivo.
       Si no, retorna i (sin consumir)."""
    if i < len(src) and src[i] in LETRAS:
        j = i + 1
        while j < len(src) and src[j] in LETRAS_DIGITOS:
            j += 1
        return j
    return i

def match_integer(src: str, i: int) -> int:
    """Enteros con signo opcional: [+-]?[0-9]+
       Nota: el signo se reconoce como parte del número solo si hay dígitos después."""
    if i >= len(src):
        return i
    j = i
    # signo opcional
    if src[j] in "+-":
        if j + 1 < len(src) and src[j+1] in DIGITOS:
            j += 1
        else:
            return i  # '+' o '-' solo no es número
    # dígitos obligatorios
    if j < len(src) and src[j] in DIGITOS:
        j += 1
        while j < len(src) and src[j] in DIGITOS:
            j += 1
        return j
    return i

def match_string(src: str, i: int) -> int:
    """Cadenas con comillas simples o dobles. No se manejan escapes complejos (versión simple).
       Retorna índice final exclusivo si hay cierre; si no hay cierre, retorna i (sin consumir)."""
    if i >= len(src) or src[i] not in {'"', "'"}:
        return i
    quote = src[i]
    j = i + 1
    while j < len(src) and src[j] != quote:
        # versión simple: no consideramos escapes
        if src[j] == "\n":
            # no cerrada antes de salto de línea: consideramos error en otra capa
            return i
        j += 1
    if j < len(src) and src[j] == quote:
        return j + 1  # consume la comilla de cierre
    return i  # sin cierre
