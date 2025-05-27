import pygame
from settings import MAP_HEIGHT,MAP_WIDTH,FPS
from grid import Grid
from snake import Snake
from direction import Direction
from food import Food

class Game:
    def __init__(self,ai_mode = False):
        pygame.init()
        self.win = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        self.clock = pygame.time.Clock()
        self.ai_mode = ai_mode
        self.score = 0
        self.run = True
        self.font = pygame.font.Font(None, 36)
        self.grid = Grid()
        self.snake = Snake((0,0),Direction.RIGHT)
        self.food = [Food(self.snake,self.grid.cells)]

    def start_game(self):
        while self.run:
            self.draw()
            self.update()

    def update(self):
        self.clock.tick(FPS)
        if not self.ai_mode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_d:
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_s:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_a:
                        self.snake.change_direction(Direction.LEFT)

                
        self.snake.move()

        if not self.ai_mode:
            if self.snake.eat(self.food):
                self.snake.grow()
                self.food.append(Food(self.snake,self.grid.cells))

            if self.snake.wall_collision(self.grid.cells) or self.snake.snake_collision():
                self.run = False

    def draw(self):
        self.win.fill((0, 0, 0))

        self.grid.draw(self.win)

        self.snake.draw(self.win)

        for food in self.food:
            food.draw(self.win)
       
        pygame.display.update()

#game = Game()
#game.start_game()