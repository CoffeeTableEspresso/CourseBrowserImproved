from tokens import *
from ast import *

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    def error(self,token_type):
        raise Exception("Expected %s Token at pos %s, got %s" % \
            (token_type, self.lexer.pos, self.current_token))
    def eat(self, token_type):
        #print self.current_token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)
    def statement(self):
        if self.current_token.type == BEGIN:
            return self.begin_block()
        elif self.current_token.type == ECHO:
            return self.echo()
        elif self.current_token.type == SELECT:
            return self.select_statement()
        elif self.current_token.type == SET:
            return self.assign_var()
        elif self.current_token.type == DEFUN:
            return self.def_func()
        else:
            return self.val()
        self.error()
    def begin_block(self):
            self.eat(BEGIN)
            statements = []
            while self.current_token.type != END:
                statements.append(self.statement())
                self.eat(SEMI)
            self.eat(END)
            return UnOp(Token(BEGIN, BEGIN), Token(LIST, statements))
    def echo(self):
        self.eat(ECHO)
        return UnOp(Token(ECHO, ECHO), self.val())
    def select_statement(self):
        self.eat(SELECT)
        columns = self.columns()
        self.eat(FROM)
        db = self.db()
        if self.current_token.type == WHERE:
            self.eat(WHERE)
            cond = self.cond()
        else:
            cond = None
        return TriOp(Token(SELECT, SELECT), columns, db, cond)
    def columns(self):
        # TODO: fix return values
        if self.current_token.type == STAR:
            self.eat(STAR)
            return Token(STAR, "*")
        else:
            columns = []
            columns.append(self.column())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                columns.append(self.column())
            return Token(LIST, columns)
    def db(self):
        token = self.current_token
        self.eat(ID)
        return DB(token)
    def column(self):
        token = self.current_token
        self.eat(ID)
        return Var(token) #Column
    def cond(self):
        first = self.val() # TODO: make sure this doesn't give any errors
        op = self.current_token
        self.eat(OP)
        second = self.val() # TODO: make sure this doesn't give any errors
        if self.current_token.value in ["&", "|"]:
            boolop = self.current_token
            self.eat(OP)
            return BinOp(boolop, BinOp(op, first, second), self.cond())
        else:
            return BinOp(op, first, second)
    def assign_var(self):
        self.eat(SET)
        var = Var(self.current_token)
        self.eat(ID)
        if self.current_token.value == "=":
            self.eat(OP)
        val = self.val() # TODO: make sure this works
        return Assign(var, val)
    def def_func(self):
        self.eat(DEFUN)
        name = Var(self.current_token)
        self.eat(ID)
        self.eat(COLON)
        params = []
        if self.current_token.type != ARROW:
            params.append(Var(self.current_token))
            self.eat(ID)
        while self.current_token.type != ARROW:
            self.eat(COMMA)
            params.append(Var(self.current_token))
            self.eat(ID)
        self.eat(ARROW)
        body = self.statement()
        return FuncDecl(name, params, body)
    def val(self):
        first = self.term()
        if self.current_token.type == OP:
            op = self.current_token
            self.eat(OP)
            second = self.val()
            return BinOp(op, first, second) 
        else: 
            return first
    def term(self):
        name = self.current_token
        # STR
        if self.current_token.type == STR:
             self.eat(STR)
             return String(name)
        # VAR
        self.eat(ID)
        if self.current_token.type != LPAREN:
             return Var(name)
        # func_call
        self.eat(LPAREN)
        params = []
        if self.current_token.type != RPAREN:
            params.append(self.val())
        while self.current_token.type != RPAREN:
            self.eat(COMMA)
            params.append(self.val())
        self.eat(RPAREN)
        return FuncCall(Var(name), params)
    def parse(self):
        while self.current_token.type != EOF:
            result = self.statement()
            if self.current_token.type == SEMI:
                self.eat(SEMI)
            elif self.current_token.type != EOF:
                self.error(EOF)
        return result
