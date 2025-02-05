import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("PATH FINDER")

PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbors = []
        # if row is less than total rows - 1 and not if the box directly below the box being checked is a barrier(DIRECTION DOWN)
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # if row is greater than 0 and not if the box directly above the box being checked is a barrier(DIRECTION UP)
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # if col is less than total cols - 1 and not if the box directly to the right of the box being checked is a barrier(DIRECTION RIGHT)
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # if col is greater than 0 and not if the box directly to the left of the box being checked is a barrier(DIRECTION LEFT)
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):  # HEURISTIC FUNCTION
    # print(p1, p2)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # set g scores of all spots to inf
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0  # set g score of start to 0
    # set f score of all spots to inf
    f_score = {spot: float("inf") for row in grid for spot in row}
    # set f score of start to manhattan dist.
    f_score[start] = h(start.get_pos(), end.get_pos())
    # since priority queue does not let us access elements, put all the elements in an open_set_hash too.
    open_set_hash = {start}

    # while open set is not empty keep running
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # in the first iteration open set has only one item, get it. this will be updated in subsequent iterations
        current = open_set.get()[2]
        # remove current hash from open_set_hash
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)  # make path in purple
            end.make_end()
            return

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def d_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    open_set_hash = {start}
    distances = {spot: float('inf') for row in grid for spot in row}
    distances[start] = 0
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return

        for neighbor in current.neighbors:
            temp_distance = distances[current] + 1
            if temp_distance < distances[neighbor]:
                came_from[neighbor] = current
                distances[neighbor] = temp_distance
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((distances[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):  # FILL GRID WITH SPOT OBJECTS
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):  # DRAW GRID LINES
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))


def draw(win, grid, rows, width):  # DRAW EVERYTHING
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            # print(spot.x, spot.y, spot.width, spot.color)
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):  # GET CLICKED BOX
    gap = width // rows
    y, x = pos
    row = y//gap
    col = x//gap
    return row, col


def main(win, width):  # MAIN FUNCTION WITH GAME LOOP
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # LEFT MOUSE BUTTON
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    # start =
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # RIGHT MOUSE BUTTON
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    d_algorithm(lambda: draw(
                        win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


main(WIN, WIDTH)
# while True:
