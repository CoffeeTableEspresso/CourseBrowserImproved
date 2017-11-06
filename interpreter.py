from tokens import *
from ast import *
from parser import Parser
from lexer import Lexer
import pickle
import sys

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class Symbol(object):
    def __init__(self, name, stype=None):
        self.name = name
        self.type = stype
class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)
    def __str__(self):
        return self.name
    __repr__ = __str__
class VarSymbol(Symbol):
    def __init__(self, name, stype):
        super(VarSymbol, self).__init__(name, stype)
    def __str__(self):
        return "%s: %s" % (self.name, self.type)
    __repr__ = __str__
class FuncSymbol(Symbol):
    def __init__(self, name, params=None):
        super(FuncSymbol, self).__init__(name)
        self.params = params if params is not None else []
    def __str__(self):
        return "<%s(name=%s, parameters=%s)>" % (self.__class__.__name__, self.name, self.params)
    __repr__ = __str__

class ScopedSymbolTable(object):
    def __init__(self, name, level, parent=None):
        self._symbols = {}
        self.scope_name = name
        self.scope_level = level
        self.parent = parent
        self._init_builtins()
    def _init_builtins(self):
        self.insert(VarSymbol("Courses", "DB"))
        self.insert(BuiltinTypeSymbol("DB"))
        self.insert(BuiltinTypeSymbol("COURSE"))
        self.insert(BuiltinTypeSymbol("DEPT"))
        self.insert(BuiltinTypeSymbol("YEAR"))
    def __str__(self):
        return "Symbols: %s" % str([value for value in self._symbols.values()])
    __repr__ = __str__
    def insert(self, symbol):
        #print "Insert: %s" % symbol
        self._symbols[symbol.name] = symbol
    def lookup(self, name, cur_only=False):
        #print "Lookup: %s" % name
        symbol = self._symbols.get(name) # return Symbol | None
        if symbol is not None:
            return symbol
        if cur_only:
            return None
        if self.parent is not None:
            return self.parent.lookup(name)
        return None #not found


class Memory(object):
    def __init__(self):
        self._mem = {}
        self._mem["Courses"] = Stack().push(pickle.load(open("Courses.db")))
        self._mem["postreqs"] = Stack().push(([Var(Token(ID, "n"))], \
                                         TriOp(Token(SELECT, SELECT), \
                                               Token(LIST, [Var(Token(ID, "title"))]), \
                                               DB(Token(ID, "Courses")), \
                                               BinOp(Token(OP, IN), Var(Token(ID, "n")), Var(Token(ID, "prereqs"))))))
        self._mem["get"] = Stack().push(([Var(Token(ID, "n"))], \
                                         TriOp(Token(SELECT, SELECT), \
                                               Token(STAR, "*"), \
                                               DB(Token(ID, "Courses")), \
                                               BinOp(Token(OP, "="), Var(Token(ID, "n")), Var(Token(ID, "name"))))))
    def insert(self, key, value):
        #print "Insert: %s, %s" % (key, value)
        if key in self._mem.keys():
            self._mem.get(key).push(value)
        else:
            self._mem[key] = Stack().push(value)
    def get(self, key):
        #print "Lookup: %s, %s" % (key, self._mem[key].peek())
        return self._mem[key].peek()
    def delete(self, key):
        #print "Delete: %s, %s" % (key, self._mem[key].peek())
        self._mem[key].pop()
    def __str__(self):
        result = ""
        for key in self._mem.keys():
            result += "%s: %s\n" % (key, self._mem.get(key))
	return result
    __repr__ = __str__

class Stack(object):
    def __init__(self):
        self.stack = []
    def push(self, val):
        self.stack.append(val)
        return self
    def pop(self):
        tmp = self.stack[-1]
        self.stack = self.stack[:-1]
        return tmp
    def peek(self):
        return self.stack[-1]
    def __str__(self):
        result = ""
        for element in self.stack:
            result += ("\t%s\n" % element)
        return result
    __repr__ = __str__

class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception("No visit_%s method: %s" % (type(node).__name__, node))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.current_scope = ScopedSymbolTable("GLOBAL", 1)
        self.mem = Memory()
    def visit_TriOp(self, node):
        if node.op.type == SELECT:
            db = self.visit(node.middle)
            for d in db:
                for pair in d.__dict__.items():
                    self.mem.insert(pair[0], pair[1])
                if not node.right or self.visit(node.right):
                    cols = node.left.value # TODO: make sure this works for large DB
                    if node.left.value == "*":
                        cols = [Var(Token(ID, pair[0])) for pair in d.__dict__.items()]
                        cols.reverse()
                    for col in cols:
                        print self.visit(col)
                    print "-"*80
                for pair in d.__dict__.items():
                    self.mem.delete(pair[0])
    def visit_BinOp(self, node):
        if node.op.value == "IN":
            return self.visit(node.left) in self.visit(node.right)
        elif node.op.value == "CONTAINS":
            return self.visit(node.right) in self.visit(node.left)
        elif node.op.value == "=":
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.value == "&":
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.value == "|":
            return self.visit(node.left) or self.visit(node.right)
    def visit_UnOp(self, node):
        if node.op.type == BEGIN:
            if len(node.expr.value) == 0:
                return None
            else:
                for innernode in node.expr.value[:-1]:
                    self.visit(innernode)
                return self.visit(node.expr.value[-1])
        elif node.op.type == ECHO:
            val = self.visit(node.expr)
            print val
            return val
    #def visit_NulOp(self, node):
    #   return "MC TEXT"
    def visit_FuncDecl(self, node):
        self.mem.insert(node.value, (node.params, node.block))
    def visit_FuncCall(self, node):
        func = self.mem.get(node.value)
        for i in range(0, len(func[0])):
            self.mem.insert(func[0][i].value, self.visit(node.params[i]))
        tmp = self.visit(func[1])
        for i in range(0, len(func[0])):
            self.mem.delete(func[0][i].value)
        return tmp
    def visit_Decl(self, node):
        pass
    def visit_Assign(self, node):
        var_name = node.left.value
        result = self.visit(node.right)
        self.mem.insert(var_name, result)
        return self.mem.get(var_name)
    def visit_Var(self, node):
        var_name = node.value
        val = self.mem.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val
    def visit_DB(self, node):
        db_name = node.value
        val = self.mem.get(db_name)
        if val is None:
            raise NameError(repr(db_name))
        else:
            return val
    def visit_String(self, node):
        return node.value
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    interpreter = Interpreter("")
    while True:
        try:
            text = raw_input(">>> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter.parser = parser # = Interpreter(parser)
        result = interpreter.interpret()
        print result

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        assert(len(sys.argv) == 2)
        interpreter = Interpreter("")
        texts = open(sys.argv[1]).read().splitlines() #TODO: make more general, so file can be located anywhere
        for text in texts: #TODO: fix so that expressions can cross newlines
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter.parser = parser # = Interpreter(parser)
            result = interpreter.interpret()
