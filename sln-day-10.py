import typing


def get_lines(file_name:str):
    with open(file_name) as f:
        return [l.strip() for l in f.readlines()]


EX = 'ex-day-10.txt'
IN = 'input-day-10.txt'

SCORE_CORRUPT_DICT = {
    ')': 3,
    ']' : 57,
    '}': 1197,
    '>': 25_137
}

SCORE_INCOMPLETE_DICT = {
    ')': 1,
    ']' : 2,
    '}': 3,
    '>': 4
}

PAIR_DICT = {
    '{': '}',
    '[' : ']',
    '(' : ')',
    '<' : '>',
}

OPEN_SET = set(PAIR_DICT.keys())


class ParseResult:

    def __init__(self, line:str, corrupted_char:str = None, remaining:typing.List[str] = None):
        self._line = line
        self._corrupted_char = corrupted_char
        self._remaining = remaining

    @property
    def is_corrupt(self):
        return self._corrupted_char is not None
    
    @property
    def score(self):
        if self.is_corrupt:
            return SCORE_CORRUPT_DICT[self._corrupted_char]
        
        if not self.is_incomplete:
            return 0
        
        score = 0

        rem = self._remaining[:]
        while len(rem) != 0:
            score *= 5
            score += SCORE_INCOMPLETE_DICT[PAIR_DICT[rem.pop()]]
        
        return score
    
    @property
    def is_incomplete(self):
        return self._remaining is not None
    
    
class LineParser:

    def __init__(self, line:str):
        self._l = line
    
    def parse(self):
        pos = 0
        open_stack = []

        while pos < len(self._l):
            c = self._l[pos]
            pos+= 1
            
            if c in OPEN_SET:
                open_stack.append(c)
                continue
            
            if PAIR_DICT[open_stack[-1]] != c:
                return ParseResult(self._l, c)
            
            open_stack.pop()
        
        return ParseResult(self._l, None, open_stack)
    
def part_1():
    lines = get_lines(IN)
    parsers = [LineParser(l) for l in lines]
    parse_results = [p.parse() for p in parsers]
    corrupted = [r for r in parse_results if r.is_corrupt]
    print(sum([r.score for r in corrupted]))

def part_2():
    lines = get_lines(IN)
    parsers = [LineParser(l) for l in lines]
    parse_results = [p.parse() for p in parsers]
    incomplete = sorted([r for r in parse_results if r.is_incomplete], key=lambda x:x.score)
    print(incomplete[int(len(incomplete)/ 2)].score)

part_1()
part_2()