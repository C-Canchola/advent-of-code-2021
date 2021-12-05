from typing import List

def _get_counts(rows:List[str]):
    counts = [[0, 0] for _ in rows[0]]
    for l in rows:
        for idx, c in enumerate(l):
            counts[idx][int(c)] += 1
    return counts

def _get_used_count_bit(cur_count:List[int], use_highest:bool):
    
    if cur_count[1] > cur_count[0]:
        if use_highest:
            return 1
        return 0
    
    if cur_count[0] > cur_count[1]:
        if use_highest:
            return 0
        return 1
    
    if use_highest:
        return 1

    return 0
    
def _scrub_recurse(filtered_rows:List[str], idx:int, use_highest:bool):
    if len(filtered_rows) == 1:
        return filtered_rows[0]

    counts = _get_counts(filtered_rows)
    cur_count = counts[idx]
    
    used_bit = _get_used_count_bit(cur_count, use_highest)
    filtered_rows = [r for r in filtered_rows if r[idx] == str(used_bit)]

    return _scrub_recurse(filtered_rows, idx+1, use_highest)

class Converter:

    def __init__(self, rows:List[str]):
        stripped_rows = [l.strip() for l in rows]
        self.rows = stripped_rows
        self.counts = _get_counts(stripped_rows)
    
    @property
    def gamma_rate(self):
        return ''.join([str(1) if count[1] > count[0] else str(0) for count in self.counts])
    
    @property
    def epsilon_rate(self):
        return ''.join(str(0) if count[1] > count[0] else str(1) for count in self.counts)

    @property
    def power_consumption(self):
        return int(self.gamma_rate, base=2) * int(self.epsilon_rate, base=2)
    
    @property
    def oxygen_generator_rating(self):
        return _scrub_recurse(self.rows, 0, True)
    
    @property
    def co2_scrubber_rating(self):
        return _scrub_recurse(self.rows, 0, False)
    
    @property
    def life_support_rating(self):
        return int(self.oxygen_generator_rating, base=2) * int(self.co2_scrubber_rating, base=2)
        
def row_iter(file_name:str):
    with open(file_name) as f:
        for l in f:
            yield l

if __name__ == '__main__':

    converter = Converter(row_iter('ex-day-3.txt'))
    print(converter.power_consumption)
    print(converter.life_support_rating)
    
    converter = Converter(row_iter('input-day-3.txt'))
    print(converter.power_consumption)
    print(converter.life_support_rating)

