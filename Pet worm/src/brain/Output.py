import pygame
import math

pygame.mixer.init()

def collision(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance <= (r1 + r2)

class Output:
    def __init__(self, type, strength, id):
        self.type = type
        self.activation_strength = strength
        self.current_weight = 0.0
        self.id = id

    def move_up(self, worm_y):
        worm_y -= 1
        return worm_y

    def move_down(self, worm_y):
        worm_y += 1
        return worm_y

    def move_left(self, worm_x):
        worm_x -= 1
        return worm_x

    def move_right(self, worm_x):
        worm_x += 1
        return worm_x

    def display(self, screen, worm_x, worm_y, treats, highest_weight=0.0, segments=[]):
        if highest_weight > 0 and self.current_weight == highest_weight:
            if self.type == "up":
                worm_y = self.move_up(worm_y)
            elif self.type == "down":
                worm_y = self.move_down(worm_y)
            elif self.type == "left":
                worm_x = self.move_left(worm_x)
            elif self.type == "right":
                worm_x = self.move_right(worm_x)
            elif self.type == "eat":
                yummy = pygame.mixer.Sound('assets/yummy.mp3')
                yummy.play()
                for index, treat in enumerate(treats):
                    if collision(worm_x, worm_y, 10, treat.x, treat.y, 5):
                        treats.pop(index)
                        break

        segments.insert(0, (worm_x, worm_y))
        if len(segments) > 300:
            segments.pop()

        for segment in segments:
            pygame.draw.circle(screen, (0, 0, 255), segment, 10)

        return [worm_x, worm_y]

    def reset_weight(self):
        self.current_weight = 0.0

    def update_weight(self, weight):
        self.current_weight = max(self.current_weight, weight)
