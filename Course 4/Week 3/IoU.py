from sys import orig_argv

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def on_key(event):

    global box1_plt_x, box1_plt_y
    global box2_plt_x, box2_plt_y

    global box1_x1, box1_y1
    global box1_x2, box1_y2

    global box2_x1, box2_y1
    global box2_x2, box2_y2

    global intersection

    global inter_plt_x, inter_plt_y

    global inter_width, inter_height, inter_area, orig_alg

    if event.key =="t":

        orig_alg = not orig_alg

    if event.key == 'left':

        box1_plt_x -= step

    elif event.key == 'right':

        box1_plt_x += step

    elif event.key == 'up':

        box1_plt_y += step

    elif event.key == 'down':

        box1_plt_y -= step

    # Move rectangle

    box1.set_xy((box1_plt_x, box1_plt_y))

    # Compute the top left corner (x1, y1) of box 1 from the plot (x, y) of matplotlib
    box1_x1 = box1_plt_x
    box1_y1 = ylim_max - (box1_plt_y + box1_height)

    # Compute the bottom right corner (x2, y2) of box 1 from the plot (x, y) of matplotlib
    box1_x2 = box1_plt_x + box1_width
    box1_y2 = ylim_max - box1_plt_y

    # Compute the top left corner (x1, y1) of box 2 from the plot (x, y) of matplotlib
    box2_x1 = box2_plt_x
    box2_y1 = ylim_max - (box2_plt_y + box2_height)

    # Compute the bottom right corner (x2, y2) of box 2 from the plot (x, y) of matplotlib
    box2_x2 = box2_plt_x + box2_width
    box2_y2 = ylim_max - box2_plt_y

    xi1 = max(box1_x1, box2_x1)
    yi1 = max(box1_y1, box2_y1)
    xi2 = min(box1_x2, box2_x2)
    yi2 = min(box1_y2, box2_y2)

    if orig_alg:

        inter_width = max(xi2 - xi1, 0)
        inter_height = max(yi2 - yi1, 0)

        if inter_width > 0 or inter_height > 0:

            inter_plt_x = xi1
            inter_plt_y = ylim_max - yi2

            intersection.set_xy((inter_plt_x, inter_plt_y))
            intersection.set_width(inter_width)
            intersection.set_height(inter_height)
            intersection.set_visible(True)

        else:

            intersection.set_visible(False)

    else:

        if xi1 < xi2 and yi1 < yi2:

            inter_width = xi2 - xi1
            inter_height = yi2 - yi1

            inter_plt_x = xi1
            inter_plt_y = ylim_max - yi2

            intersection.set_xy((inter_plt_x, inter_plt_y))
            intersection.set_width(inter_width)
            intersection.set_height(inter_height)
            intersection.set_visible(True)

        else:

            inter_width = 0
            inter_height = 0

            intersection.set_visible(False)

    inter_area = inter_width * inter_height

    fig.suptitle(f"xi1={xi1:.1f}, yi1={yi1:.1f}; xi2={xi2:.1f}, yi2={yi2:.1f}\n\n width={inter_width:.1f}, height={inter_height:.1f}, area: {inter_area:.1f}")

    # Redraw figure
    fig.canvas.draw()

fig, ax = plt.subplots(figsize=(6, 6))

fig.canvas.mpl_connect('key_press_event', on_key)

orig_alg = False

step = 0.1

BOX_1_TOP_LEFT_X = 1
BOX_1_TOP_LEFT_Y = 1
BOX_2_TOP_LEFT_X = 5
BOX_2_TOP_LEFT_Y = 5

xlim_min = 0; xlim_max = 10
ylim_min = 0; ylim_max = 10

ax.set_xlim(xlim_min, xlim_max)
ax.set_ylim(ylim_min, ylim_max)

# x, y, width, height
box1_width = 3.5
box1_height = 4

box1_x1 = BOX_1_TOP_LEFT_X
box1_y1 = BOX_1_TOP_LEFT_Y
box1_x2 = box1_x1 + box1_width
box1_y2 = box1_y1 + box1_height

box2_width = 3.45
box2_height = 3.2

box2_x1 = BOX_2_TOP_LEFT_X
box2_y1 = BOX_2_TOP_LEFT_Y
box2_x2 = box2_x1 + box2_width
box2_y2 = box2_y1 + box2_height

box1_plt_x = box1_x1
box1_plt_y = ylim_max - (box1_y1 + box1_height)

box2_plt_x = box2_x1
box2_plt_y = ylim_max - (box2_y1 + box2_height)

box1 = Rectangle((box1_plt_x, box1_plt_y), box1_width, box1_height, color='blue')
box2 = Rectangle((box2_plt_x, box2_plt_y), box2_width, box2_height, color='blue')

ax.add_patch(box1)
ax.add_patch(box2)

intersection = Rectangle((0, 0), 0, 0, color='red')
ax.add_patch(intersection)
intersection.set_visible(False)

xi1 = max(box1_x1, box2_x1)
yi1 = max(box1_y1, box2_y1)
xi2 = min(box1_x2, box2_x2)
yi2 = min(box1_y2, box2_y2)

inter_width = 0
inter_height = 0

inter_plt_x = 0
inter_plt_y = 0

if xi1 < xi2 and yi1 < yi2:

    inter_width = xi2 - xi1
    inter_height = yi2 - yi1

    inter_plt_x = xi1
    inter_plt_y = ylim_max - yi2

    intersection.set_xy((inter_plt_x, inter_plt_y))
    intersection.set_width(inter_width)
    intersection.set_height(inter_height)
    intersection.set_visible(True)

else:

    inter_width = 0
    inter_height = 0

    intersection.set_visible(False)

inter_area = inter_width * inter_height

fig.suptitle(f"xi1={xi1:.1f}, yi1={yi1:.1f}; xi2={xi2:.1f}, yi2={yi2:.1f}\n\n width={inter_width:.1f}, height={inter_height:.1f}, area: {inter_area:.1f}")

plt.show()
