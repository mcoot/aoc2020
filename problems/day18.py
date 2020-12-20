from dataclasses import dataclass
from typing import List

## Grammar Pt1
#
# Galaxy brain: we need left-associativity, but ops are commutative
# So I'm reversing the expression and then using a right-associative 
# recursive descent parser
#
# So this grammar is right-associative
#
# Expr := Value {Operator Expr}
# Value := intvalue | lparen Expr rparen
#
#
## Grammar Pt2
# Precedence of + and * reversed lol
#
# Expr := Term {* Expr}
# Term := Value {+ Term}
# Value := intvalue | lparen Expr rparen

# Tokens

@dataclass
class Token:
    def is_literal(self) -> bool:
        return isinstance(self, IntToken)

    def is_plus(self) -> bool:
        return isinstance(self, OpToken) and self.operator == '+'

    def is_mult(self) -> bool:
        return isinstance(self, OpToken) and self.operator == '*'

    def is_operator(self) -> bool:
        return self.is_plus() or self.is_mult()

    def is_lparen(self) -> bool:
        return isinstance(self, ParenToken) and self.is_left

    def is_rparen(self) -> bool:
        return isinstance(self, ParenToken) and not self.is_left

@dataclass
class IntToken(Token):
    value: int

@dataclass
class OpToken(Token):
    operator: str

@dataclass
class ParenToken(Token):
    is_left: bool


# AST

@dataclass
class Expr:
    def eval(self) -> int:
        raise ValueError('Cannnot eval base Expr')


@dataclass
class IntExpr(Expr):
    val: int

    def eval(self) -> int:
        return self.val

@dataclass
class OpExpr(Expr):
    op: str
    lhs: Expr
    rhs: Expr

    def eval(self) -> int:
        lhs_val = self.lhs.eval()
        rhs_val = self.rhs.eval()
        if self.op == '+':
            return lhs_val + rhs_val
        elif self.op == '*':
            return lhs_val * rhs_val
        else:
            raise ValueError(f'Invalid operator {self.op}')


def build_token(token: str) -> Token:
    if token.isdigit():
        return IntToken(int(token))
    elif token.startswith('('):
        return ParenToken(True)
    elif token.startswith(')'):
        return ParenToken(False)
    elif len(token) > 0:
        return OpToken(token)
    else:
        raise ValueError(f'Cannot tokenise empty token')


def tokenise(line: str) -> List[Token]:
    tokens = []
    cur_token = ''
    remaining_chars = [c for c in line.strip()]
    while len(remaining_chars) > 0:
        c = remaining_chars.pop(0)
        if c == ' ':
            # If we have something to build, build it
            # If we're after a right-brace we may have nothing
            if len(cur_token) > 0:
                tokens.append(build_token(cur_token))
            cur_token = ''
        elif c == '(':
            # Open paren; should always be a fresh token (after a space or another open paren)
            tokens.append(build_token('('))
            cur_token = ''
        elif c == ')':
            # End paren, we may have an existing operand token to complete
            if len(cur_token) > 0:
                tokens.append(build_token(cur_token))
            tokens.append(build_token(')'))
            cur_token = ''
        else:
            cur_token += c
    # Build the final token
    if len(cur_token) > 0:
        tokens.append(build_token(cur_token))
    return tokens


def parse_input(lines: List[str]) -> List[List[Token]]:
    # Precedence might change so parse per-part
    # Just tokenise here
    return [tokenise(line.strip()) for line in lines if not line.strip().startswith('#')]


@dataclass
class Parser:
    tokens: str

    def finished_input(self) -> bool:
        return len(self.tokens) == 0

    def consume_token(self) -> Token:
        if self.finished_input():
            raise ValueError(f'Cannot consume token, input finished')
        return self.tokens.pop(0)

    def lookahead(self) -> Token:
        if self.finished_input():
            raise ValueError(f'Cannot lookahead, input finished')
        return self.tokens[0]

    def consume_paren_block(self) -> List[Token]:
        # Check we are at an lparen
        lparen_token = self.consume_token()
        if not lparen_token.is_lparen():
            raise ValueError(f'Expected lparen token, got {lparen_token}')
        paren_indent = 1
        consumed = []
        while paren_indent > 0:
            cur_token = self.consume_token()
            if cur_token.is_lparen():
                paren_indent += 1
            elif cur_token.is_rparen():
                paren_indent -= 1
            if paren_indent > 0:
                consumed.append(cur_token)
        return consumed

    # Value parsing common between parts
    def parse_value(self) -> Expr:
        next_token = self.lookahead()
        if next_token.is_literal():
            return IntExpr(self.consume_token().value)
        elif next_token.is_lparen():
            paren_block = self.consume_paren_block()
            subparser = self.__class__(paren_block)
            return subparser.parse()
        else:
            raise ValueError(f'Parse error at {next_token}; remaining {tokens}')

    # Abstract main parse function
    def parse(self):
        raise Exception('Expected parser subclass')


@dataclass
class Part1Parser(Parser):
    def parse_expr(self):
        lhs = self.parse_value()

        # Base case
        if self.finished_input():
            return lhs

        # Recursive case: operator and then right-assoc expression
        operator_token = self.consume_token()
        if not operator_token.is_operator():
            raise ValueError(f'Parsing error: expected operator, got {operator_token}; remaining {self.tokens}')

        rhs = self.parse_expr()

        return OpExpr(operator_token.operator, lhs, rhs)

    def parse(self):
        return self.parse_expr()
        

def reverse_paren_token(token: Token) -> Token:
    if isinstance(token, ParenToken):
        return ParenToken(not token.is_left)
    return token


# Galaxy brain: ops are commutative
# The parser here is right-associative
# So just reverse the expression, properly reversing parens
def reverse_tokens(tokens: List[Token]) -> List[Token]:
    return [reverse_paren_token(t) for t in reversed(tokens)]


def part1(tokenised_exprs: List[List[Token]]):
    tokenised_exprs = [reverse_tokens(tokens) for tokens in tokenised_exprs]
    exprs = [Part1Parser(tokens).parse() for tokens in tokenised_exprs]
    results = [expr.eval() for expr in exprs]
    return sum(results)


@dataclass
class Part2Parser(Parser):
    def parse_expr(self):
        lhs = self.parse_term()

        # Base case: no further tokens, i.e. no more operators
        if self.finished_input():
            return lhs

        # Recursive case: operator and then right-assoc expression
        operator_token = self.consume_token()
        if not operator_token.is_mult():
            raise ValueError(f'Parsing error: expected mult, got {operator_token}; remaining {self.tokens}')

        rhs = self.parse_expr()

        return OpExpr(operator_token.operator, lhs, rhs)

    def parse_term(self):
        lhs = self.parse_value()

        # Base case: no further tokens, or next token is a mult
        if self.finished_input() or self.lookahead().is_mult():
            return lhs

        # Recursive case: operator and then right-assoc expression
        operator_token = self.consume_token()
        if not operator_token.is_plus():
            raise ValueError(f'Parsing error: expected plus, got {operator_token}; remaining {self.tokens}')

        rhs = self.parse_term()

        return OpExpr(operator_token.operator, lhs, rhs)

    def parse(self):
        return self.parse_expr()


def part2(tokenised_exprs: List[List[Token]]):
    tokenised_exprs = [reverse_tokens(tokens) for tokens in tokenised_exprs]
    exprs = [Part2Parser(tokens).parse() for tokens in tokenised_exprs]
    results = [expr.eval() for expr in exprs]
    return sum(results)