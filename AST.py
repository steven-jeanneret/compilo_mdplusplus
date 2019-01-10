"""
Jaggi Charles-Lewis
Jeanneret Steven
HE-ARC
13 janvier 2019
"""


import pydot


class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'

    def __init__(self, children=None):
        self.ID = str(Node.count)
        Node.count += 1
        if not children:
            self.children = []
        elif hasattr(children, '__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self, next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c, Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix, type(c), c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
        if not dot: dot = pydot.Dot()
        dot.add_node(pydot.Node(self.ID, label=repr(self), shape=self.shape))
        label = edgeLabels and len(self.children) - 1
        for i, c in enumerate(self.children):
            c.makegraphicaltree(dot, edgeLabels)
            edge = pydot.Edge(self.ID, c.ID)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
            # Workaround for a bug in pydot 1.0.2 on Windows:
            # dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.38\bin\dot.exe'})
        return dot

    def threadTree(self, graph, seen=None, col=0):
        colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
        if not seen: seen = []
        if self in seen: return
        seen.append(self)
        new = not graph.get_node(self.ID)
        if new:
            graphnode = pydot.Node(self.ID, label=repr(self), shape=self.shape)
            graphnode.set_style('dotted')
            graph.add_node(graphnode)
        label = len(self.next) - 1
        for i, c in enumerate(self.next):
            if not c: return
            col = (col + 1) % len(colors)
            col = 0  # FRT pour tout afficher en rouge
            color = colors[col]
            c.threadTree(graph, seen, col)
            edge = pydot.Edge(self.ID, c.ID)
            edge.set_color(color)
            edge.set_arrowsize('.5')
            # Les arr�tes correspondant aux coutures ne sont pas prises en compte
            # pour le layout du graphe. Ceci permet de garder l'arbre dans sa repr�sentation
            # "standard", mais peut provoquer des surprises pour le trajet parfois un peu
            # tarabiscot� des coutures...
            # En commantant cette ligne, le layout sera bien meilleur, mais l'arbre nettement
            # moins reconnaissable.
            edge.set_constraint('false')
            if label:
                edge.set_taillabel(str(i))
                edge.set_labelfontcolor(color)
            graph.add_edge(edge)
        return graph


class ProgramNode(Node):
    type = 'Program'


class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self, children)
        self.op = op

    def __repr__(self):
        return f"{self.op}"


class LineNode(Node):
    def __init__(self, children):
        Node.__init__(self, children)
        self.tok = "line"

    def __repr__(self):
        return self.tok


class StyleNode(Node):
    type = 'style'

    def __init__(self, tok, children=None):
        Node.__init__(self, children)
        self.tok = tok

    def __repr__(self):
        return self.tok


class WhileNode(Node):
    type = 'while'

    def __init__(self, op, children=None):
        Node.__init__(self, children)
        self.op = op

    def __repr__(self):
        return f"while {self.op}"


class ForNode(Node):
    type = 'for'

    def __init__(self, set_var, cond, inc, children=None):
        Node.__init__(self, children)
        self.set_var = set_var
        self.cond = cond
        self.inc = inc

    def __repr__(self):
        return f"for {self.cond}"


class IfNode(Node):
    type = 'if'

    def __init__(self, cond, children):
        Node.__init__(self, children)
        self.cond = cond

    def __repr__(self):
        return f"if {self.cond}"


class EvalNode(Node):
    type = 'eval'

    def __init__(self, var_name, cond, stop_val):
        Node.__init__(self)
        self.var_name = var_name
        self.cond = cond
        self.stop_val = stop_val

    def __repr__(self):
        return f"{self.var_name} {self.cond} {self.stop_val}"


class StatementNode(Node):
    def __init__(self, children=None):
        Node.__init__(self, children)

    def __repr__(self):
        return "Statement"


class TokenNode(Node):
    type = 'token'

    def __init__(self, tok, children=None):
        Node.__init__(self, children)
        self.tok = tok

    def __repr__(self):
        return repr(self.tok)


class AssignNode(Node):
    type = '='


class PrintNode(Node):
    type = 'print'


class EntryNode(Node):
    type = 'ENTRY'

    def __init__(self):
        Node.__init__(self, None)


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator
