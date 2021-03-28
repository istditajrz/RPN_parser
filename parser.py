"""A module containing operations concerning propositional logic."""
from typing import Tuple
from itertools import product

OPERATOR_ARITY = {"&": 2, "|": 2, "¬": 1, ">": 2, "=": 2}

class ASTNode:
    """Represents a node of an abstract syntax tree."""

    def __init__(self, symbol: str, variable: bool = False) -> None:
        self.symbol = symbol
        self.variable = variable
        self.children = []

    def __repr__(self) -> str:
        return f"{self.symbol}: {self.children}" if self.children else self.symbol


def parse_symbol(inp: str, pos: int = 0) -> Tuple[ASTNode, int]:
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


def generate_truth_table_inputs(num: int):
    """Returns inputs for a truth table."""
    res = []
    for i in product([0, 1], repeat=num):
        res.append(i)
    return res

def generate_variables(expr: ASTNode):
    if expr.variable:
        return expr.symbol
    variables = []
    for child in expr.children:
        temp = generate_variables(child)
        for i in temp:
            variables.append(i)
    return variables

def eval_expr(expr: ASTNode, inputs: dict[str, int]):
    for i in expr.children:
        if i.symbol in list(OPERATOR_ARITY):
            i.symbol = eval_expr(i, inputs)
        elif not isinstance(i.symbol, int):
            i.symbol = inputs[i.symbol]
    if expr.symbol == "&":
        return int(expr.children[0].symbol and expr.children[1].symbol)
    if expr.symbol == "|":
        return int(expr.children[0].symbol or expr.children[1].symbol)
    if expr.symbol == "¬":
        return int(not expr.children[0].symbol)
    if expr.symbol == ">":
        return int(not(expr.children[0].symbol) or expr.children[1].symbol)
    if expr.symbol == "=":
        return int( ( not( expr.children[0].symbol ) or expr.children[1].symbol ) and ( not( expr.children[1].symbol ) or expr.children[0].symbol ) )
    return expr.symbol


def generate_truth_table(expr: ASTNode):
    variables = generate_variables(expr)
    print(variables)
    inputs = generate_truth_table_inputs(len(variables))
    print(inputs)
    variables_assigned = [{variables[n]: i[n] for n in range(len(variables))} for i in inputs]
    print(variables_assigned)
    for i in variables_assigned:
        print(eval_expr(expr, i))
        
    


generate_truth_table(parse_symbol("&|pq¬r")[0])