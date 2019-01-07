import AST
from AST import addToClass

vars = {}


@addToClass(AST.ProgramNode)
def compile(self):
    output = ""
    for c in self.children:
        print(f"before :{c} => {type(c)}")
        out = c.compile()
        if out is not None:
            output += out
    return output


@addToClass(AST.TokenNode)
def compile(self):
    if self.tok in vars:
        return vars[self.tok]
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:
            output += out + " "
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
    if output != "":
        output += "<br>\n"
    return output


@addToClass(AST.StatementNode)
def compile(self):
    output = ""
    for c in self.children:
        output += c.compile() + " "
    return output


@addToClass(AST.StyleNode)
def compile(self):
    return f"<{self.tok}>{self.children[0].compile()}</{self.tok}>"


if __name__ == '__main__':
    from parser import parse
    import sys, os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.html'
    with open(name, 'w') as outputfile:
        outputfile.write(compiled)
    print(f"Wrote output to {name}")