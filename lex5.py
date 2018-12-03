import ply.lex as lex

reserved_words = (
    '_while',
    '_endwhile',
    '_if',
    '_elif',
    '_endif',
    '_for',
    '_endfor',
    '_func',
    '_endfunc',
)

tokens = (
             'WORD',
             'newline',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '#'

t_WORD=r'\S+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)

t_ignore  = ' \t'

lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
