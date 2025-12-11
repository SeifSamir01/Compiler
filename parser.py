from scanner import Scanner
class ParserError(Exception):
    pass

class Parser:

    DATATYPES = {"int", "float", "double", "char"}

    OPERATORS = {"+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="}

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def Token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return None

    def Read_token(self):
        """Return (type, value) or (None, None) if no token."""
        raw = self.Token()
        if raw is None:
            return (None, None)
        s = raw.strip()
        if not (s.startswith("<") and s.endswith(">")):
            return (None, raw)
        inner = s[1:-1]
        parts = inner.split(",", 1)
        if len(parts) == 1:
            type = parts[0].strip()
            value = ""
        else:
            type = parts[0].strip()
            value = parts[1].strip()
        return (type, value)

    def next_token(self):
        self.index += 1

    def match(self, expected_type=None, expected_value=None):
        type, value = self.Read_token()
        if type == expected_type and (expected_value is None or value == expected_value):
            self.next_token()
            return (type, value)
        raise ParserError("Syntax error")

    #grammer
    def parse(self):
        # PROGRAM -> FUNC
        self.func()
        # after parse, we must have finished all tokens
        if self.index != len(self.tokens):
            # if not finished syntax error
            raise ParserError("Syntax error")

    def func(self):
        # FUNC -> "int" "main" "(" ")" BLOCK
        self.match("KEYWORD", "int")
        self.match("KEYWORD", "main")
        self.match("SPECIAL CHARACTER", "(")
        self.match("SPECIAL CHARACTER", ")")
        self.block()

    def block(self):
        # BLOCK -> "{" STATEMENTS "}"
        self.match("SPECIAL CHARACTER", "{")
        self.statements()
        self.match("SPECIAL CHARACTER", "}")

    def statements(self):
        # STATEMENTS -> STATEMENT STATEMENTS | ε
        # iterate while next token can start a statement
        while True:
            type, value = self.Read_token()
            if type is None:
                # end of input inside block -> will be caught by missing "}"
                break
            # what tokens can start a statement?
            if (type == "KEYWORD" and (value in self.DATATYPES or value == "if" or value == "return")) \
               or type == "IDENTIFIER" \
               or (type == "SPECIAL CHARACTER" and value == "{"):
                self.statement()
                continue
            # otherwise epsilon (no more statements)
            break

    def statement(self):
        # STATEMENT → DECLARATION ";" | ASSIGN ";" | IF_STMT | RETURN ";" | BLOCK
        type, value = self.Read_token()

        if type == "KEYWORD" and value in self.DATATYPES:
            # declaration then ;
            self.declaration()
            self.match("SPECIAL CHARACTER", ";")
            return

        if type == "IDENTIFIER":
            # assign then ;
            self.assign()
            self.match("SPECIAL CHARACTER", ";")
            return

        if type == "KEYWORD" and value == "if":
            self.if_stmt()
            return

        if type == "KEYWORD" and value == "return":
            self.return_stmt()
            self.match("SPECIAL CHARACTER", ";")
            return

        if type == "SPECIAL CHARACTER" and value == "{":
            self.block()
            return

        # no valid statement start
        raise ParserError("Syntax error")

    def declaration(self):
        # DECLARATION → TYPE ID_LIST
        # TYPE
        type, value = self.match("KEYWORD")
        if value not in self.DATATYPES:
            raise ParserError("Syntax error")
        # ID_LIST → id ("," id)*
        self.match("IDENTIFIER")
        while True:
            type2, value2 = self.Read_token()
            if type2 == "SPECIAL CHARACTER" and value2 == ",":
                self.next_token()
                self.match("IDENTIFIER")
                continue
            break

    def assign(self):
        # ASSIGN → id "=" EXPR
        self.match("IDENTIFIER")
        # expect operator "="
        self.match("OPERATOR", "=")
        self.expr()

    def if_stmt(self):
        # IF_STMT → "if" "(" EXPR ")" STATEMENT ( "else" STATEMENT )?
        self.match("KEYWORD", "if")
        self.match("SPECIAL CHARACTER", "(")
        self.expr()
        self.match("SPECIAL CHARACTER", ")")
        self.statement()
        # optional else
        type, value = self.Read_token()
        if type == "KEYWORD" and value == "else":
            self.next_token()
            self.statement()

    def return_stmt(self):
        # RETURN → "return" EXPR
        self.match("KEYWORD", "return")
        self.expr()

    # Expressions (no precedence conflicts because we use term/expr)
    def expr(self):
        # EXPR → TERM (OP TERM)*
        self.term()
        while True:
            type, value = self.Read_token()
            if type == "OPERATOR" and value in self.OPERATORS:
                self.next_token()
                self.term()
                continue
            break

    def term(self):
        # TERM → id | number | "(" EXPR ")"
        type, value = self.Read_token()
        if type == "IDENTIFIER":
            self.next_token()
            return
        if type == "NUMBER":
            self.next_token()
            return
        if type == "SPECIAL CHARACTER" and value == "(":
            self.next_token()
            self.expr()
            self.match("SPECIAL CHARACTER", ")")
            return
        raise ParserError("Syntax error")


if __name__ == "__main__":

    sc = Scanner("main.c")
    toks = sc.scan()
    parser = Parser(toks)
    try:
        parser.parse()
        print("Compiled successfully")
    except ParserError:
        print("Syntax error")
