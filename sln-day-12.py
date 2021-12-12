import typing


EX = 'ex-day-12.txt'
IN = 'input-day-12.txt'

def get_lines(file_name:str):
    with open(file_name) as f:
        return [l.strip() for l in f.readlines()]

class Cave:

    def __init__(self, s:str):
        self._s = s

    @property
    def is_start(self):
        return self._s == 'start'
    
    @property
    def is_end(self):
        return self._s == 'end'
    
    @property
    def is_small(self):
        return not (self.is_start or self.is_end) and  self._s.islower()
    
    @property
    def is_large(self):
        return self._s.isupper()
    
    @property
    def value(self):
        return self._s
    
    def __hash__(self):
        return hash(self._s)
    
    def __eq__(self, other):
        return self._s == other._s
    
    def __str__(self):
        return str(self._s)
    
class Connection:
    def __init__(self, start:Cave, end:Cave):
        self._start = start
        self._end = end
    
    @property
    def is_path_start(self):
        return self._start.is_start
    
    @property
    def is_path_end(self):
        return self._end.is_end
    
    @property
    def is_initially_filtered(self):
        return self._start.is_end or self._end.is_start
    
    @property
    def start(self):
        return self._start
    
    @property
    def end(self):
        return self._end
    
    def __str__(self):
        return "{} <-> {}".format(self._start.value, self._end.value)

def connection_iter(lines:typing.Iterable[str]):
    for line in lines:
        s1, s2 = line.split('-')
        yield Connection(Cave(s1), Cave(s2))
        yield Connection(Cave(s2), Cave(s1))


def get_all_connections(file_name:str):
    lines = get_lines(file_name)
    return list((c for c in connection_iter(lines) if not c.is_initially_filtered))

class ConnectionMap:

    def __init__(self, connections:typing.List[Connection]):
        self._d = {}
        
        for c in connections:
            caves = self._d.get(c.start, list())
            caves.append(c.end)
            self._d[c.start] = caves
        
        
    def get_next_possible(self, cave:Cave):
        if cave.is_end:
            return []
        return self._d[cave]

def caves_to_str(caves:typing.List[Cave]):
    return ','.join([str(c) for c in caves])

def caves_to_tuple(caves:typing.List[Cave]):
    return tuple([str(c) for c in caves])

class PathTraverser:

    def __init__(self, conn_map:ConnectionMap, part_2=False):
        self._caves = [Cave('start')]
        self._small_cave_map = {}
        self._visited_caves = {caves_to_tuple(self._caves):True}
        self._conn_map = conn_map
        self._completed_paths = 0
        self._i = 0
        self._part_2 = part_2

    def _add_cave(self, cave:Cave):
        if cave.is_small:
            self._small_cave_map[cave] = self._small_cave_map.get(cave, 0) + 1
            

        self._caves.append(cave) 
        self._visited_caves[caves_to_tuple(self._caves)] = True
        
    
    def _pop_cave(self):
        rm_cave = self._caves.pop()
        if rm_cave not in self._small_cave_map:
            return
        self._small_cave_map[rm_cave] -= 1
        
    def _small_cave_filter(self, possible_caves:typing.List[Cave]):
        if not self._part_2:
            return [c for c in possible_caves if self._small_cave_map.get(c, 0) < 1]
        
        has_twice_visited = len([v for v in self._small_cave_map.values() if v > 1]) > 0
        if not has_twice_visited:
            return possible_caves
        
        return [c for c in possible_caves if self._small_cave_map.get(c, 0) < 1]

    def _get_possible_caves(self):

        possible_caves = self._conn_map.get_next_possible(self._caves[-1])
        possible_caves = self._small_cave_filter(possible_caves)
        
        self._i += 1
        return [c for c in possible_caves if caves_to_tuple(self._caves + [c]) not in self._visited_caves]
    
    def find_all_paths(self):

        completed_paths = []

        while len(self._caves) != 0:
            possible_caves = self._get_possible_caves()
            if len(possible_caves) == 0:
                if self._caves[-1].is_end:
                    completed_paths.append(caves_to_str(self._caves))

                self._pop_cave()
                continue
            
            self._add_cave(possible_caves[0])
        
        return completed_paths
            


    

def part_1():
    conn_map = ConnectionMap(get_all_connections(IN))
    path_traverser = PathTraverser(conn_map)
    valid_paths = path_traverser.find_all_paths()
    print(len(valid_paths))

def part_2():
    conn_map = ConnectionMap(get_all_connections(IN))
    path_traverser = PathTraverser(conn_map, part_2=True)
    valid_paths = path_traverser.find_all_paths()
    print(len(valid_paths))

part_1()
part_2()