from typing import List
POS_H = 0
POS_DEPTH = 1

def get_pos_index_and_coeff(split_line:List[str]):
    d = split_line[0]
    if d == 'up':
        return POS_DEPTH, -1
    if d == 'down':
        return POS_DEPTH, 1
    if d == 'forward':
        return POS_H, 1

    raise ValueError('unexpected direction:', d)

def update_pos(pos:List[int], split_line:List[str], use_aim:bool = False):
    pos_idx, coeff = get_pos_index_and_coeff(split_line)
    v = int(split_line[1])
    if not use_aim:
        pos[pos_idx]+= coeff * v
        return
    
    if pos_idx == POS_DEPTH:
        pos[2]+= coeff * v
        return
    
    pos[0] += v
    pos[1] += pos[2] * v


def get_distance(file_name:str, use_aim:bool=False):
    dist = [0, 0, 0]
    with open(file_name) as f:
        for l in f:
            split_line = l.split()
            update_pos(dist, split_line, use_aim)
    return dist[0] * dist[1]

if __name__ == '__main__':
    print(get_distance('ex-day-2.txt'))
    print(get_distance('input-day-2.txt'))
    print(get_distance('ex-day-2.txt', True))
    print(get_distance('input-day-2.txt', True))