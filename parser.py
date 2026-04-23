from dataclasses import dataclass

# ===== RegExp AST =====
class RegExp:
    pass

@dataclass
class Dot(RegExp):
    pass

@dataclass
class Literal(RegExp):
    char: str

@dataclass
class Closure(RegExp):
    expr: RegExp

@dataclass
class OneOrMore(RegExp):
    expr: RegExp

@dataclass
class ZeroOrOne(RegExp):
    expr: RegExp

@dataclass
class Concatenation(RegExp):
    left: RegExp
    right: RegExp

@dataclass
class Union(RegExp):
    left: RegExp
    right: RegExp


# ===== Parser =====
class ParserError(Exception):
    pass


class Parser:
    def __init__(self, s: str):
        self.s = s
        self.i = 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None

    def consume(self, c=None):
        if self.i >= len(self.s):
            raise ParserError("Unexpected EOF")
        ch = self.s[self.i]
        if c and ch != c:
            raise ParserError(f"Expected '{c}', got '{ch}'")
        self.i += 1
        return ch

    def eof(self):
        return self.i >= len(self.s)

    # ===== Grammar =====

    def parse_expr(self):
        return self.parse_union()

    def parse_union(self):
        parts = [self.parse_concatenation()]
        while self.peek() == '|':
            self.consume('|')
            parts.append(self.parse_concatenation())

        expr = parts[0]
        for p in parts[1:]:
            expr = Union(expr, p)
        return expr

    def parse_concatenation(self):
        expr = self.parse_expr_post()
        while True:
            ch = self.peek()
            if ch is None or ch in '|)':
                break
            next_expr = self.parse_expr_post()
            expr = Concatenation(expr, next_expr)
        return expr

    def parse_expr_post(self):
        expr = self.parse_expr1()
        ch = self.peek()

        if ch == '*':
            self.consume('*')
            return Closure(expr)
        elif ch == '+':
            self.consume('+')
            return OneOrMore(expr)
        elif ch == '?':
            self.consume('?')
            return ZeroOrOne(expr)
        else:
            return expr

    def parse_expr1(self):
        ch = self.peek()

        if ch == '(':
            return self.parse_paren()
        elif ch == '.':
            self.consume('.')
            return Dot()
        elif ch is not None and ch not in ['.', '|', '*', '+', '?', '(', ')']:
            return Literal(self.consume())
        else:
            raise ParserError(f"Unexpected character: {ch}")

    def parse_paren(self):
        self.consume('(')
        expr = self.parse_expr()
        self.consume(')')
        return expr


# ===== Entry point =====
def parse_regexp(s: str) -> RegExp:
    try:
        parser = Parser(s)
        result = parser.parse_expr()
        if not parser.eof():
            raise ParserError("Trailing input")
        return result
    except ParserError:
        raise  ValueError(f"invalid regexp, {s}")