import pygame

import math
import random
#from time import sleep

NUM_OUTPUT_SAMPLES = 10000

IMAGE_SIZE = (300, 300)
CLOTH_SIZE = (250, 150) # Before scaling is applied (transformations are optional).
CLOTH_TL = (25, 75) # TL is `top left corner` before scaling/rotation is applied (transformations are optional).

RANDOM_ROTATE = True # [True/False] Rotation, with True applies random 0-360 degrees.
RANDOM_SCALE_MAX = 0.25 # [percent] Scaling, reducing random variation (does not apply expansion because it could go outside the image). Set to 0 for False
RANDOM_MOVE_MAX = 15 # [pixels] on each side, e.g. 15 will move -15 to 15. Set to 0 for False

labels_file = open("labels.txt", "w") # or "a" to append

def scale(origin, point, scale):
    ox, oy = origin
    px, py = point
    qx = ox + (px - ox) * scale
    qy = oy + (py - oy) * scale
    return qx, qy

def move(origin, value):
    ox, oy = origin
    qx = ox + value
    qy = oy + value
    return qx, qy

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    Modified from [Mark Dickinson](https://stackoverflow.com/users/270986):
    - <https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python>
    """
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def reflect(p1, p2, pin):
    """
    Modified from [MBo](https://stackoverflow.com/users/844416):
    - <https://stackoverflow.com/questions/65252818/quickly-compute-reflection-of-point-about-line-described-by-two-points>
    """
    x12 = p2[0] - p1[0]
    y12 = p2[1] - p1[1]
    xxp = pin[0] - p1[0]
    yyp = pin[1] - p1[1]
    dotp = x12 * xxp + y12 * yyp
    dot12 = x12 * x12 + y12 * y12
    coeff = dotp / dot12
    lx = p1[0] + x12 * coeff
    ly = p1[1] + y12 * coeff
    return 2*lx-pin[0], 2*ly-pin[1]

pygame.init()
window = pygame.display.set_mode(IMAGE_SIZE)

for sample_idx in range(NUM_OUTPUT_SAMPLES):

    # note: offset 1 to avoid dot12 ZeroDivisionError: division by zero
    fold_x = random.randint(1, CLOTH_SIZE[0]-1) # (CLOTH_SIZE[0]/2, CLOTH_SIZE[0])
    fold_y = random.randint(1, CLOTH_SIZE[1]-1) # (CLOTH_SIZE[1]/2, CLOTH_SIZE[1])

    p = [CLOTH_TL,
        (CLOTH_TL[0]+CLOTH_SIZE[0], CLOTH_TL[1]),
        (CLOTH_TL[0]+CLOTH_SIZE[0], CLOTH_TL[1]+fold_y),
        (CLOTH_TL[0]+fold_x,        CLOTH_TL[1]+CLOTH_SIZE[1]),
        (CLOTH_TL[0],               CLOTH_TL[1]+CLOTH_SIZE[1])]
    p_place = (CLOTH_TL[0]+CLOTH_SIZE[0], CLOTH_TL[1]+CLOTH_SIZE[1])
    p_pick = reflect(p[2], p[3], p_place)

    image_center = (IMAGE_SIZE[0]/2,IMAGE_SIZE[1]/2)

    if RANDOM_ROTATE:
        angle = random.uniform(0, 6.28)
        p = [rotate(image_center, item, angle) for item in p]
        p_place = rotate(image_center, p_place, angle)
        p_pick = rotate(image_center, p_pick, angle)

    if RANDOM_SCALE_MAX != 0:
        scale_value = random.uniform(1-RANDOM_SCALE_MAX, 1) # 1+RANDOM_SCALE_MAX
        p = [scale(image_center, item, scale_value) for item in p]
        p_place = scale(image_center, p_place, scale_value)
        p_pick = scale(image_center, p_pick, scale_value)

    if RANDOM_MOVE_MAX != 0:
        value = random.uniform(-RANDOM_MOVE_MAX, RANDOM_MOVE_MAX)
        p = [move(item, value) for item in p]
        p_place = move(p_place, value)
        p_pick = move(p_pick, value)

    window.fill((0, 0, 0))
    
    pygame.draw.polygon(window, (100, 100, 100), (p[0], p[1], p[2], p[3], p[4]))
    pygame.draw.polygon(window, (200, 200, 200), (p[2], p[3], p_pick))

    #pygame.display.flip()
    image_name = 'image'+str(sample_idx)+'.png'
    pygame.image.save(window, image_name)
    labels_string = ', '.join([image_name, str(int(p_pick[0])),str(int(p_pick[1])),
        str(int(p_place[0])), str(int(p_place[1]))])
    labels_file.write(labels_string+'\n')
    
    if((sample_idx % 250) == 0):
        print(labels_string)

#sleep(1)

labels_file.close()
pygame.quit()
print("bye!")
