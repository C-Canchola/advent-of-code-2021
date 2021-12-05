def get_diff_iter():
    with open('input-day-1.txt') as f:
        prev = int(f.readline())
        cur = int(f.readline())
        yield cur - prev

        for l in f:
            prev = cur
            cur = int(l)
            yield cur - prev

print(len([diff for diff in get_diff_iter() if diff > 0]))