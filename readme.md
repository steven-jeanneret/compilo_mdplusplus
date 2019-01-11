# Markdown++
## Download
```shell=
git clone https://github.com/steven-jeanneret/compilo_mdplusplus
cd compilo_mdplusplus
```

## Requirement
* Python 3.6

### Modules python
* pydot
* ply

### Logiciel
* Graphviz

## Lex
To run lex, run the following command and specify a Markdown++ file.

```shell=
python lex.py filename.txt
```

In the same folder a new text file was created : *filename.txt*. This file contain all the *lexems*.

## Parser
> Graphviz is needed and it may be necessary to define the path, if so edit *parserproj.py* and change the content of `PATH_TO_GRAPHVIZ` places after import.

To run parser, run ths following command and specify a Markdown++ file.

```shell=
python parserproj.py filename.txt
```

In the same folder a new *pdf* file was created : filename-ast.pdf. This file contains the AST tree.

## Compiler
```shell=
python compiler.py filename.txt
```
In the same folder a new *html* file has been created : filename.html. This file contains the compiled *html* of input code.
