import ply.yacc as yacc

from lex5 import tokens
import AST

vars = {}


def p_text_statemet(p):
    ''' text : line '''
    p[0] = p[1]


def p_text(p):
    ''' text : line newline text
    | title newline text '''
    p[0] = p[1] + "\n" + p[3]


def p_line(p):
    ''' line : WORD '''
    p[0] = p[1]


def p_wordLine(p):
    '''  line : WORD line '''
    p[0] = p[1] + " " + p[2]


def p_title(p):
    ''' title : HEADER_TITLE line '''
    lvl_title = len(p[1])
    p[0] = f"<h{lvl_title}>" + p[2] + f"</h{lvl_title}>"


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
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
        print(result)

    else:
        print("Parsing returned no result!")
