import typing
import functools
import collections.abc as abc
import dataclasses

BOLD = '\033[1m'
END = '\033[0m'
GREEN = '\033[93m'

'''
- a is always the value in len 3 combo not in len 2 output - MAPPED a
- can find potential b, d maps by rmeoving len 2 chars from len 4 chars

- map d: - MAPPED a, d
    - of potential b or d, find whichever value is in all 3 len 5 patterns

- map b: - MAPPED a, d, b
    - whichever value of potential b or d which is not found to be d

- map e: - MAPPED a, d, b, e
    - Of the len 5 without b, find the one without all the characters of len 2
    - find differnce in characters with other one without b

- the difference in the other 2 5 len sequences can determine possible b and c maps
    - can be solved by finding which character is in length 2 - MAPPED a, b, c, e, f
- can solve for d by looking for any unmapped character in len 4 - MAPPED a,b,c,d,e,f

'''
OUTPUT_DICT = {
    ('a', 'b', 'c', 'e', 'f', 'g'): 0,
    ('c', 'f') : 1,
    ('a', 'c', 'd', 'e', 'g'): 2,
    ('a', 'c', 'd', 'f', 'g'): 3,
    ('b', 'c', 'd', 'f'): 4,
    ('a', 'b', 'd', 'f', 'g'): 5,
    ('a', 'b', 'd', 'e', 'f', 'g'): 6,
    ('a', 'c', 'f') : 7,
    ('a', 'b', 'c', 'd', 'e', 'f', 'g'): 8,
    ('a','b','c', 'd', 'f', 'g'): 9
}
OUTPUT_DICT = {tuple(sorted(k)): v for k, v in OUTPUT_DICT.items()}
ALL_CHARS = 'abcdefg'

COUNT_DICT = {}
for output_key in OUTPUT_DICT:
    key_len = len(output_key)
    for ch in output_key:
        char_list = COUNT_DICT.get(key_len, list())
        if ch in char_list:
            continue
        char_list.append(ch)
        COUNT_DICT[key_len] = char_list

COUNT_DICT = {char_len:tuple(chars) for char_len, chars in COUNT_DICT.items()}

def parse_file(file_name:str):
    with open(file_name) as f:
        text = f.read()
        rplc = text.replace(' |\n', '|')
        new_line_split = rplc.split('\n')

        
        for l in new_line_split:
            delim_split = l.split('|')
            yield delim_split[0].split(), delim_split[1].split()



class PatternComponent:
    
    def __init__(self, letter, possible_values:typing.List[str]):
        self._letter = letter
        self._possible_values = possible_values

        self._found_value = None

    @property
    def converted_value(self):
        return self._found_value
    
    @property
    def has_converted_value(self):
        return self._found_value is not None
    
    @property
    def original_value(self):
        return self._letter
    
    def __str__(self):
        if not self.has_converted_value:
            return self._letter
        return BOLD + GREEN +  self.converted_value + END
    
    def update_from_map(self, map_dict:typing.Dict[str, str]):
        if self.original_value not in map_dict:
            return
        self._found_value = map_dict[self.original_value]
    

@functools.total_ordering
class Pattern(abc.Sequence):
    def __init__(self, text:str):
        self._text = text
        self._possible_values = COUNT_DICT[len(text)]
        
        self._possible_outputs = {k:v for k, v in OUTPUT_DICT.items() if len(text) == len(k)}
        self._components = [PatternComponent(c, self._possible_values) for c in text]

        
    
    def __len__(self):
        return len(self._text)

    def __getitem__(self, idx):
        return self._components[idx]
    
    def __str__(self):
        return ''.join(str(c) for c in self._components)
    
    @property
    def chars(self):
        return [ch for ch in self._text]

    @property
    def text(self):
        return self._text

    def __lt__(self, other):
        if len(self) != len(other):
            return len(self) < len(other)
        
        return sorted(self.text) < sorted(other.text)

    @property
    def remaining_values(self):
        return [component.original_value for component in self._components if not component.has_converted_value]
    
    def update_from_map_dict(self, map_dict: typing.Dict[str, str]):
        for com in self._components:
            com.update_from_map(map_dict)
        
    def contains_char(self, char:str):
        return char in self._text
    
    def is_subset_of_other(self, other):
        other : Pattern
        for c in self._text:
            if c not in other._text:
                return False
        return True
    
    def chars_other_than(self, ch:str):
        return [c for c in self._text if c not in ch]



