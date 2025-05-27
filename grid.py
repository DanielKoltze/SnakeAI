from settings import MAP_WIDTH,MAP_HEIGHT,CELL_SIZE
from cell import Cell

class Grid:

    def __init__(self):
        self.cells = self.create_cells()


    def draw(self,win):
        for cell in self.cells:
            cell.draw(win)

    def create_cells(self):
        x = MAP_WIDTH // CELL_SIZE
        y = MAP_HEIGHT // CELL_SIZE
        grid = []
        for i in range(x):
            for j in range(y):
                grid.append(Cell(i,j))
        return grid