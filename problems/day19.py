from dataclasses import dataclass
import sys
from typing import Dict, List


@dataclass
class Rule:
    address: int

    def is_literal(self):
        return isinstance(self, LiteralRule)

    def is_reference(self):
        return isinstance(self, ReferenceRule)

    def is_concat(self):
        return isinstance(self, ConcatRule)

    def is_alternation(self):
        return isinstance(self, AlternationRule)


@dataclass
class LiteralRule(Rule):
    literals: List[str]


@dataclass
class ReferenceRule(Rule):
    ref_to: int


@dataclass
class ConcatRule(Rule):
    rules: List[Rule]


@dataclass
class AlternationRule(Rule):
    alternatives: List[Rule]


@dataclass
class Data:
    rules: Dict[int, Rule]
    messages: List[str]


def parse_concat_rule(address: int, body: str) -> Rule:
    refs = [ReferenceRule(address, int(ref)) for ref in body.split(" ")]
    if len(refs) == 1:
        return refs[0]
    return ConcatRule(address, refs)


def parse_alt_rule(address: int, body: str) -> Rule:
    alts = [parse_concat_rule(address, alt.strip()) for alt in body.split("|")]
    if len(alts) == 1:
        return alts[0]
    return AlternationRule(address, alts)


def parse_rule(line: str) -> Rule:
    splt = line.split(':')
    address = int(splt[0])
    body = splt[1].strip()

    if body.startswith("\""):
        return LiteralRule(address, [body[1:-1]])
    return parse_alt_rule(address, body)


def parse_input(lines) -> Data:
    rules = dict()
    messages = []
    finished_rules = False
    for line in lines:
        if line.strip() == '':
            finished_rules = True
            continue
        if finished_rules:
            if not line.strip().startswith('#'):
                messages.append(line.strip())
        else:
            cur_rule = parse_rule(line.strip())
            rules[cur_rule.address] = cur_rule
    return Data(rules, messages)


@dataclass
class Rules:
    rules: Dict[int, Rule]


@dataclass
class RulesMatcher(Rules):
    message: List[str]
    verbose_log: bool = False
    depth: int = 0

    def log(self, msg: str, verbose_only: bool = True):
        if verbose_only and not self.verbose_log:
            return
        indent = self.depth * '..'
        print(f'{indent}{msg}')

    def log_rule(self, rule: Rule):
        return self.log(''.join(self.message))

    def log_result(self, result: bool):
        return self.log('[MATCH]' if result else '[FAIL]')

    def match_literal(self, rule: LiteralRule) -> bool:
        for literal in rule.literals:
            if len(literal) > len(self.message):
                continue
            if literal == ''.join(self.message[0:len(literal)]):
                # Consume the chars
                self.message = self.message[len(literal):]
                return True
        return False

    def match_reference(self, rule: ReferenceRule) -> bool:
        self.depth += 1
        result = self.match_recursive(self.rules[rule.ref_to])
        self.depth -= 1
        return result

    def match_concat(self, rule: ConcatRule) -> bool:
        self.depth += 1
        result = True
        for subrule in rule.rules:
            if not self.match_recursive(subrule):
                result = False
                break
        self.depth -= 1
        return result

    def match_alternation(self, rule: AlternationRule) -> bool:
        starting_message = self.message.copy()
        self.depth += 1
        result = False
        for subrule in rule.alternatives:
            if self.match_recursive(subrule):
                result = True
                break
            else:
                # Put back the characters we consumed
                self.message.clear()
                for c in starting_message:
                    self.message.append(c)
        self.depth -= 1
        return result

    def match_recursive(self, rule: Rule) -> bool:
        self.log_rule(rule)
        result = False
        if rule.is_literal():
            result = self.match_literal(rule)
        elif rule.is_reference():
            result = self.match_reference(rule)
        elif rule.is_concat():
            result = self.match_concat(rule)
        elif rule.is_alternation():
            result = self.match_alternation(rule)
        else:
            raise ValueError(f'Unknown rule {rule}')
        self.log_result(result)
        return result
        
    def match(self, rule: Rule) -> bool:
        does_match = self.match_recursive(rule)
        # Only match if we didn't leave any remaining input
        return does_match and len(self.message) == 0


