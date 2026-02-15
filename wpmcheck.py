import pygame,sys,pymunk
import string, random

wall_thickness = 10
width = 1280
height = 720

#Function of random text generator
def generate_text(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def draw_walls():
    left = pygame.draw.line(screen, 'white',(0,0),(0,height), wall_thickness)
    right = pygame.draw.line(screen , 'white',(width, 0),(width,height), wall_thickness)
    top = pygame.draw.line(screen , 'white',(0,0),(width,0), wall_thickness)
    bottom = pygame.draw.line(screen , 'white',(0, height),(width, height), wall_thickness)
    wall_list = [left, right, top, bottom]
    return wall_list

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    screen.fill("purple")
    walls = draw_walls()
    pygame.display.update()
    clock.tick(120)
