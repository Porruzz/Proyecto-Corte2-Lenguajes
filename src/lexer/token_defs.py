# -*- coding: utf-8 -*-
"""
Definiciones de tokens para el analizador léxico (subconjunto de Python).
- Palabras reservadas (se reportan por su lexema: <if, linea, col>)
- Tokens simbólicos (operadores y signos de puntuación)
- Categorías léxicas: identificadores, enteros y cadenas
Formato de salida sugerido:
  - Reservada:            <if, linea, col>
  - Identificador:        <identificador, nombre, linea, col>
  - Entero:               <tk_entero, 123, linea, col>
  - Cadena:               <tk_cadena, "hola", linea, col>
  - Símbolo/operador:     <tk_suma, linea, col>   (para +)
"""

# Palabras reservadas del subconjunto (puedes ajustar)
RESERVED = {
    "if", "else", "while", "for", "def", "return", "print",
    "and", "or", "not", "True", "False", "None"
}

# Mapa de lexema -> nombre de token para símbolos/operadores (longest-match)
TOKENS = {
    # Operadores de dos caracteres (deben evaluarse primero)
    "==": "tk_igual_igual",
    "!=": "tk_diferente",
    "<=": "tk_menor_igual",
    ">=": "tk_mayor_igual",

    # Operadores de un caracter
    "+": "tk_suma",
    "-": "tk_resta",
    "*": "tk_mult",
    "/": "tk_div",
    "%": "tk_mod",
    "<": "tk_menor",
    ">": "tk_mayor",
    "=": "tk_asignacion",

    # Puntuación
    "(": "tk_par_izq",
    ")": "tk_par_der",
    "[": "tk_cor_izq",
    "]": "tk_cor_der",
    "{": "tk_llave_izq",
    "}": "tk_llave_der",
    ",": "tk_coma",
    ".": "tk_punto",
    ":": "tk_dos_puntos",
    ";": "tk_punto_y_coma",
}

# Conjuntos útiles para el scanner
WHITESPACE = {" ", "\t", "\r"}
NEWLINE = {"\n"}
COMMENT_START = "#"

# Categorías:
# - IDENTIFICADOR: [A-Za-z_][A-Za-z0-9_]*
# - ENTERO:        [+-]?[0-9]+   (si el '+' o '-' no forma parte de un número, se reporta como símbolo)
# - CADENA:        " ... "  o  ' ... '  (simple sin escapes; cierre obligatorio en esta versión)
