import pygame
from settings import CELL_SIZE
from helper import get_rect

class Cell:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.position = (self.x,self.y)

    def draw(self,win):
        rect = get_rect(self.x,self.y)
        pygame.draw.rect(win, (255, 255, 255), rect)
        pygame.draw.rect(win, (0, 0, 0), rect, 1)