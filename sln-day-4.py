from typing import List
from collections import defaultdict
from collections.abc import Sequence

def _get_grouped_pos(coord_values, use_j=False):
    getter = lambda x: x[0]
    if use_j:
        getter = lambda x: x[1]
    
    grouped = defaultdict(list)

    for coord in coord_values:
        grouped[getter(coord)].append(coord)
    
    return grouped

def _groups_has_winning(groups):
    for g in groups:
        if not len(g) > 4:
            continue
        return True
    return False


class Board:

    def __init__(self, values:List[List[int]]):
        
        self._values = values
        
        self._value_positions = {v:(i, j) for i, l in enumerate(self._values) for j, v in enumerate(l) }
        self._drawn_positions = {}
        self._draw_history = []
        
        self._total_possible = sum([v for value_row in self._values for v in value_row])

        self._won = False
        self._winning_draw = 0

    def handle_draw(self, drawn_value:int):
        
        if self._won:
            return

        self._draw_history.append(drawn_value)
        if drawn_value not in self._value_positions:
            return

        self._drawn_positions[drawn_value] = self._value_positions[drawn_value]
        self._won = self._check_win()
        if self._won:
            self._winning_draw = drawn_value

    
    def _check_win(self):
        if self._won:
            return True

        drawn_coords = list(self._drawn_positions.values())

        grouped_i = _get_grouped_pos(drawn_coords)
        if _groups_has_winning(grouped_i.values()):
            return True

        
        grouped_j = _get_grouped_pos(drawn_coords, use_j=True)
        if _groups_has_winning(grouped_j.values()):
            return True
        
        return False

    def _unmarked_score(self):
        return self._total_possible - sum([drawn for drawn in self._drawn_positions])

    @property
    def unmarked_score(self):
        return self._unmarked_score()

    @property
    def score(self):
        return  self._unmarked_score() * self._winning_draw
    
    @property
    def has_won(self):
        return self._won

    @property
    def number_of_draws_to_win(self):
        return len(self._draw_history)

def _convert_str_row(str_row):
    return [int(c) for c in str_row]

def _parse_board_section(bs):
    splt = bs.split('\n')
    str_values = [r.split() for r in splt]
    return [_convert_str_row(str_row) for str_row in str_values]

class Parser:

    def __init__(self, file_name:str):
        with open(file_name) as f:
            self._split = f.read().split('\n\n')
    
    @property
    def draws(self):
        return [int(c) for c in self._split[0].split(',')]
    
    @property
    def board_values(self):
        board_sections = self._split[1:]
        return [_parse_board_section(bs) for bs in board_sections]

    def parsed_game(self):
        return Game(self.draws, self.board_values)

class BoardCollection(Sequence):
    
    def __init__(self, board_values):
        self._boards = [Board(bv) for bv in board_values]
        self._has_winning = False
        self._first_winning_score = -1
    
    def __len__(self):
        return len(self._boards)
    
    def __getitem__(self, idx):
        return self._boards[idx]
    
    def _check_win(self):
        for b in self._boards:  
            if not b.has_won:
                continue
            
            self._has_winning = True
            self._first_winning_score = b.score
            return
    
    def _last_won_board(self):
        return sorted([b for b in self._boards if b.has_won], key=lambda x:x.number_of_draws_to_win)[-1]
    
    def _first_won_board(self):
        return sorted([b for b in self._boards if b.has_won], key=lambda x:x.number_of_draws_to_win)[0]

    def _play_all_draws(self, draws):
        for d in draws:
            self.handle_draw(d)  

    def calculate_first_won_board(self, all_draws):
        self._play_all_draws(all_draws)
        return self._first_won_board()

    def calculate_last_won_board(self, draws):
        self._play_all_draws(draws)
        return self._last_won_board()
        

    def handle_draw(self, drawn_value):
        for b in self._boards:
            b.handle_draw(drawn_value)

        self._check_win()
    
    @property
    def has_winner(self):
        return self._has_winning
    
    @property
    def first_winning_score(self):
        if not self._has_winning:
            return -1
        return self._first_winning_score
    
    @property
    def last_won_board(self):
        return self._last_won_board()
    

class Game:

    def __init__(self, draws, board_values):
        self._draws = draws
        self._board_values = board_values

    @property
    def first_winning_board(self):
        bc = BoardCollection(self._board_values)
        return bc.calculate_first_won_board(self._draws)

    @property
    def first_winning_score(self):
        bc = BoardCollection(self._board_values)
        for d in self._draws:
            bc.handle_draw(d)
            
            if not bc.has_winner:
                continue
            
            return bc.first_winning_score

        return bc.first_winning_score
    
    @property
    def last_winning_board(self):
        bc = BoardCollection(self._board_values)
        return bc.calculate_last_won_board(self._draws)

    @property
    def last_winning_score(self):
        return self.last_winning_board.score

if __name__ == '__main__':
    game = Parser('ex-day-4.txt').parsed_game()
    print(game.first_winning_score)
    print(game.last_winning_score)

    game = Parser('input-day-4.txt').parsed_game()
    print(game.first_winning_score)
    print(game.last_winning_score)


