"""A module containing operations concerning propositional logic."""
from typing import Tuple

OPERATOR_ARITY = {"&": 2, "|": 2, "¬": 1, ">": 2, "=": 2}


class ASTNode:
    """Represents a node of an abstract syntax tree."""

    def __init__(self, symbol: str, variable: bool = False) -> None:
        self.symbol = symbol
        self.variable = variable
        self.children = []

    def __repr__(self) -> str:
        return f"{self.symbol}: {self.children}" if self.children else self.symbol


def parse_symbol(inp: str, pos: int) -> Tuple[ASTNode, int]:
    """Parses the given string from the given position."""
    if inp[pos] in OPERATOR_ARITY:
        top = ASTNode(inp[pos])
        curr = pos + 1
        for _ in range(OPERATOR_ARITY[inp[pos]]):
            temp = parse_symbol(inp, curr)
            top.children.append(temp[0])
            curr = temp[1]
        return (top, curr)
    return (ASTNode(inp[pos], True), pos + 1)


def generate_truth_table_row(num: int):
    """Returns a generator that will produce a row of inputs for a truth table."""
    count = 0
    for _ in range(2 ** num):
        count += 1
        yield [(count >> i) for i in range(num)]
