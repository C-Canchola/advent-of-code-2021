import typing
import dataclasses

def get_nums(file_name:str):
    with open(file_name) as f:
        str_lines = f.readlines()
        return [[int(c) for c in l.strip()] for l in str_lines]

@dataclasses.dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int

class Point:
    def __init__(self, height:int, neighbor_heights:typing.List[int], pos:Position):
        self._height = height
        self._neighbor_heights = neighbor_heights
        self._pos = pos
    
    @property
    def position(self):
        return self._pos
    
    @property
    def height(self):
        return self._height
    
    @property
    def is_low_point(self):
        for n in self._neighbor_heights:
            if self._height >= n:
                return False
        return True
    
    @property
    def risk_level(self):
        return 1 + self._height
    
    @property
    def x(self):
        return self._pos.x
    
    @property
    def y(self):
        return self._pos.y
    
    def __str__(self):
        return 'x: {}; y: {}; height: {}'.format(self.x, self.y, self.height)

def get_points_from_nums(nums:typing.List[typing.List[int]]):

    points = []

    for x, row in enumerate(nums):
        for y, num in enumerate(row):

            neighbors = []
            if x != 0:
                neighbors.append(nums[x - 1][y])
            if x != len(nums) - 1:
                neighbors.append(nums[x + 1][y])
            
            if y != 0:
                neighbors.append(nums[x][y - 1])
            
            if y != len(row) - 1:
                neighbors.append(nums[x][y + 1])
            
            points.append(Point(num, neighbor_heights=neighbors, pos=Position(x, y)))
        
    return points

class PointMap:

    def __init__(self, points:typing.List[Point]):
        self._point_dict = {p.position:p for p in points}

    def get_all_low_points(self):
        return [p for p in self._point_dict.values() if p.is_low_point]

    def calculate_risk_sum(self):
        return sum([p.risk_level for p in self.get_all_low_points()])

    def calculate_basin_size_from_low_point(self, low_point:Point):
        visited = {}
        size = 0

        stack = [low_point]
        while len(stack) != 0:
            p = stack.pop()
            size += 1
            visited[p.position] = True
            
            while True:
                new_pos = Position(p.x - 1, p.y)
                if new_pos not in self._point_dict:
                    break
                if new_pos in visited:
                    break
                new_point = self._point_dict[new_pos]
                if new_point.height == 9:
                    break
                if new_point.height <= p.height:
                    break
                visited[new_pos] = True

                stack.append(new_point)
                break
            
            while True:
                new_pos = Position(p.x + 1, p.y)
                if new_pos not in self._point_dict:
                    break
                if new_pos in visited:
                    break
                new_point = self._point_dict[new_pos]
                if new_point.height == 9:
                    break
                if new_point.height <= p.height:
                    break
                
                visited[new_pos] = True
                stack.append(new_point)
                break

            while True:
                new_pos = Position(p.x, p.y - 1)
                if new_pos not in self._point_dict:
                    break
                if new_pos in visited:
                    break
                new_point = self._point_dict[new_pos]
                if new_point.height == 9:
                    break
                if new_point.height <= p.height:
                    break
                
                visited[new_pos] = True
                stack.append(new_point)
                break

            while True:
                new_pos = Position(p.x, p.y + 1)
                if new_pos not in self._point_dict:
                    break
                if new_pos in visited:
                    break
                new_point = self._point_dict[new_pos]
                if new_point.height == 9:
                    break
                if new_point.height <= p.height:
                    break
                
                visited[new_pos] = True
                stack.append(new_point)
                break

        return size

    def calculate_all_basins(self):
        return [self.calculate_basin_size_from_low_point(p) for p in self.get_all_low_points()]

def part_1(file_name:str):
    nums = get_nums(file_name)
    points = get_points_from_nums(nums)
    point_map = PointMap(points)
    print(point_map.calculate_risk_sum())
    risk_sum = 0
    for p in points:
        p:Point
        if not p.is_low_point:
            continue
        risk_sum += p.risk_level
    print(risk_sum)

def part_2(file_name:str):
    nums = get_nums(file_name)
    points = get_points_from_nums(nums)
    point_map = PointMap(points)


    amt = 1
    
    basin_sizes = point_map.calculate_all_basins()
    sorted_basins = sorted(basin_sizes)
    considered_basins = sorted_basins[-3:]
    print(considered_basins)
    for b in considered_basins:
        amt *= b
    
    print(amt)


part_1('input-day-9.txt')
part_2('input-day-9.txt')