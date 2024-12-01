import pygame
import math
from src.simulation.Simulation import Simulation
from src.simulation.Treat import Treat

worm_x = 400
worm_y = 300

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Neural Input Simulation")
clock = pygame.time.Clock()

simulation = Simulation("data/brain_config.json")
treats = []

def collision_treat(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance <= (r1 + r2)

def collision_wall(circle, rectangle):
    cx, cy, radius = circle
    rx, ry, width, height = rectangle

    closest_x = max(rx, min(cx, rx + width))
    closest_y = max(ry, min(cy, ry + height))

    distance_x = cx - closest_x
    distance_y = cy - closest_y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    return distance <= radius

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                treats.append(Treat(math.floor(event.pos[0]), math.floor(event.pos[1])))
                print(treats)

    simulation.update_positions()
    screen.fill((255, 255, 255))
    worm_postition = simulation.draw(screen, worm_x, worm_y, treats)
    worm_x = worm_postition[0]
    worm_y = worm_postition[1]
    input_commands = []
    walls = simulation.get_walls()

    treats.sort(key=lambda treat: math.sqrt((treat.x - worm_x) ** 2 + (treat.y - worm_y) ** 2))
    walls.sort(key=lambda wall: math.sqrt((wall.x - worm_x) ** 2 + (wall.y - worm_y) ** 2))

    for treat in treats:
        Treat.draw(treat, screen)

    for wall in walls:
        if collision_wall((worm_x + 1, worm_y, 10), (wall.x, wall.y, wall.width, wall.height)):
            input_commands.append("wall right")

        if collision_wall((worm_x - 1, worm_y, 10), (wall.x, wall.y, wall.width, wall.height)):
            input_commands.append("wall left")

        if collision_wall((worm_x, worm_y - 1, 10), (wall.x, wall.y, wall.width, wall.height)):
            input_commands.append("wall up")

        if collision_wall((worm_x, worm_y + 1, 10), (wall.x, wall.y, wall.width, wall.height)):
            input_commands.append("wall down")



    for treat in treats: 
        if treat.x > worm_x:
            input_commands.append("smell right")
        if treat.x < worm_x:
            input_commands.append("smell left")
        if treat.y < worm_y:
            input_commands.append("smell up")
        if treat.y > worm_y:
            input_commands.append("smell down")
        
        if collision_treat(worm_x, worm_y, 10, treat.x, treat.y, 5):
            input_commands.append("treat near")
        
        break

    simulation.handle_user_input(input_commands)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
