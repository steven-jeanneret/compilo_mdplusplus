import AST
from AST import addToClass

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
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
    output = ""
    if len(self.children) > 0:
        output += self.children[0].compile()
    return self.tok + " " + output


@addToClass(AST.AssignNode)
def compile(self):
    vars[self.children[0].tok] = self.children[1].compile()


@addToClass(AST.LineNode)
def compile(self):
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:
            output += out
    output += "<br>\n"
    return output


@addToClass(AST.StatementNode)
def compile(self):
    output = ""
    for c in self.children:
        output += c.compile() + " "
    return output


@addToClass(AST.OpNode)
def compile(self):
    try:
        y = int(self.children[1])
        x = int(vars[self.children[0]])
        res = AST.TokenNode(str(operations[self.op](x, y)))
    except ValueError:
        res = AST.TokenNode(vars[self.children[0]])
    return res


@addToClass(AST.StyleNode)
def compile(self):
    return f"<{self.tok}>{self.children[0].compile()}</{self.tok}>"


if __name__ == '__main__':
    from parserproj import parse
    import sys, os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.html'
    with open(name, 'w') as outputfile:
        outputfile.write(compiled)
    print(f"Wrote output to {name}")
