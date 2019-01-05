import ply.yacc as yacc
from lex import tokens

vars = {}


def p_file_line(p):
    """ file : line file
            | list file """
    p[0] = p[1] + p[2]


def p_file(p):
    """ file : line
            | list """
    p[0] = p[1]


def p_line(p):
    """ line : statement NEW_LINE """
    p[0] = p[1] + "<br>\n"


def p_line_title(p):
    """ line : HEADER_TITLE words NEW_LINE """
    lvl_title = len(p[1])
    p[0] = f"<h{lvl_title}>" + p[2] + f"</h{lvl_title}>\n"


def p_statement(p):
    """ statement : words statement
                | words """
    p[0] = p[1]
    if len(p) > 2:
        p[0] += " " + p[2]


def p_statement_bold(p):
    """ statement : DOUBLE_DELIMITER words DOUBLE_DELIMITER """
    p[0] = f"<b>{p[2]}</b>"


def p_statement_italic(p):
    """ statement : SINGLE_DELIMITER words SINGLE_DELIMITER"""
    p[0] = f"<i>{p[2]}</i>"


def p_words(p):
    """ words : WORD
                | WORD words"""
    p[0] = p[1]
    if len(p) > 2:
        p[0] += " " + p[2]


def p_list(p):
    """ list : SINGLE_DELIMITER statement NEW_LINE"""
    p[0] = f"<li>{p[2]}</li>\n"


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
        print(result)
        with open('index.html', 'w') as f:
            f.writelines(result)

    else:
        print("Parsing returned no result!")
