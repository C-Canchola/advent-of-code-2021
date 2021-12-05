def get_diff_iter():
    with open('input-day-1.txt') as f:
        prev = int(f.readline())
        cur = int(f.readline())
        yield 1 if cur - prev > 0 else 0

        for l in f:
            prev = cur
            cur = int(l)
            yield 1 if cur - prev > 0 else 0

if __name__ == '__main__':
    print(sum(get_diff_iter()))