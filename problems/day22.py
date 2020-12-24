from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple


@dataclass
class Hands:
    player1: List[int]
    player2: List[int]

    def __hash__(self) -> int:
        return 7 * tuple(self.player1).__hash__() + 31 * tuple(self.player2).__hash__()

    def draw(self) -> Tuple[int, int]:
        return (self.player1.pop(0), self.player2.pop(0))

    def put_cards(self, player_idx: int, cards: Iterable[int]) -> None:
        self.player_hand(player_idx).extend(cards)

    def player_hand(self, player_idx: int) -> List[int]:
        return self.player1 if player_idx == 0 else self.player2

    def copy(self):
        return Hands([c for c in self.player1], [c for c in self.player2])


def parse_input(lines: List[str]) -> Hands:
    hands_idx = 0
    hands = [[], []]
    for line in lines:
        if line.strip() == '' or line.strip() == 'Player 1:':
            continue
        elif line.strip() == 'Player 2:':
            hands_idx = 1
        else:
            hands[hands_idx].append(int(line.strip()))
    return Hands(hands[0], hands[1])


def play_pt1_game(hands: Hands) -> Tuple[int, Hands]:
    while len(hands.player1) > 0 and len(hands.player2) > 0:
        p1card, p2card = hands.draw()
        if p1card > p2card:
            hands.put_cards(0, [p1card, p2card])
        else:
            hands.put_cards(1, [p2card, p1card])
    winner_index = 0 if len(hands.player1) > 0 else 1
    return winner_index, hands


def get_score(hand: List[int]) -> int:
    return sum([(i + 1) * v for i,v in enumerate(reversed(hand))])


def part1(starting_hands: Hands) -> int:
    winner, final_hands = play_pt1_game(starting_hands)
    return get_score(final_hands.player_hand(winner))


def play_pt2_game(hands: Hands, depth: int = 0) -> Tuple[int, Hands]:
    prev_hands = set()
    while len(hands.player1) > 0 and len(hands.player2) > 0:
        # Infinite game break
        if hands in prev_hands:
            # Player 1 wins
            return 0, hands
        prev_hands.add(hands.copy())
        hands = hands.copy()

        p1card, p2card = hands.draw()
        if len(hands.player1) >= p1card and len(hands.player2) >= p2card:
            # Recursive round
            rec_hands = Hands([c for c in hands.player1[:p1card]], [c for c in hands.player2[:p2card]])
            round_winner, _ = play_pt2_game(rec_hands, depth + 1)
            used_cards = [p1card, p2card] if round_winner == 0 else [p2card, p1card]
            hands.put_cards(round_winner, used_cards)
        else:
            # Non-recursive round
            if p1card > p2card:
                hands.put_cards(0, [p1card, p2card])
            else:
                hands.put_cards(1, [p2card, p1card])
    
    winner_index = 0 if len(hands.player1) > 0 else 1
    return winner_index, hands



def part2(starting_hands: Hands) -> int:
    winner, final_hands = play_pt2_game(starting_hands)
    return get_score(final_hands.player_hand(winner))