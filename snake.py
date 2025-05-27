from helper import get_rect,add_tuples
import pygame

class Snake:
    def __init__(self,starting_position,starting_direciton):
        self.parts = [starting_position,(1,0),(2,0),(3,0),(4,0)]
        self.color = (255, 0, 0)
        self.direction = starting_direciton

    def draw(self,win):
        for part in self.parts:
            rect = get_rect(part[0],part[1])
            pygame.draw.rect(win, self.color, rect)

    def move(self):
       del self.parts[0]
       last = self.parts[-1]
       self.parts.append(add_tuples(last,self.direction.value))

    def change_direction(self,direction):
        if self.direction.opposite() == direction or self.direction == direction:
            return
        self.direction = direction
        
    def grow(self) -> None:
        last_part = self.parts[0]
        opposite_direction = self.direction.opposite()
        new_part = add_tuples(last_part,opposite_direction.value)
        self.parts.insert(0,new_part)
    
    def eat(self,food) -> bool:
        first_part = self.parts[-1]
        for f in food:
            if f.position == first_part:
                food.remove(f)
                return True
        return False

    def wall_collision(self,grid):
        first_part = self.parts[-1]
        for cell in grid:
            if cell.position == first_part:
                return False
        return True
    
    def snake_collision(self):
        copy_snake = self.parts[:]
        first_part = copy_snake.pop()
        if first_part in copy_snake:
            return True
        return False
