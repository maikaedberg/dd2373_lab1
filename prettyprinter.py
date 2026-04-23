from parser import (
    RegExp, Dot, Literal, Closure,
    OneOrMore, ZeroOrOne, Concatenation, Union
)

def pretty_format(expr: RegExp) -> str:
    if isinstance(expr, Literal):
        return expr.char

    elif isinstance(expr, Dot):
        return "."

    elif isinstance(expr, Union):
        return f"({pretty_format(expr.left)}|{pretty_format(expr.right)})"

    elif isinstance(expr, Concatenation):
        return f"({pretty_format(expr.left)}{pretty_format(expr.right)})"

    elif isinstance(expr, Closure):
        return f"({pretty_format(expr.expr)}*)"

    elif isinstance(expr, OneOrMore):
        return f"({pretty_format(expr.expr)}+)"

    elif isinstance(expr, ZeroOrOne):
        return f"({pretty_format(expr.expr)}?)"

    else:
        raise ValueError(f"Unknown RegExp node: {expr}")

def pretty_print(expr: RegExp) -> None:
    pretty_str = pretty_format(expr)
    print(pretty_str)