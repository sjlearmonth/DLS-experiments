def compute_width_and_height(box1, box2):
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

    x1 = box1_x1, box2_x1

    x2 = box1_x2, box2_x2

    box1_x1_is_max = (x1[0] - x1[1]) <= 0
    box1_x2_is_min = (x2[0] - x2[1]) >= 0

    y1 = box1_y1, box2_y1

    y2 = box1_y2, box2_y2

    box1_y1_is_max = (y1[0] - y1[1]) <= 0
    box1_y2_is_min = (y2[0] - y2[1]) >= 0

    w = (x2[box1_x2_is_min] - x1[box1_x1_is_max]) * ( (x2[box1_x2_is_min] - x1[box1_x1_is_max]) > 0 )

    h = (y2[box1_y2_is_min] - y1[box1_y1_is_max]) * ( (y2[box1_y2_is_min] - y1[box1_y1_is_max]) > 0)

    # return x1[box1_x1_is_max], y1[box1_y1_is_max], x2[box1_x2_is_min], y2[box1_y2_is_min]

    return w, h
b1_w = 3.5; b1_h = 4
b2_w = 3.45; b2_h = 3.2

b1_x1 = 1; b1_y1 = 1;
b2_x1 = 2.75; b2_y1 = 2.75
# b2_x1 = 3.0;  b2_y1 = 3.0

b1 = [(b1_x1, b1_y1), (b1_x1 + b1_w, b1_y1 + b1_h)]; b2 = [(b2_x1, b2_y1), (b2_x1 + b2_w, b2_y1 + b2_h)]

width, height = compute_width_and_height(b1, b2)

print(width, height)
exit()


xi1 = max(box1_x1, box2_x1)
yi1 = max(box1_y1, box2_y1)
xi2 = min(box1_x2, box2_x2)
yi2 = min(box1_y2, box2_y2)
