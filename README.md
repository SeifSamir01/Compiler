# Compiler design


# Mini C-Like Compiler (Scanner + Recursive Descent Parser)**

## 📌 **Project Overview**

This project implements a **simple compiler** for a small subset of the C language.
It contains **two main modules**:

1. **Scanner**:
   Converts raw code (plain text) into a list of tokens such as
   `<KEYWORD, int>`, `<IDENTIFIER, x>`, `<NUMBER, 42>`, `<OPERATOR, ==>`, etc.

2. **Recursive Descent Parser**:
   Takes the tokens produced by the scanner and checks if the program follows the grammar rules.
   It outputs one of the following:

   * `Compiled successfully`
   * `Syntax error`

This project does **not** generate machine code or intermediate representation — it only validates syntax.

---

## 📌 **Files Included**

| File              | Description                                        |
| ----------------- | -------------------------------------------------- |
| `scanner.py`      | Converts input source code (`.c` file) into tokens |
| `parser.py`       | Performs syntax analysis using recursive descent   |
| `main.c` (sample) | Example program used as input                      |

---

# 📘 **Grammar Used in the Parser**

This is the exact grammar implemented:

```
PROGRAM        → FUNC

FUNC           → "int" "main" "(" ")" BLOCK

BLOCK          → "{" STATEMENTS "}"

STATEMENTS     → STATEMENT STATEMENTS | ε

STATEMENT      → DECLARATION ";"
               | ASSIGN ";"
               | IF_STMT
               | RETURN ";"
               | BLOCK

DECLARATION    → TYPE ID_LIST
TYPE           → "int" | "float" | "double" | "char"
ID_LIST        → id ("," id)*

ASSIGN         → id "=" EXPR

IF_STMT        → "if" "(" EXPR ")" STATEMENT
               | "if" "(" EXPR ")" STATEMENT "else" STATEMENT

RETURN         → "return" EXPR

EXPR           → TERM (OP TERM)*

TERM           → id | number | "(" EXPR ")"
```

---

# 🔍 **Scanner Description**

The scanner recognizes:

### **Keywords**

```
main, int, float, double, char, if, else, return,
while, for, do, break, continue, void
```

### **Operators**

Supports **single** and **multi-character** operators such as:

```
+, -, *, /, %, =, +=, -=, *=, /=, ==, !=, <, >, <=, >=,
&&, ||, &, |, ^, ~, <<, >>, ++, --
```

### **Special Characters**

```
( ) { } [ ] ; , " ' $ @
```

### **Comments**

* `// single-line comment`
* `/* multi-line comment */`

---

# ⚠️ **Note About Scanner Modifications**

A small modification was made to the scanner to simplify integration with the parser.
Because of this, some parts of the original scanner were removed/rewritten,
which is why the old scanner file was deleted.

The current version is fully compatible with the parser in this project.

---

# 📄 **Sample Input (`main.c`)**

This example demonstrates declarations, comments, if/else, arithmetic, and return:

```c
int main() {
    int x,y;
    // This is a single-line comment
    if (x == 42) {
        /* This is
           a block
           comment */
        x = x-3;
    } else {
        y = 3.1; // Another comment
    }
    return 0;
}
```

---

# 🚀 **How to Run**

1. Place `scanner.py`, `parser.py`, `main.c` in one project directory.
2. Run:

```
python parser.py
```

3. Output will be either:

```
Compiled successfully
```

or

```
Syntax error
```
---
# 🧐 **How to see tokens(Optional)**
1. Run:
```
scanner.py
```
---

# 📌 **Project Purpose**

This project demonstrates:

* Tokenization
* Lexical analysis
* Grammar design
* Recursive descent parsing
* Error detection in source code
  
---
