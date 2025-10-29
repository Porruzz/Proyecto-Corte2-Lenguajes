# -*- coding: utf-8 -*-
"""
main.py
-------
CLI unificada:
- --mode lex   : solo tokeniza un archivo fuente (.py o .txt) y muestra tokens
- --mode parse : tokeniza + parsea LL(1) usando una gramática dada (.g)
                 e imprime FIRST, FOLLOW, PREDICT y Tabla si se pide.

Ejemplos:
  python -m src.main --mode parse --grammar grammars/ejemplo_p6.g --input examples/ok/expresion1.txt --show-sets --show-table
  python -m src.main --mode parse --grammar grammars/python_subset.g --input examples/python/ok/mini.py
"""
import argparse
from pathlib import Path

# LEXER
from .lexer.tokenizer import tokenize
from .reporter import print_tokens

# SYNTAX (LL1)
from .syntax.grammar_io import load_grammar, EPS
from .syntax.first_follow import compute_first_sets, compute_follow_sets
from .syntax.predict import compute_predict_sets
from .syntax.table import build_ll1_table, has_conflicts
from .syntax.parser_ll1 import parse_ll1

def run_lex(input_path: str, out_path: str | None) -> int:
    p = Path(input_path)
    if not p.exists():
        print(f"Archivo no encontrado: {input_path}")
        return 1
    src = p.read_text(encoding="utf-8")
    try:
        tokens = tokenize(src)
        if out_path:
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                for ttype, lex, line, col in tokens:
                    if ttype in {"identificador", "tk_entero", "tk_cadena"}:
                        f.write(f"<{ttype}, {lex}, {line}, {col}>\n")
                    else:
                        if ttype.startswith("tk_"):
                            f.write(f"<{ttype}, {line}, {col}>\n")
                        else:
                            f.write(f"<{ttype}, {line}, {col}>\n")
        print_tokens(tokens)
        return 0
    except ValueError as e:
        print(str(e))
        return 1

def run_parse(grammar_path: str, input_path: str, show_sets: bool, show_table: bool, show_deriv: bool) -> int:
    gp = Path(grammar_path)
    ip = Path(input_path)
    if not gp.exists():
        print(f"Gramática no encontrada: {grammar_path}")
        return 1
    if not ip.exists():
        print(f"Archivo de entrada no encontrado: {input_path}")
        return 1

    # 1) Cargar gramática
    start, G = load_grammar(str(gp))

    # 2) Tokenizar entrada
    src = ip.read_text(encoding="utf-8")
    try:
        tokens = tokenize(src)
    except ValueError as e:
        print(str(e))
        return 1

    # 3) FIRST, FOLLOW, PREDICT y Tabla
    FIRST = compute_first_sets(G)
    FOLLOW = compute_follow_sets(start, G, FIRST)
    PRED = compute_predict_sets(start, G, FIRST, FOLLOW)
    TABLE = build_ll1_table(PRED)

    # 4) Reportes opcionales
    if show_sets:
        print("== PRIMEROS ==")
        for A in G:
            print(f"{A} :", sorted(FIRST.get(A, set())))
        print("\n== SIGUIENTES ==")
        for A in G:
            print(f"{A} :", sorted(FOLLOW.get(A, set())))

        print("\n== PREDICCIÓN ==")
        for (A, rhs), terms in PRED.items():
            print(f"{A} -> {' '.join(rhs)} : {sorted(terms)}")

    if show_table:
        print("\n== Tabla LL(1) ==")
        for (A, a), prods in sorted(TABLE.items()):
            print(f"[{A},{a}] -> {' / '.join(prods)}")
        conf = has_conflicts(TABLE)
        print("\n✓ Sin conflictos LL(1)" if conf == 0 else f"\n✗ Conflictos: {conf}")

    # 5) Parse predictivo
    ok, msg = parse_ll1(start, G, TABLE, tokens, show_derivations=show_deriv)
    print(msg)
    return 0 if ok else 2

def main():
    ap = argparse.ArgumentParser(description="Proyecto Corte 2: Analizador léxico + sintáctico (LL(1)).")
    ap.add_argument("--mode", choices=["lex", "parse"], required=True, help="lex: solo lexer; parse: LL(1).")
    ap.add_argument("--input", required=True, help="Ruta del archivo fuente (.py o .txt)")
    ap.add_argument("--out", help="(lex) archivo de salida de tokens")
    ap.add_argument("--grammar", help="(parse) gramática .g, ej: grammars/ejemplo_p6.g", default="grammars/ejemplo_p6.g")
    ap.add_argument("--show-sets", action="store_true", help="(parse) imprime FIRST/FOLLOW/PREDICT")
    ap.add_argument("--show-table", action="store_true", help="(parse) imprime la tabla LL(1)")
    ap.add_argument("--show-deriv", action="store_true", help="(parse) imprime derivaciones aplicadas")
    args = ap.parse_args()

    if args.mode == "lex":
        exit(run_lex(args.input, args.out))
    else:
        exit(run_parse(args.grammar, args.input, args.show_sets, args.show_table, args.show_deriv))

if __name__ == "__main__":
    main()
