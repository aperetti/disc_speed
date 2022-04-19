import numpy as np
from pytablewriter import MarkdownTableWriter
# File used to help calculate how well the system will perform

def distance_calc():
    fps = [15,30,60,120,240]

    speed = np.arange(1, 16)*5

    dist = (np.outer(speed, np.ones(len(fps))) * 1.477 / fps - .702) * 12
    dist = np.round(np.c_[speed.astype(int), dist], 0)

    header = ["Speed (MPH)"]
    header.extend(fps)

    md = MarkdownTableWriter(table_name="Gap Per Frame", headers=[str(x) for x in header], value_matrix=dist.tolist())
    md.write_table()


if __name__ == '__main__':
    distance_calc()
