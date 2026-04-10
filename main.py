import pygame
import random
import heapq

# ---------------- CONFIG ----------------
WIDTH = 600
ROWS = 30
CELL_SIZE = WIDTH // ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ---------------- GRID ----------------
def create_grid():
    grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]

    for i in range(ROWS):
        for j in range(ROWS):
            if random.random() < 0.2:  # obstacle density
                grid[i][j] = 1

    return grid

# ---------------- DRAW ----------------
def draw_grid(win, grid):
    for i in range(ROWS):
        for j in range(ROWS):
            color = WHITE
            if grid[i][j] == 1:
                color = BLACK

            pygame.draw.rect(win, color,
                             (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(win, GREY,
                             (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# ---------------- A* ALGORITHM ----------------
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, grid):
    neighbors = []
    directions = [(0,1),(1,0),(-1,0),(0,-1)]

    for d in directions:
        x = node[0] + d[0]
        y = node[1] + d[1]

        if 0 <= x < ROWS and 0 <= y < ROWS:
            if grid[x][y] == 0:
                neighbors.append((x, y))

    return neighbors

def a_star(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in get_neighbors(current, grid):
            temp_g = g_score[current] + 1

            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score = temp_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return []

# ---------------- MAIN ----------------
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("AI Autonomous Navigation")

    grid = create_grid()

    start = (0, 0)
    goal = (ROWS - 1, ROWS - 1)

    # Ensure start & goal are free
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    path = a_star(grid, start, goal)

    agent_pos = start
    step = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(5)
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw grid
        draw_grid(win, grid)

        # Draw path
        for node in path:
            x, y = node
            pygame.draw.rect(win, GREEN,
                             (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Move agent
        if step < len(path):
            agent_pos = path[step]
            step += 1

        # Draw agent
        x, y = agent_pos
        pygame.draw.rect(win, BLUE,
                         (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw goal
        pygame.draw.rect(win, RED,
                         (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()