class Scanner:
    KEYWORDS = {
        "main", "int", "float", "double", "char", "if", "else",
        "return", "while", "for", "do", "break", "continue", "void"
    }

    OPERATORS = {
        '+', '-', '*', '/', '%',
        '=', '+=', '-=', '*=', '/=', '%=',
        '==', '!=', '<', '>', '<=', '>=',
        '&&', '||',
        '&', '|', '^', '~', '<<', '>>',
        '++', '--'
    }

    SPECIAL_CHARS = {'(', ')', '{', '}', '[', ']', ';', ',', '"', "'", "$", "@"}

    def __init__(self, filename):
        self.filename = filename

    def scan(self):
        tokens = []

        with open(self.filename, "r") as f:
            code = f.read()

        i = 0
        n = len(code)

        while i < n:
            c = code[i]

            # Ignore whitespace
            if c.isspace():
                i += 1
                continue

            # Line comment
            if c == '/' and i + 1 < n and code[i + 1] == '/':
                i += 2
                while i < n and code[i] != '\n':
                    i += 1
                continue

            # Block comment
            if c == '/' and i + 1 < n and code[i + 1] == '*':
                i += 2
                while i + 1 < n and not (code[i] == '*' and code[i + 1] == '/'):
                    i += 1
                i += 2
                continue

            # Identifier or Keyword
            if c.isalpha() or c == '_':
                start = i
                i += 1
                while i < n and (code[i].isalpha() or code[i] == '_' or code[i].isdigit()):
                    i += 1
                value = code[start:i]
                if value in self.KEYWORDS:
                    tokens.append(f"<KEYWORD, {value}>")
                else:
                    tokens.append(f"<IDENTIFIER, {value}>")
                continue

            # Number (int or float)
            if c.isdigit():
                start = i
                i += 1
                is_float = False
                while i < n and (code[i].isdigit() or code[i] == '.'):
                    if code[i] == '.':
                        is_float = True
                    i += 1
                value = code[start:i]
                tokens.append(f"<NUMBER, {value}>")
                continue

            # Operators (two-char)
            if i + 1 < n and code[i:i + 2] in self.OPERATORS:
                tokens.append(f"<OPERATOR, {code[i:i + 2]}>")
                i += 2
                continue

            # Operators (single-char)
            if c in self.OPERATORS:
                tokens.append(f"<OPERATOR, {c}>")
                i += 1
                continue

            # Special characters
            if c in self.SPECIAL_CHARS:
                tokens.append(f"<SPECIAL CHARACTER, {c}>")
                i += 1
                continue

            # Unexpected character
            print(f"Error: Unexpected character: {c}")
            i += 1

        return tokens
if __name__ == "__main__":
    scanner = Scanner("main.c")
    tokens = scanner.scan()

    for t in tokens:
        print(t)
