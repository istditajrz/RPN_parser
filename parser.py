from typing import Tuple
import pprint
OPERATOR_ARITY = {"&": 2, "|": 2, "¬": 1, ">": 2, "=": 2}

class syntax_tree:
    def __init__(self, symbol: str, variable: bool = False) -> None:
        self.symbol = symbol
        self.variable = variable
        self.children = []
    
    def __repr__(self) -> str:
        if self.children:
            return f"{self.symbol}: {self.children}"
        else:
            return f"{self.symbol}"

def parse_symbol(inp: str, pos: int) -> Tuple[syntax_tree, int]:
    if inp[pos] in OPERATOR_ARITY:
        top = syntax_tree(inp[pos])
        curr = pos + 1
        for _ in range(OPERATOR_ARITY[inp[pos]]):
            temp = parse_symbol(inp, curr)
            if isinstance(temp, tuple):
                top.children.append(temp[0]); curr = temp[1]
            else:
                top.children.append(temp)
        return tuple([top, curr])
    else:
        return syntax_tree(inp[pos], True)
    
def generate_binary(num: int):
    res = []
    p = 0
    for _ in range(2 ** num):
        p += 1
        yield [(p >> i) for i in range(num)]

pprint.pprint(parse_symbol("&|pq¬r", 0)[0])