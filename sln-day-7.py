import typing

def counts(nums:typing.List[int]):
    d = {}
    for n in nums:
        d[n] = 1 + d.get(n, 0)
    return d

def nums_example():
    with open('ex-day-7.txt') as f:
        return [int(num) for num in f.readline().split(',')]

def input_example():
    with open('input-day-7.txt') as f:
        return [int(num) for num in f.readline().split(',')]

def sum_n(n:int):
    return n * (n + 1) / 2

class DistanceResult:

    def __init__(self, counts:typing.Dict[int, int], point:int):
        self._counts = counts
        self._point = point
    
    def distance(self):
        return sum([
            abs(self._point - start) * count 
            for start, count 
            in self._counts.items()
            ]
        )

    def distance_part_2(self):
        return sum([
            sum_n(abs(self._point - start)) * count
            for start, count
            in self._counts.items()
        ])


class DistanceChecker: # This could be changed to do some sort of binary search to increase complexity time.
    # Another method would to start at some mid point (mean or median probably) and check the distances in both increasing and decreasing direction.
    # Once a specific direction INCREASES count, you know that's the maximum of that direction. Once both maximums are found, the two can be compared

    def __init__(self, nums:typing.List[int], part_1=True):
        self._nums = sorted(nums)
        self._min, self._max = self._nums[0], self._nums[-1]
        
        self._range_list = list(range(self._min, self._max + 1))
        self._counts = counts(self._nums)
        self._mean = int(sum(nums) / len(nums))

        res = DistanceResult(self._counts, self._mean)
        self._is_part_1 = part_1
        self._mean_dist = res.distance() if part_1 else res.distance_part_2()
    
    def _distance_check(self, idx:int):
        res = DistanceResult(self._counts, idx)

        if self._is_part_1:
            return res.distance()

        return res.distance_part_2()

    def _calculate_direction_min(self, coeff = 1):
        idx = self._mean
        min_dist = self._mean_dist
        while True:
            
            if idx == self._min:
                return min_dist
            
            if idx == self._max:
                return min_dist
                
            idx += coeff * 1
            dist = self._distance_check(idx)
            
            if dist >= min_dist:
                return min_dist
            
            min_dist = dist

    def _calculate_left_min(self):
        return self._calculate_direction_min(-1)
    
    def _calculate_right_min(self):
        return self._calculate_direction_min(1)
    
    def minimum_distance_middle_out(self):
        return int(min(self._calculate_left_min(), self._calculate_right_min()))

def example_checker(part_1 = True):
    return DistanceChecker(nums_example(), part_1)

def input_checker(part_1 = True):
    return DistanceChecker(input_example(), part_1)

def example_part_1():
    return example_checker().minimum_distance_middle_out()

def input_part_1():
    return input_checker().minimum_distance_middle_out()

def example_part_2():
    return example_checker(False).minimum_distance_middle_out()

def input_part_2():
    return input_checker(False).minimum_distance_middle_out()

if __name__ == '__main__':
    print(example_part_1())
    print(input_part_1())
    print(example_part_2())
    print(input_part_2())
    
    