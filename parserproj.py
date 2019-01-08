import ply.yacc as yacc

import AST
from lex import tokens

vars = {}


def p_file_line(p):
    """ file : line file
            | list file """
    p[0] = AST.ProgramNode([p[1]] + p[2].children)


def p_file(p):
    """ file : line
            | list """
    p[0] = AST.ProgramNode(p[1])


def p_line(p):
    """ line : statement NEW_LINE """
    p[0] = AST.LineNode(p[1])

def p_line_assign(p):
    """ line : assign NEW_LINE """
    p[0] = AST.StatementNode(p[1])  # Don't display blank line


def p_op(p):
    """ statement : VAR ADD_OP WORD
        | VAR MUL_OP WORD"""
    try:
        p[0] = AST.OpNode(p[2], [AST.TokenNode(p[1]), AST.TokenNode(p[3])])
    except(ValueError):
        pass


def p_line_title(p):
    """ line : HEADER_TITLE words NEW_LINE """
    lvl_title = len(p[1])
    p[0] = AST.StyleNode(f"h{lvl_title}", p[2])


def p_statement(p):
    """ statement : words statement
                | words
                | use_var """
    if len(p) > 2:
        p[0] = AST.StatementNode([p[1], p[2]])
    else:
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


def p_words(p):
    """ words : WORD
                | WORD words"""
    if len(p) > 2:
        p[0] = AST.TokenNode(p[1], p[2])
    else:
        p[0] = AST.TokenNode(p[1])


def p_list(p):
    """ list : SINGLE_DELIMITER statement NEW_LINE"""
    p[0] = AST.StyleNode('li', p[2])


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.yacc().errok()
    else:
        print("Sytax error: unexpected end of file!")


def p_var_assign(p):
    """ assign : VAR '=' statement """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_var_use(p):
    """ use_var : VAR """
    p[0] = AST.TokenNode(p[1])


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    print(result)
    if result:
        import os

        ##os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)

    else:
        print("Parsing returned no result!")