def get_chars_not_in_other(p1:Pattern, oP: Pattern):
    return [c for c in p1.chars if c not in oP.chars]

def is_subset_of_other(p1:Pattern, p2: Pattern):
    for c in p1.text:
        if not c in p2.text:
            return False
    return True

class Converter:

    def __init__(self, map_dict:typing.Dict[str, str]):
        self._d = map_dict

    def _convert_str(self, s:str):
        chars = tuple(sorted(self._d[c] for c in s))
        return OUTPUT_DICT[chars]

    def convert_output(self, chars:typing.List[str]):
        return [self._convert_str(s) for s in chars]

    def convert_output_part_two(self, chars:typing.List[str]):
        return int(''.join([str(c) for c in self.convert_output(chars)]))

class PatternSequence(abc.Sequence):

    def __init__(self, text_list:typing.List[str], print_steps=False):
        self._patterns = [Pattern(t) for t in  text_list]
        self._sorted_patterns = sorted(self._patterns)
        self._mapped = {}
        self._print_steps = print_steps


    def __len__(self):
        return len(self._patterns)
    
    def __getitem__(self, idx):
        return self._patterns[idx]
    
    def __str__(self):
        return ' '.join(str(p) for p in self._patterns)

    def update_map(self):
        for pattern in self._patterns:
            pattern.update_from_map_dict(self._mapped)
        if not self._print_steps:
            return
        print(self)

    @classmethod
    def from_patterns(cls, patterns:typing.List[Pattern]):
        ps = cls([])
        ps._patterns = patterns
        return ps
    

    def _solve(self):
        a_map = get_chars_not_in_other(self._sorted_patterns[1], self._sorted_patterns[0])[0]
        self._mapped[a_map] = 'a'
        self.update_map()

        b_or_d = get_chars_not_in_other(self._sorted_patterns[2], self._sorted_patterns[0])
        
        len_5_patterns = self._sorted_patterns[3:6]
        first_d_filtered = [p for p in len_5_patterns if p.contains_char(b_or_d[0])]

        d_map = b_or_d[0] if len(first_d_filtered) == 3 else b_or_d[1]
        self._mapped[d_map] = 'd'
        self.update_map()

        b_map = b_or_d[1] if b_or_d[0] == d_map else b_or_d[0]
        self._mapped[b_map] = 'b'
        self.update_map()

        len_5_wo_b = sorted([(int(self._sorted_patterns[0].is_subset_of_other(p)), p) for p in len_5_patterns if not p.contains_char(b_map)])
        e_map = get_chars_not_in_other(len_5_wo_b[0][1], len_5_wo_b[1][1])[0]
        self._mapped[e_map] = 'e'
        self.update_map()

        f_map = get_chars_not_in_other(len_5_wo_b[1][1], len_5_wo_b[0][1])[0]
        self._mapped[f_map] = 'f'
        self.update_map()

        c_map = self._sorted_patterns[0].chars_other_than(f_map)[0]
        self._mapped[c_map] = 'c'
        self.update_map()

        g_map = self._sorted_patterns[-1].chars_other_than(''.join(self._mapped))[0]
        self._mapped[g_map] = 'g'
        self.update_map()
    

    def create_conveter(self):
        self._solve()
        return Converter(self._mapped)



        
def part_1():
    sequences_output_tuple = [(PatternSequence(l[0]), l[1]) for l in parse_file('input-day-8.txt')]
    nums_to_keep = [1, 4, 7, 8]
    count = 0
    for s, o in sequences_output_tuple:
        converter = s.create_conveter()
        for num in converter.convert_output(o):
            if num not in nums_to_keep:
                continue
            count+=1
    print(count)


def part_2():
    sequences_output_tuple = [(PatternSequence(l[0]), l[1]) for l in parse_file('input-day-8.txt')]
    count = 0
    for s, o in sequences_output_tuple:
        converter = s.create_conveter()
        count += converter.convert_output_part_two(o)
    print(count)

part_2()
# first_seq.update_map()