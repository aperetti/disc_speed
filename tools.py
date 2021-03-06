from collections import namedtuple
import math
import time
import numpy as np
import cv2


def crop_roi(img, roi):
    return img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

def tuple_int(tpl):
    return tuple([int(x) for x in tpl])

def midpoint(pt1, pt2):
	return (int((pt1[0] + pt2[0]) * 0.5), int((pt1[1] + pt2[1]) * 0.5))

def angle(pt1, pt2):
    return math.tan((pt2[1]-pt1[1]) * 1. / (pt2[0]-pt1[0]))

def distance(pt1, pt2):
    return np.linalg.norm(np.asarray(pt1)-np.asarray(pt2))

class CircularTimeBuffer:
    def __init__(self, max_len: int, fps: int = 0) -> None:
        self.time = [None for x in range(max_len)]
        self.data = [None for x in range(max_len)]
        self.max_len = max_len
        self.spot = 0
        self.fps= fps


    def add(self, item):
        self.data[self.spot] = item
        self.time[self.spot] = time.time()
        self.spot = (self.spot + 1) % self.max_len

    def get_prev(self, n=1):
        return self.data[(self.spot -n) % self.max_len]

    def get_prev_time(self, n=1):
        return self.time[(self.spot - n) % self.max_len]

    def get_two(self, n1=1, n2=2):
        if self.fps != 0:
            time_diff = (n2-n1) * 1. / self.fps
        else:
            time_diff = abs(self.get_prev_time(n2)- self.get_prev_time(n1))
        return self.get_prev(n1), self.get_prev(n2), time_diff

    def is_full(self):
        return all([x is not None for x in self.data])

class CaptureWrapper:
    def __init__(self, cap):
        self.cap = cap

    def read(self):
        ret, frame = self.cap.read()
        if ret == False:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        return ret, frame



def angle(p1, p2):
    return math.tan(-1 * (p2.y-p1.y)/(p2.x-p1.x))

Point = namedtuple("Point", ["x", "y"])