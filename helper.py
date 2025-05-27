from settings import CELL_SIZE

def get_rect(x,y):
    return (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

def add_tuples(tuple1,tuple2):
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]) 