import ply.lex as lex

reserved_words = (
    '_if',
    '_elif',
    '_endif',
    '_for',
    '_endfor',
    '_func',
    '_endfunc',
)

tokens = (
             'VAR',
             'WHILE_BEGIN',
             'WHILE_END',
             'WORD',
             'ADD_OP',
             'MUL_OP',
             'NEW_LINE',
             'HEADER_TITLE',
             'DOUBLE_DELIMITER',
             'SINGLE_DELIMITER',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '()=<>'

t_WHILE_BEGIN = r'_while'
t_WHILE_END = r'_endwhile'
t_HEADER_TITLE = r'\#{1,6}'
t_WORD = r'[A-Za-z0-9()!?;:.,]+'
t_DOUBLE_DELIMITER = r'[*]{2}'
t_SINGLE_DELIMITER = r'[*]{1}'
t_VAR = r'_\w+'
t_ADD_OP = r'[+-]'
t_MUL_OP = r'[*/]'


def t_NEW_LINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.value = ""
    return t


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


t_ignore = ' \t'

lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
