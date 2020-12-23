from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
import re
from typing import Dict, Iterable, List, Set, Tuple


PLAYER_START_RE = re.compile(r'^Player (\d+):$')


def parse_input(lines: List[str]) -> Dict[int, List[int]]:
    result = defaultdict(list)

    current_player = None
    for line in lines:
        if line.strip() == '':
            continue

        m = PLAYER_START_RE.match(line.strip())
        if m:
            current_player = int(m.group(1))
            continue
        
        result[current_player].append(int(line.strip()))

    return result



max_used_game_id = 1


@dataclass
class GameState:
    hands: Dict[int, List[int]]
    prev_hands: List[Dict[int, List[int]]]
    game_number: int = 1
    round_number = 1
    winner: int = None
    parent = None

    def players(self) -> Iterable[int]:
        return self.hands.keys()

    def get_hand(self, player: int) -> List[int]:
        return self.hands[player]

    def play_card(self, player: int) -> int:
        return self.hands[player].pop(0)

    def put_cards(self, player: int, cards: Iterable[int]):
        self.hands[player].extend(cards)

    def draw_current_trick(self) -> List[Tuple[int, int]]:
        self.round_number += 1
        return list(reversed(sorted([(player, self.play_card(player)) for player in self.players()], key=lambda c: c[1])))

    def get_trick_winner(self, trick: List[Tuple[int, int]]) -> Tuple[int, int]:
        return trick[0]

    def record_hands(self):
        self.prev_hands.append(deepcopy(self.hands))

    def are_current_hands_duplicate(self):
        return self.hands in self.prev_hands
    
    def finish_game(self, winning_player: int):
        self.winner = winning_player

    def is_finished(self):
        return self.winner is not None

    def gen_recursive_state(self, drawn_trick: Dict[int, int]):
        global max_used_game_id
        max_used_game_id += 1
        new_hands = dict()
        for p, hand in self.hands.items():
            num_cards = drawn_trick[p]
            new_hands[p] = hand[:num_cards].copy()
        recursive_state = GameState(new_hands, [], max_used_game_id)
        recursive_state.parent = self
        return recursive_state


def check_pt1_winner(state: GameState):
    found_winner = None
    for player in state.players():
        if len(state.get_hand(player)) > 0:
            if found_winner:
                # Game not over
                return None
            else:
                found_winner = player
    if found_winner:
        state.finish_game(found_winner)


def play_pt1_round(state: GameState) -> None:
    if state.is_finished():
        return

    # Take the top card of each player
    trick = state.draw_current_trick()
    winner, _ = state.get_trick_winner(trick)
    # Put trick cards onto the bottom of the winner's hand
    state.put_cards(winner, (c[1] for c in trick))

    # Check if the game is over
    check_pt1_winner(state)


def get_score(hand: List[int]) -> int:
    return sum((i + 1) * v for (i, v) in enumerate(reversed(hand)))


def part1(starting_hands: Dict[int, List[int]]) -> int:
    state = GameState(starting_hands, [])
    while not state.is_finished():
        play_pt1_round(state)
    
    return get_score(state.get_hand(state.winner))


VERBOSE_LOG = True


def play_pt2_round(state: GameState) -> None:
    if VERBOSE_LOG:
        print()
        print(f'-- Round {state.round_number} (Game {state.game_number}) --')
        for i in [1, 2]:
            cur_hand = ', '.join(str(c) for c in state.get_hand(i))
            print(f'Player {i}\'s deck: {cur_hand}')
    if state.are_current_hands_duplicate():
        # Infinite game break
        print(f'Breaking up game as it would go infinitely')
        state.finish_game(1)
        return
    state.record_hands()
    trick = state.draw_current_trick()
    trick_dict = {p: c for p, c in trick}
    if VERBOSE_LOG:
        for i in [1, 2]:
            print(f'Player {i} plays: {trick_dict[i]}')
    should_recurse = all([c <= len(state.get_hand(p)) for p, c in trick_dict.items()])
    # Determine winner of the round
    if should_recurse:
        recursive_state = state.gen_recursive_state(trick_dict)
        if VERBOSE_LOG:
            print('Playing a sub-game to determine the winner...\n')
        play_pt2_game(recursive_state)
        # The winner of the sub-game wins this trick
        winner = recursive_state.winner
        winning_card = trick_dict[winner]
    else:
        winner, winning_card = state.get_trick_winner(trick)

    if VERBOSE_LOG:
        print(f'Player {winner} wins round {state.round_number - 1} of game {state.game_number}!')

    # Ensure winning card is on top of the trick
    trick.remove((winner, winning_card))
    trick.insert(0, (winner, winning_card))

    # Put trick cards onto the bottom of the winner's hand
    state.put_cards(winner, (c[1] for c in trick))

    # Check if the game is over
    check_pt1_winner(state)


def play_pt2_game(state: GameState) -> None:
    if VERBOSE_LOG:
        print(f'=== Game {state.game_number} ===')
    while not state.is_finished():
        play_pt2_round(state)
    if VERBOSE_LOG:
        print(f'The winner of game {state.game_number} is player {state.winner}!')
        if state.parent:
            print(f'\n...anyway, back to game {state.parent.game_number}.')


def part2(starting_hands: Dict[int, List[int]]):
    state = GameState(starting_hands, [])
    play_pt2_game(state)
    if VERBOSE_LOG:
        print('\n\n== Post-game results ==')
        for i in [1, 2]:
            cur_hand = ', '.join(str(c) for c in state.get_hand(i))
            print(f'Player {i}\'s deck: {cur_hand}')
    return get_score(state.get_hand(state.winner))