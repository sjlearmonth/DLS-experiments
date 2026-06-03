import timeit

def orig_compute_width_and_height(box1, box2):

    box1_x1 : float = box1[0][0]
    box1_y1 : float  = box1[0][1]

    box1_x2 : float  = box1[1][0]
    box1_y2 : float  = box1[1][1]

    box2_x1 : float  = box2[0][0]
    box2_y1 : float  = box2[0][1]

    box2_x2 : float  = box2[1][0]
    box2_y2 : float  = box2[1][1]

    xi1 = max(box1_x1, box2_x1)
    yi1 = max(box1_y1, box2_y1)
    xi2 = min(box1_x2, box2_x2)
    yi2 = min(box1_y2, box2_y2)

    w = max(xi2 - xi1, 0)
    h = max(yi2 - yi1, 0)

    area = w * h

    return w, h, area

def mod_compute_width_and_height(box1, box2):
    """
    box1 is a Python list of two tuples. Each tuple contains two values, the
    first value is an x co-ordinate and the second value is a y co-ordinate.

    The first tuple in the list contains the co-ordinates of the top left corner
    of a box and the second tuple contains the co-ordinates of the bottom right
    corner of the box.

    box2 is the same type as box1 but contains the corresponding co-ordinates
    of the other box.

    :param box1:
    :param box2:
    :return:
    """

    box1_x1 = box1[0][0]
    box1_y1 = box1[0][1]

    box1_x2 = box1[1][0]
    box1_y2 = box1[1][1]

    box2_x1 = box2[0][0]
    box2_y1 = box2[0][1]

    box2_x2 = box2[1][0]
    box2_y2 = box2[1][1]

    x1_max = (box1_x1, box2_x1)[box1_x1 < box2_x1]
    x2_min = (box1_x2, box2_x2)[box1_x2 > box2_x2]

    w = (x2_min - x1_max, 0)[x2_min < x1_max]

    y1_max = (box1_y1, box2_y1)[box1_y1 < box2_y1]
    y2_min = (box1_y2, box2_y2)[box1_y2 > box2_y2]

    h = (y2_min - y1_max, 0)[y2_min < y1_max]

    area = 0

    if w > 0 and h > 0:

        area = h * w

    return w, h, area

b1_w = 3.5; b1_h = 4
b2_w = 3.45; b2_h = 3.2

b1_x1 = 1; b1_y1 = 1

b2_x1 = 2.75; b2_y1 = 2.75

b1 = [(b1_x1, b1_y1), (b1_x1 + b1_w, b1_y1 + b1_h)]; b2 = [(b2_x1, b2_y1), (b2_x1 + b2_w, b2_y1 + b2_h)]

orig_t = timeit.timeit(
    "orig_compute_width_and_height(b1, b2)",
    globals=globals(),
    number=1000000
)

print(f"Original average execution time: {orig_t/1000000*1e9:.2f} ns")

mod_t = timeit.timeit(
    "mod_compute_width_and_height(b1, b2)",
    globals=globals(),
    number=1000000
)

print(f"Modified average execution time:  {mod_t/1000000*1e9:.2f} ns")

print(f"The modified code is {(orig_t - mod_t)*100/orig_t:.2f}% faster than the original code.")


