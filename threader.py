import AST
from AST import addToClass

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self


def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry


if __name__ == '__main__':
    from parserproj import parse
    import sys
    import os

    ##os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)
    graph = ast.makegraphicaltree()
    entry.threadTree(graph)
    name = os.path.splitext(sys.argv[1])[0] + '-ast-threaded.pdf'
    graph.write_pdf(name)
    print(f"wrote threaded ast to {name}")