import math
import numpy as np


def crop_roi(img, roi):
    return img[int(roi[1]):int(roi[1]+roi[3]),
                      int(roi[0]):int(roi[0]+roi[2])]

def tuple_int(tpl):
    return tuple([int(x) for x in tpl])

def midpoint(pt1, pt2):
	return (int((pt1[0] + pt2[0]) * 0.5), int((pt1[1] + pt2[1]) * 0.5))

def angle(pt1, pt2):
    return math.tan((pt2[1]-pt1[1]) * 1. / (pt2[0]-pt1[0]))

def length(pt1, pt2):
    return np.linalg.norm(np.asarray(pt1)-np.asarray(pt2))
