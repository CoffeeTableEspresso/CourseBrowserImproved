from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import sys


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
