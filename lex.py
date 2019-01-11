"""
Jaggi Charles-Lewis
Jeanneret Steven
HE-ARC
13 janvier 2019

module that contain the lexeme of the language.
is use to detect the word of the language with regular expression
"""

import ply.lex as lex

reserved_words = (
    '_while',
    '_endwhile',
    '_for',
    '_endfor',
    '_if',
    '_else',
    '_endif',
)

tokens = (
             'WORD',
             'ADD_OP',
             'NEW_LINE',
             'HEADER_TITLE',
             'DOUBLE_DELIMITER',
             'SINGLE_DELIMITER',
             'EVAL_OP',
             'VAR',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '=;'
t_EVAL_OP = r'<|>|=='
t_HEADER_TITLE = r'\#{1,6}'
t_WORD = r'\w+'
t_DOUBLE_DELIMITER = r'[*]{2}'
t_SINGLE_DELIMITER = r'[*]{1}'
t_ADD_OP = r'[+-/]'


def t_NEW_LINE(t):
    """
    function to detect a new line in the code
    :param t: token detected
    :return: token
    """
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.value = ""
    return t


def t_VAR(t):
    """
    Function to detect a variable in the code
    if the var name is in reserved word put
    :param t: token detected
    :return: token
    """
    r'_\w+'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_error(t):
    """
    function executed when an error occure in the lex process
    :param t: token which make the error
    """
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
