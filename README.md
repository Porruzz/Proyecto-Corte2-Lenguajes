🧠 Proyecto Corte 2 – Analizador Léxico y Sintáctico LL(1)
📌 Descripción general

Este proyecto implementa un analizador léxico y sintáctico LL(1) capaz de procesar código fuente en un subconjunto de Python o en una gramática de expresiones aritméticas (E/T/F).
El usuario puede elegir qué modo de análisis ejecutar desde la terminal, así como mostrar los conjuntos FIRST, FOLLOW y PREDICCIÓN, y verificar la tabla LL(1).

El objetivo es demostrar el funcionamiento completo de un parser LL(1) a partir de una gramática libre de contexto, aplicando los algoritmos vistos en la presentación 6 del curso:

Cálculo de conjuntos FIRST

Cálculo de conjuntos FOLLOW

Generación de conjuntos PREDICT

Construcción de la tabla LL(1)

Ejecución del análisis sintáctico predictivo sobre un archivo de entrada .py

🧩 Estructura del proyecto
proyecto-ll1-corte2/
├─ README.md
├─ grammars/
│  ├─ ejemplo_p6.g               # Gramática de expresiones aritméticas (E/T/F)
│  └─ python_subset.g            # Subconjunto LL(1) del lenguaje Python
├─ examples/
│  ├─ python/
│  │  ├─ ok/mini.py              # Ejemplo válido en Python subset
│  │  ├─ bad/error_lex.py        # Ejemplo con error léxico
│  │  └─ bad/error_syntax.py     # Ejemplo con error sintáctico
│  └─ arith/
│     └─ expresion1.txt          # Ejemplo válido para gramática E/T/F
├─ src/
│  ├─ lexer/                     # Analizador léxico
│  │  └─ lexer.py
│  ├─ syntax/                    # Analizador sintáctico LL(1)
│  │  ├─ grammar_io.py
│  │  ├─ first_follow.py
│  │  ├─ predict.py
│  │  ├─ table.py
│  │  └─ parser_ll1.py
│  ├─ reporter.py                # Reportes de errores léxicos/sintácticos
│  └─ main.py                    # Punto de entrada (CLI principal)
└─ scripts/
   ├─ run_examples.sh            # Corre ejemplos válidos e inválidos
   └─ bench.sh                   # Pruebas de rendimiento

⚙️ Requisitos previos

Asegúrate de tener instalado Python 3.10 o superior y de ejecutar todo desde la carpeta raíz del proyecto.

cd ~/Escritorio/proyecto-ll1-corte2

🚀 Ejecución del analizador
🔹 1. Mostrar los conjuntos y la tabla LL(1)

Para visualizar los conjuntos FIRST, FOLLOW, PREDICT y la tabla LL(1) de la gramática:

Gramática de expresiones aritméticas (E, T, F)
python -m src.main --mode parse \
  --grammar grammars/ejemplo_p6.g \
  --input examples/arith/expresion1.txt \
  --show-sets --show-table

Subconjunto de Python
python -m src.main --mode parse \
  --grammar grammars/python_subset.g \
  --input examples/python/ok/mini.py \
  --show-sets --show-table

🔹 2. Analizar un archivo Python válido
python -m src.main --mode parse \
  --grammar grammars/python_subset.g \
  --input examples/python/ok/mini.py


Salida esperada:

El analisis sintactico ha finalizado exitosamente.

🔹 3. Analizar un archivo con error léxico
python -m src.main --mode parse \
  --grammar grammars/python_subset.g \
  --input examples/python/bad/error_lex.py


Salida esperada:

<1,5> Error léxico: carácter no reconocido '@'

🔹 4. Analizar un archivo con error sintáctico
python -m src.main --mode parse \
  --grammar grammars/python_subset.g \
  --input examples/python/bad/error_syntax.py


Salida esperada:

<2,1> Error sintactico: se encontro: "print"; se esperaba: "$", ")", "*", "+", "id"

🔹 5. Ejecutar pruebas automáticas
chmod +x scripts/run_examples.sh
./scripts/run_examples.sh


Muestra los resultados de archivos válidos e inválidos, indicando si fueron correctamente aceptados o rechazados.

🔹 6. Pruebas de rendimiento (opcional)
chmod +x scripts/bench.sh
./scripts/bench.sh


Ejecuta 10 pruebas y muestra los tiempos promedio de ejecución del analizador LL(1).

🧮 Algoritmos implementados
🔸 Conjuntos FIRST

Determinan qué terminales pueden aparecer al comienzo de una derivación desde cada no terminal.
Basado en el algoritmo recursivo:

Si X es terminal → FIRST(X) = {X}
Si X → ε → ε ∈ FIRST(X)
Si X → Y1 Y2 ... Yn:
   agrega FIRST(Y1) sin ε
   si ε ∈ FIRST(Y1) agrega FIRST(Y2), y así sucesivamente

🔸 Conjuntos FOLLOW

Indican qué terminales pueden seguir a cada no terminal dentro de una derivación.
El algoritmo se basa en el análisis de las producciones y el símbolo inicial $.

🔸 Conjuntos PREDICT

Se calculan para cada producción A → α:

Si ε ∉ FIRST(α): PREDICT(A → α) = FIRST(α)
Si ε ∈ FIRST(α): PREDICT(A → α) = FIRST(α) ∪ FOLLOW(A)

🔸 Tabla LL(1)

Se genera a partir de los conjuntos PREDICT y permite construir un analizador sintáctico predictivo no recursivo.
El parser utiliza una pila para comparar los símbolos esperados con los tokens generados por el analizador léxico.
