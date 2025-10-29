# Subconjunto LL(1) de Python para asignaciones y print

S         -> stmt S | ε

stmt      -> assign | printStmt

assign    -> id = expr

printStmt -> print ( expr )

expr      -> term expr'
expr'     -> + term expr' | ε

term      -> factor term'
term'     -> * factor term' | ε

factor    -> ( expr ) | id | NUM
