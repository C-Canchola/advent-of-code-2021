import dataclasses
from typing import List, Dict

BOLD = '\033[1m'
END = '\033[0m'
GREEN = '\033[93m'

def get_nums(file_name:str):
    with open(file_name) as f:
        str_lines = f.readlines()
        return [[int(c) for c in l.strip()] for l in str_lines]

@dataclasses.dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

class Octopus:

    def __init__(self, level:int, x:int, y:int):
        self._level = level
        self._point = Point(x, y)
    
    @property
    def point(self):
        return self._point
    
    @property
    def x(self):
        return self._point.x
    
    @property
    def y(self):
        return self._point.y
    
    def level_up(self):
        self._level += 1

    def handle_reset(self):
        if not self._level > 9:
            return
        self._level = 0

    @property
    def is_flashing(self):
        return self._level > 9
    
    @property
    def adjacent_positions(self):
        pos = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == y == 0:
                    continue
                pos.append(Point(self.x + x, self.y + y))
        
        return pos
    
    def __str__(self):
        if self._level != 0:
            return str(self._level)
        return BOLD + GREEN + str(self._level) + END

class OctupusMap:

    def __init__(self, nums:List[List[int]]):
        self._width = len(nums[0])
        self._height = len(nums)

        self._d:Dict[Point, Octopus] = {}
        for x, row in enumerate(nums):
            for y, num in enumerate(row):
                self._d[Point(x, y)] = Octopus(num, x, y)
        
        self._flash_counts = []
        self._total_flashes = 0
        self._advancements = 0
        self._first_simultaneous_flash_round = 0
        
    def __str__(self):
        chars = []
        for x in range(self._width):
            for y in range(self._height):
                chars.append(str(self._d[Point(x, y)]))
            chars.append('\n')
        return ''.join(chars)[:-1]
    
    def _level_up_all(self):
        for o in self._d.values():
            o.level_up()
    
    def _get_surrounding(self, o:Octopus):
        for p in o.adjacent_positions:
            if p not in self._d:
                continue
            yield self._d[p]


    def advance(self):
        
        self._level_up_all()

        flash_stack = [o for o in self._d.values() if o.is_flashing]
        flash_map = {o.point: o for o in flash_stack}

        while len(flash_stack) != 0:
            o = flash_stack.pop()
            
            for adj in self._get_surrounding(o):
                
                adj.level_up()
                
                if not adj.is_flashing:
                    continue
                
                if adj.point in flash_map:
                    continue

                flash_map[adj.point] = adj
                flash_stack.append(adj)
        
        for o in flash_map.values():
            o.handle_reset()
        

        self._flash_counts.append(len(flash_map))
        self._total_flashes += len(flash_map)
        self._advancements += 1

        if len(flash_map) == len(self._d) and self._first_simultaneous_flash_round == 0:
            self._first_simultaneous_flash_round = self._advancements

        print(self)
        print('-' * 20)
        print('round - {}'.format(self._advancements))
        print('flashes this round - {}'.format(self._flash_counts[-1]))
        print('flashes total - {}'.format(self._total_flashes))
        if self._first_simultaneous_flash_round != 0:
            print(self._first_simultaneous_flash_round)
        print('-' * 20)

    def flash_until_adjacent(self):
        while self._first_simultaneous_flash_round == 0:
            self.advance()
            
        



EX = 'ex-day-11.txt'
IN = 'input-day-11.txt'

def part_1():
    m = OctupusMap(get_nums(IN))
    print(m)
    print('-' * 20)
    m.flash_until_adjacent()

    

part_1()