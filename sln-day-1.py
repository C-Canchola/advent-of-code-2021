'''made this an iterator cause I didn't know multiple reads were going to be necessary'''

def get_diff_iter(file_name:str, group_count = 1):
    with open(file_name) as f:

        prev = [int(f.readline()) for _ in range(group_count)]
        cur = prev[1:] + [int(f.readline())]

        if sum(cur) - sum(prev) > 0:
            yield 1
        
        for l in f:
            prev, cur = cur, cur[1:] + [int(l)]

            if not sum(cur) - sum(prev) > 0:
                continue
            
            yield 1

if __name__ == '__main__':
    print(sum(get_diff_iter("ex-day-1.txt")))
    print(sum(get_diff_iter("ex-day-1.txt", 3)))
    print(sum(get_diff_iter("input-day-1.txt")))
    print(sum(get_diff_iter("input-day-1.txt", 3)))