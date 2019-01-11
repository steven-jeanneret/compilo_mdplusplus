"""
Jaggi Charles-Lewis
Jeanneret Steven
HE-ARC
13 janvier 2019

Module to parse the given code.
Contain the rules of the language and build the syntactic tree
Graphviz is needed and it may be necessary to define the path
Edit PATH_TO_GRAPHVIZ places after import
"""


import ply.yacc as yacc

import AST
from lex import tokens

PATH_TO_GRAPHVIZ = 'C:/Program Files (x86)/Graphviz2.38/bin/'
vars = {}


def p_file_line_file(p):
    """ file : line file
            | list file """
    p[0] = AST.ProgramNode([p[1]] + p[2].children)


def p_file_list_code(p):
    """ file : code file """
    p[0] = AST.ProgramNode(p[1].children + p[2].children)


def p_file_line(p):
    """ file : line
            | list """
    p[0] = AST.ProgramNode(p[1])


def p_file(p):
    """ file : code """
    p[0] = AST.ProgramNode(p[1].children)


def p_line(p):
    """ line : statement NEW_LINE
            | statement """
    p[0] = AST.LineNode(p[1])  # Will add <br>\n at end of line


def p_line_assign(p):
    """ line : assign NEW_LINE
            | assign """
    p[0] = AST.StatementNode(p[1])


def p_line_title(p):
    """ line : HEADER_TITLE words NEW_LINE
    | HEADER_TITLE words """
    lvl_title = len(p[1])
    p[0] = AST.StyleNode(f"h{lvl_title}", p[2])


def p_op(p):
    """ statement : VAR ADD_OP WORD
        | VAR SINGLE_DELIMITER WORD"""
    try:
        p[0] = AST.OpNode(p[2], [AST.TokenNode(p[1]), AST.TokenNode(p[3])])
    except ValueError:
        print(f"An error occured with operation {p[1]} - {p[2]} - {p[3]}")
        exit(1)


def p_statement(p):
    """ statement : words
                | use_var"""
    p[0] = AST.StatementNode(p[1])


def p_statement_multi(p):
    """ statement : statement statement """
    p[0] = AST.StatementNode([p[1], p[2]])


def p_statement_bold(p):
    """ statement : DOUBLE_DELIMITER words DOUBLE_DELIMITER """
    p[0] = AST.StyleNode('b', p[2])


def p_statement_italic(p):
    """ statement : SINGLE_DELIMITER words SINGLE_DELIMITER"""
    p[0] = AST.StyleNode('i', p[2])


def p_list(p):
    """ list : SINGLE_DELIMITER statement NEW_LINE
            | SINGLE_DELIMITER statement"""
    p[0] = AST.StyleNode('li', p[2])


def p_words(p):
    """ words : WORD """
    p[0] = AST.TokenNode(p[1])


def p_words_multi(p):
    """ words : WORD words """
    p[0] = AST.TokenNode(p[1], p[2])


def p_var_use(p):
    """ use_var : VAR """
    p[0] = AST.TokenNode(p[1])


def p_eval(p):
    """ eval : VAR EVAL_OP WORD"""
    p[0] = AST.EvalNode(AST.TokenNode(p[1]), p[2], p[3])


def p_var_assign(p):
    """ assign : VAR '=' statement """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_code_line(p):
    """ code : code NEW_LINE """
    p[0] = AST.ProgramNode(p[1].children)


def p_code(p):
    """ code : while_block
            | for_block
            | if_block
            | if_else_block """
    p[0] = AST.ProgramNode(p[1])


def p_while(p):
    """while_block : _WHILE eval NEW_LINE file _ENDWHILE"""
    p[0] = AST.WhileNode(p[2], p[4].children)


def p_for(p):
    """ for_block : _FOR assign ';' eval ';' assign NEW_LINE file _ENDFOR"""
    p[0] = AST.ForNode(p[2], p[4], p[6], p[8].children)


def p_if(p):
    """ if_block : _IF eval NEW_LINE file _ENDIF """
    p[0] = AST.IfNode(p[2], p[4].children)


def p_if_else(p):
    """ if_else_block : _IF eval NEW_LINE file _ELSE NEW_LINE file _ENDIF """
    p[0] = AST.IfNode(p[2], p[4].children + p[7].children)


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.yacc().errok()
    else:
        print("Sytax error: unexpected end of file!")


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        import os

        os.environ["PATH"] += os.pathsep + PATH_TO_GRAPHVIZ
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)

    else:
        print("Parsing returned no result!")
