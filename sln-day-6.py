'''
all I need to do for part 1 is figure out the formula
for how many days the fish count will be by starting day.

Then apply it to all the original fish starting days.
Calculating based upon the ever growing list will give a much worse O(N).

Start with 1:
Day 0: 1
------------
Day 1: 0,
Day 2: 6, 8
Day 3: 5, 7,
Day 4: 4, 6
Day 5: 3, 5
Day 6: 2, 4
Day 7: 1, 3
Day 8: 0, 2
Day 9: 6, 1, 8
Day 10: 5, 0, 7
Day 11: 4, 6, 6, 8

'''
import functools


def get_nums(file_name:str):
    with open(file_name) as f:
        return [int(num) for num in f.readline().split(",")]


@functools.lru_cache()
def get_child_count_for_day_1_fish(days:int):
    if days < 2:
        return 0
    return 1 + get_child_count_for_day_1_fish(days - 7) + get_child_count_for_day_1_fish(days - (7 + 2))

@functools.lru_cache()
def get_count_for_day_1_fish(days:int):
    return 1 + get_child_count_for_day_1_fish(days)

@functools.lru_cache()
def get_count_for_fish(days:int, fish_day:int):
    days_past_1 = fish_day - 1
    return get_count_for_day_1_fish(days - days_past_1)

def example_1():
    days = 80
    nums = get_nums('ex-day-6.txt')
    
    return sum([get_count_for_fish(days, fish_num) for fish_num in nums])

def solution_1():
    days = 80
    nums = get_nums('input-day-6.txt')
    return sum([get_count_for_fish(days, fish_num) for fish_num in nums])

def solution_2():
    days = 256
    nums = get_nums('input-day-6.txt')
    return sum([get_count_for_fish(days, fish_num) for fish_num in nums])

if __name__ == '__main__':
    print(solution_1())
    print(solution_2())
    # for i in range(1, 20):
    #     print(i, get_count_for_fish(i, 2))