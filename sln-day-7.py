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
    
class DistanceChecker:

    def __init__(self, nums:typing.List[int]):
        self._nums = sorted(nums)
        self._min, self._max = self._nums[0], self._nums[-1]
        self._range_list = list(range(self._min, self._max + 1))
        self._counts = counts(self._nums)


    def minimum_distance_brute(self):
        return min(DistanceResult(self._counts, i).distance() for i in self._range_list)

    def minimum_distance_2_brute(self):
        return min(DistanceResult(self._counts, i).distance_part_2() for i in self._range_list)

def example_part_1():
    return DistanceChecker(nums_example()).minimum_distance_brute()

def input_part_1():
    return DistanceChecker(input_example()).minimum_distance_brute()

def example_part_2():
    return DistanceChecker(nums_example()).minimum_distance_2_brute()

def input_part_2():
    return DistanceChecker(input_example()).minimum_distance_2_brute()

if __name__ == '__main__':
    example_nums = nums_example()
    # print(example_part_1())
    # print(input_part_1())
    print(example_part_2())
    print(input_part_2())
    
    