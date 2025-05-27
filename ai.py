import neat
import pickle
import os
from game import Game
from settings import MAP_HEIGHT,MAP_WIDTH,CELL_SIZE
from direction import Direction
from food import Food

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        game = Game(ai_mode=True)
        snake = game.snake
        grid = game.grid
        food = game.food[0]
        steps = 0
        max_steps = 500

        while game.run and steps < max_steps:
            inputs = get_ai_inputs(snake, food, grid)
            output = net.activate(inputs)
            action = output.index(max(output))  # 0=venstre, 1=ligeud, 2=højre
            new_dir = get_new_direction(snake.direction, action)
            snake.change_direction(new_dir)

            game.update()
            game.draw()
            steps += 1

            # Belønning og straf
            if snake.eat([food]):
                genome.fitness += 10
                snake.grow()
                game.food.append(Food(snake, grid.cells))
                food = game.food[-1]
                steps = 0  # reset step count ved spisning
            elif snake.wall_collision(grid.cells) or snake.snake_collision():
                genome.fitness -= 15
                game.run = False
            else:
                genome.fitness += 1  # overlevelse


def get_ai_inputs(snake, food, grid):
    head_x, head_y = snake.head
    food_x, food_y = food.position
    grid_width = MAP_WIDTH // CELL_SIZE
    grid_height = MAP_HEIGHT // CELL_SIZE

    danger_straight = danger_in_direction(snake, grid, "STRAIGHT")
    danger_left = danger_in_direction(snake, grid, "LEFT")
    danger_right = danger_in_direction(snake, grid, "RIGHT")

    dist_wall_straight = distance_to_wall(snake, grid_width, grid_height, "STRAIGHT")
    dist_wall_left = distance_to_wall(snake, grid_width, grid_height, "LEFT")
    dist_wall_right = distance_to_wall(snake, grid_width, grid_height, "RIGHT")

    dist_body_straight = distance_to_body(snake, "STRAIGHT")
    dist_body_left = distance_to_body(snake, "LEFT")
    dist_body_right = distance_to_body(snake, "RIGHT")

    food_dir_x = sign(food_x - head_x)
    food_dir_y = sign(food_y - head_y)
    food_dist_x = abs(food_x - head_x) / grid_width
    food_dist_y = abs(food_y - head_y) / grid_height

    directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    dir_up = int(snake.direction == Direction.UP)
    dir_right = int(snake.direction == Direction.RIGHT)
    dir_down = int(snake.direction == Direction.DOWN)
    dir_left = int(snake.direction == Direction.LEFT)

    length_norm = len(snake.parts) / (grid_width * grid_height)

    inputs = [
        int(danger_straight),
        int(danger_left),
        int(danger_right),
        dist_wall_straight,
        dist_wall_left,
        dist_wall_right,
        dist_body_straight,
        dist_body_left,
        dist_body_right,
        food_dir_x,
        food_dir_y,
        food_dist_x,
        food_dist_y,
        dir_up,
        dir_right,
        dir_down,
        dir_left,
        length_norm
    ]

    return inputs


def distance_to_wall(snake, grid_width, grid_height, relative_dir):
    directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    idx = directions.index(snake.direction)

    if relative_dir == "LEFT":
        check_dir = directions[(idx - 1) % 4]
    elif relative_dir == "RIGHT":
        check_dir = directions[(idx + 1) % 4]
    else:
        check_dir = snake.direction

    x, y = snake.head
    dx, dy = check_dir.value
    distance = 0

    while 0 <= x + dx < grid_width and 0 <= y + dy < grid_height:
        x += dx
        y += dy
        distance += 1

    return distance / max(grid_width, grid_height)  # normaliseret


def distance_to_body(snake, relative_dir):
    directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    idx = directions.index(snake.direction)

    if relative_dir == "LEFT":
        check_dir = directions[(idx - 1) % 4]
    elif relative_dir == "RIGHT":
        check_dir = directions[(idx + 1) % 4]
    else:
        check_dir = snake.direction

    x, y = snake.head
    dx, dy = check_dir.value
    distance = 0

    while True:
        x += dx
        y += dy
        distance += 1
        if (x, y) in snake.parts:
            return 1 / distance  # større værdi = tættere
        # Stop hvis uden for grid (kan justeres hvis du har grid størrelse her)
        if x < 0 or y < 0:
            break
    return 0  # Ingen krop fundet i den retning


def sign(n):
    return (n > 0) - (n < 0)


def danger_in_direction(snake, grid, relative_dir):
    directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    idx = directions.index(snake.direction)

    if relative_dir == "LEFT":
        check_dir = directions[(idx - 1) % 4]
    elif relative_dir == "RIGHT":
        check_dir = directions[(idx + 1) % 4]
    else:
        check_dir = snake.direction

    next_x = snake.head[0] + check_dir.value[0]
    next_y = snake.head[1] + check_dir.value[1]

    grid_width = MAP_WIDTH // CELL_SIZE
    grid_height = MAP_HEIGHT // CELL_SIZE

    return (
        next_x < 0 or next_x >= grid_width or
        next_y < 0 or next_y >= grid_height or
        (next_x, next_y) in snake.parts
    )

def get_new_direction(current, action):
    directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
    idx = directions.index(current)
    if action == 0:
        return directions[(idx - 1) % 4]
    elif action == 1:
        return current
    elif action == 2:
        return directions[(idx + 1) % 4]




def get_latest_checkpoint(dir,file_start_with):
    file_names = []
    newest_file_no = 0

    for file in os.listdir(dir):
        if(file.startswith(file_start_with)):
            file_names.append(file)
    
    if len(file_names) == 0:
        return None

    for file_name in file_names:
        arr = file_name.split('-')
        no = int(arr[-1])
        if no > newest_file_no:
            newest_file_no = int(no)
    
    return dir + '/' + file_start_with + str(newest_file_no)


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)