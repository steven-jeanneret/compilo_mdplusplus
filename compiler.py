"""
Jaggi Charles-Lewis
Jeanneret Steven
HE-ARC
13 janvier 2019
"""


import AST
from AST import addToClass

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

evaluate = {
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '==': lambda x, y: x == y,
}

vars = {}


@addToClass(AST.ProgramNode)
def compile(self):
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:
            output += out
    return output


@addToClass(AST.TokenNode)
def compile(self):
    if self.tok in vars:
        return vars[self.tok]
    if len(self.children) > 0:
        return f"{self.tok} {self.children[0].compile()}"
    return self.tok


@addToClass(AST.AssignNode)
def compile(self):
    vars[self.children[0].tok] = self.children[1].compile()


@addToClass(AST.LineNode)
def compile(self):
    output = ""
    for c in self.children:
        output += c.compile()
    return f"{output} <br>\n"


@addToClass(AST.StatementNode)
def compile(self):
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:
            output += out + " "
    return output


@addToClass(AST.OpNode)
def compile(self):
    try:
        x = float(vars[self.children[0].tok])
        y = float(self.children[1].tok)
        return str(operations[self.op](x, y))
    except ValueError:
        print(f"an error occured in op {self.op} : {self.children[0].tok} or {self.children[1].tok} are not number")
        exit(2)


@addToClass(AST.StyleNode)
def compile(self):
    return f"<{self.tok}>{self.children[0].compile()}</{self.tok}>"


@addToClass(AST.EvalNode)
def compile(self):
    return evaluate[self.cond](self.var_name.compile(), self.stop_val)


@addToClass(AST.WhileNode)
def compile(self):
    output = ""
    while self.op.compile():
        for c in self.children:
            out = c.compile()
            if out is not None:
                output += out + " "
    return output


@addToClass(AST.ForNode)
def compile(self):
    output = ""
    self.set_var.compile()
    while self.cond.compile():
        for c in self.children:
            out = c.compile()
            if out is not None:
                output += out + " "
        self.inc.compile()
    return output


@addToClass(AST.IfNode)
def compile(self):
    output = ""
    if self.cond.compile():
        output = self.children[0].compile()
    elif len(self.children) > 1:
        output = self.children[1].compile()
    return output


if __name__ == '__main__':
    from parserproj import parse
    import sys, os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.html'
    with open(name, 'w') as file:
        file.write(compiled)
    print(f"Wrote output to {name}")
