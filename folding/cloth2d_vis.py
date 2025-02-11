import pygame

import sys

DATASET_DIR = "dataset"

IMAGE_SIZE = (100, 100)
pick_color = "red"
pick_radius = 5
place_color = "green"
place_radius = 5

if len(sys.argv) < 5:
    print("Usage:  cloth2d_vis.py image_name pick_x pick_y place_x place_y")
    print("Example:  cloth2d_vis.py dataset/image1.png 1 2 3 4")
    quit(1)

image_name = sys.argv[-5]
pick_x = round(float(sys.argv[-4]))
pick_y = round(float(sys.argv[-3]))
place_x = round(float(sys.argv[-2]))
place_y = round(float(sys.argv[-1]))

pygame.init()
 
scrn = pygame.display.set_mode(IMAGE_SIZE)
 
surf1 = pygame.image.load(image_name).convert()
pygame.draw.circle(surf1, pick_color, (pick_x,pick_y), pick_radius)
pygame.draw.circle(surf1, place_color, (place_x,place_y), place_radius)
 
scrn.blit(surf1, (0, 0))
 
pygame.display.flip()
status = True
while (status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
 
pygame.quit()
