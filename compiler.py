"""
Jaggi Charles-Lewis
Jeanneret Steven
HE-ARC
13 janvier 2019

Module to compile an AST tree
Contain the rules to compile the AST tree to an HTML file
Need parserproj in the same folder
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
    """ Add compile function to AST.ProgramNode
    Compile each children and concatenate their output"""
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:  # In case children don't produce an output
            output += out
    return output


@addToClass(AST.TokenNode)
def compile(self):
    """ Add compile function to AST.TokenNode
    Return the value of tok if it's a variable
    else return tok and children if there is one"""
    if self.tok in vars:
        return vars[self.tok]
    if len(self.children) > 0:
        return f"{self.tok} {self.children[0].compile()}"
    return self.tok


@addToClass(AST.AssignNode)
def compile(self):
    """ Add compile function to AST.AssignNode
     Set the value in vars """
    vars[self.children[0].tok] = self.children[1].compile()


@addToClass(AST.LineNode)
def compile(self):
    """ Add compile function to AST.LineNode
    Return the value of all children and add a breakline at end of line """
    output = ""
    for c in self.children:
        output += c.compile()
    return f"{output} <br>\n"


@addToClass(AST.StatementNode)
def compile(self):
    """ Add compile function to AST.StatementNode
    Return output of each children and check if result is not none"""
    output = ""
    for c in self.children:
        out = c.compile()
        if out is not None:
            output += out + " "
    return output


@addToClass(AST.OpNode)
def compile(self):
    """ Add compile function to AST.OpNode
    Try to make operation, if x or y are not Number, exit the program"""
    try:
        x = float(vars[self.children[0].tok])
        y = float(self.children[1].tok)
        return str(operations[self.op](x, y))
    except ValueError:
        print(f"an error occured in op {self.op} : {self.children[0].tok} or {self.children[1].tok} are not number")
        exit(2)


@addToClass(AST.StyleNode)
def compile(self):
    """ Add compile function to AST.StyleNode
    Return content inside html tag form tok """
    return f"<{self.tok}>{self.children[0].compile()}</{self.tok}>"


@addToClass(AST.EvalNode)
def compile(self):
    """ Add compile function to AST.EvalNode
    Evaluate condition of between var and a value """
    try:
        return evaluate[self.cond](float(self.var_name.compile()), float(self.stop_val))
    except TypeError:
        print(f"an error occured in eval {self.cond} : {self.var_name.compile()} "
              f"and {self.stop_val} don't have the same type")
        exit(3)


@addToClass(AST.WhileNode)
def compile(self):
    """ Add compile function to AST.WhileNode
    Concatenate output of each children while the condition isn't true"""
    output = ""
    while self.op.compile():
        for c in self.children:
            out = c.compile()
            if out is not None:
                output += out + " "
    return output


@addToClass(AST.ForNode)
def compile(self):
    """ Add compile function to AST.ForNode
    Concatenante output of each children while condition isn't true and increment the variable"""
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
    """ Add compile function to AST.IfNode
    If condition is true compile child 0 else compile child 1 """
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