def match_message(rules: Dict[str, Rule], message: str) -> bool:
    return RulesMatcher(rules, [c for c in message]).match(rules[0])


def part1(data: Data):
    results = [match_message(data.rules, message) for message in data.messages]
    return sum(results)


# Flatten out a rule into an alternation of literals
# Obvs won't work with a looping rule
@dataclass
class RuleFlattener(Rules):

    def flatten_literal(self, address: int, rule: LiteralRule) -> LiteralRule:
        return LiteralRule(address, rule.literals)

    def flatten_reference(self, address: int, rule: ReferenceRule) -> LiteralRule:
        return self.flatten(address, self.rules[rule.ref_to])

    def flatten_concat(self, address: int, rule: ConcatRule) -> LiteralRule:
        subresults = []
        for subrule in rule.rules:
            subresults.append(self.flatten(address, subrule))
        literals = subresults[0].literals.copy()
        for subresult in subresults[1:]:
            literals = [x + y for x in literals for y in subresult.literals]
        return LiteralRule(address, literals)

    def flatten_alternation(self, address: int, rule: AlternationRule) -> LiteralRule:
        results = []
        for subrule in rule.alternatives:
            results.append(self.flatten(address, subrule))
        return LiteralRule(address, [l for r in results for l in r.literals])
    
    def flatten(self, address: int, rule: Rule) -> LiteralRule:
        if rule.is_literal():
            return self.flatten_literal(address, rule)
        elif rule.is_reference():
            return self.flatten_reference(address, rule)
        elif rule.is_concat():
            return self.flatten_concat(address, rule)
        elif rule.is_alternation():
            return self.flatten_alternation(address, rule)
        else:
            raise ValueError(f'Unknown rule {rule}')


class Part2RulesMatcher(RulesMatcher):
    def match_recursive(self, rule: Rule) -> bool:
        # Special case of rule 11
        # Match an equal number of 42s and 31s
        if rule.address == 11:
            # We need at least one 42
            if not self.match_recursive(self.rules[42]):
                return False
            num_42s = 1
            while True:
                message_before_lookahead = self.message.copy()
                # Can we match a 42 next?
                second_match = self.match_recursive(self.rules[42])
                if second_match:
                    # Keep going
                    num_42s += 1
                else:
                    # No longer matching 42s
                    # Restore the characters we consumed in the last attempt
                    self.message = message_before_lookahead
                    break
            
            # Should match at least one 31
            if not self.match_recursive(self.rules[31]):
                return False
            num_31s = 1
            # Now keep matching 31s
            while True:
                if not self.match_recursive(self.rules[31]):
                    break
                num_31s += 1
            # There should not be more 31s than 42s matched
            return num_31s <= num_42s
        else:
            return super().match_recursive(rule)


def match_message_part2(rules: Dict[str, Rule], message: str) -> bool:
    return Part2RulesMatcher(rules, [c for c in message]).match(rules[0])


def part2(data: Data):
    # Rule 8 and 11 are not referenced anywhere but the top level
    # and only in the configuration 0: 8 11
    # Rule 8 is just rule 42 repeated at least once
    # Rule 11 is rule 42 repeated at least once, followed by the same number of rule 31s
    # Since 8 is always followed by 11, we can consider them together
    # Because 8 can result in any number of 42s
    # and 11 requires == numbers of 42s : 31s
    # the effect is N 42s and M 31s, with N >= 2 and 1 <= M < N
    # Refactor this for convenience into a rule 8 which is just a single 42
    # Now rule 11 is N 42s and M 31s, with N >= 1 and 1 <= M <= N

    # Don't bother with the recursive case in rule 8
    data.rules[8] = parse_rule('8: 42')
    # We will use a special rule to check rule 11 to lookahead
    data.rules[11] = parse_rule('11: 42 31 | 42 11 31')

    flattener = RuleFlattener(data.rules)
    data.rules[42] = flattener.flatten(42, data.rules[42])
    data.rules[31] = flattener.flatten(31, data.rules[31])
    
    # print()
    results = [match_message_part2(data.rules, message) for message in data.messages]
    # print([(data.messages[i], results[i]) for i in range(len(results))])
    return sum(results)