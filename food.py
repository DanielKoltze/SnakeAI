import random
from helper import get_rect
import pygame


class Food:
    def __init__(self,snake,grid) -> None:
        self.position = self.spawn(snake,grid)
        self.color = (0, 255, 0)

    def draw(self,win) -> None:
        if self.position is not None:
            rect = get_rect(self.position[0],self.position[1])
            pygame.draw.rect(win, self.color, rect)

    def spawn(self,snake,grid):
        free_cells = [cell for cell in grid if cell.position not in snake.parts]
        if not free_cells:
            return None
        
        chosen_cell = random.choice(free_cells)
        return chosen_cell.position