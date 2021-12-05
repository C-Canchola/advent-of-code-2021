from typing import List
from collections.abc import Sequence
from collections import defaultdict
'''
part 1
Have paths in form of:
    0,9 -> 5,9
    8,0 -> 0,8
    2,2 -> 2,1

Consider vertical and horizontal lines only (y1==y2 | x1==x2)
'''

class VentPoint:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()
    
    def __str__(self):
        return str((self.x, self.y))
    
    def __repr__(self):
        return "VentPoint(x={}, y={})".format(self.x, self.y)
    
    def as_tuple(self):
        return (self.x, self.y)


class VentSegment:
    def __init__(self, pos_tuple):
        self.x1, self.y1, self.x2, self.y2 = pos_tuple
    
    def __str__(self):
        return "x1={}; y1={}; x2={}; y2={}".format(self.x1, self.y1, self.x2, self.y2)

    
    @property
    def is_horizontal(self):
        return self.y1 == self.y2
    
    @property
    def is_vertical(self):
        return self.x1 == self.x2

    @property
    def is_horizontal_or_vertical(self):
        return self.is_horizontal or self.is_vertical
    
    def _is_45_inc(self):
       return self.x2 - self.x1 == self.y2 - self.y1

    def _is_45_dec(self):
        return -1 * (self.x2 - self.x1) == self.y2 - self.y1

    @property
    def is_45_diagonal(self):
        return self._is_45_dec() or self._is_45_inc()

    @property
    def has_points(self):
        return self.is_horizontal_or_vertical or self.is_45_diagonal

    @property
    def points(self):
        if not self.has_points:
            return
        
        if self.is_vertical:
            sorted_y = sorted([self.y1, self.y2])
            for y_i in range(sorted_y[0], sorted_y[1] + 1):
                yield VentPoint(self.x1, y_i)
            return
        
        if self.is_horizontal:
            sorted_x = sorted([self.x1, self.x2])
            for x_i in range(sorted_x[0], sorted_x[1] + 1):
                yield VentPoint(x_i, self.y1)
            return
        
        if self._is_45_inc():
            sorted_both = sorted([(self.x1,self.y1), (self.x2, self.y2)], key=lambda x:x[0] + x[1])
            steps = sorted_both[1][0] - sorted_both[0][0] + 1
 
            for delta in range(steps):
                yield VentPoint(sorted_both[0][0] + delta, sorted_both[0][1] + delta)
            return
        
        if self._is_45_dec():
            y_coeff = 1
            if self.y2 < self.y1:
                y_coeff = -1

            steps = abs(self.y2 - self.y1) + 1
            for delta in range(steps):
                yield VentPoint(self.x1 - y_coeff * delta, self.y1 + y_coeff * delta) 
            return
    
 

class VentSegmentCollection(Sequence):
    def __init__(self, vent_segs: List[VentSegment]):
        self._vent_segs = vent_segs
    
    def __str__(self):
        return str([str(s) for s in self._vent_segs])
    
    def __repr__(self):
        return str(self._vent_segs)
    
    def __len__(self):
        return len(self._vent_segs)

    def __getitem__(self, idx):
        return self._vent_segs[idx]
    
    def non_diaganol_segments(self):
        return VentSegmentCollection([s for s in self._vent_segs if s.is_horizontal_or_vertical])
    
    def _straight_point_counts(self):
        non_d_segs = self.non_diaganol_segments()
        return _seg_point_counts(non_d_segs)

    @property
    def overlapping_straight_points(self):
        counts = self._straight_point_counts()
        return {pt:count for pt, count in counts.items() if count > 1}
    
    def diagonal_45_segments(self):
        return VentSegmentCollection([s for s in self._vent_segs if s.is_45_diagonal])
    
    def _all_segments_with_points(self):
        return VentSegmentCollection([s for s in self._vent_segs if s.has_points])
    
    
    @property
    def answer_part_1(self):
        return len(self.overlapping_straight_points)

    @property
    def answer_part_2(self):
        point_counts = _seg_point_counts(self._all_segments_with_points())
        return len({pt:count for pt, count in point_counts.items() if count > 1})

def _seg_point_counts(segments:VentSegmentCollection):
    point_counts = defaultdict(int)
    pt_gen = (pts for seg in segments for pts in seg.points)
    for pt in pt_gen:
        point_counts[pt] += 1
        
    return point_counts


def _parse_line(l:str):
    l = l.replace('\n', '').replace(' -> ', ',')
    splt = l.split(',')
    
    return tuple([int(c) for c in splt])

class Parser:

    def __init__(self, file_name:str):
        self._file_name = file_name
    
    def _text_lines(self):
        with open(self._file_name) as f:
            return f.readlines()
        
    def vent_segments(self):
        tups =[_parse_line(l) for l in self._text_lines()] 
        segs = [VentSegment(t) for t in tups]
        return VentSegmentCollection(segs)


if __name__ == '__main__':
    vent_segs = Parser('ex-day-5.txt').vent_segments()
    print(vent_segs.answer_part_1)
    print(vent_segs.answer_part_2)

    vent_segs = Parser('input-day-5.txt').vent_segments()
    print(vent_segs.answer_part_1)
    print(vent_segs.answer_part_2)