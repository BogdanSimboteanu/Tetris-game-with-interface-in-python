import pygame
import random

# Define constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Define shapes and their colors
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]]   # J shape
]

SHAPE_COLORS = [CYAN, GREEN, RED, YELLOW, BLUE, ORANGE, PURPLE]

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

# Function to check if the current piece is valid in the grid
def is_valid_move(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                    return False
                if y + off_y >= 0 and grid[y + off_y][x + off_x]:
                    return False
    return True

# Function to rotate the shape
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Function to clear completed lines
def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_grid)
    new_grid = [[0] * GRID_WIDTH] * lines_cleared + new_grid
    return new_grid, lines_cleared

# Main game loop
def main():
    clock = pygame.time.Clock()

    # Create an empty grid
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    # Randomly select a shape
    shape_index = random.randint(0, len(SHAPES) - 1)
    shape = SHAPES[shape_index]
    color = SHAPE_COLORS[shape_index]
    offset = [GRID_WIDTH // 2 - len(shape[0]) // 2, 0]  # Start in the middle

    game_over = False
    while not game_over:
        screen.fill(BLACK)
        draw_grid()

        # Check for events (key presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_move(grid, shape, [offset[0] - 1, offset[1]]):
                        offset[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid_move(grid, shape, [offset[0] + 1, offset[1]]):
                        offset[0] += 1
                elif event.key == pygame.K_DOWN:
                    if is_valid_move(grid, shape, [offset[0], offset[1] + 1]):
                        offset[1] += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate(shape)
                    if is_valid_move(grid, rotated_shape, offset):
                        shape = rotated_shape

        # Move the shape down
        if is_valid_move(grid, shape, [offset[0], offset[1] + 1]):
            offset[1] += 1
        else:
            # Place the shape in the grid
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[offset[1] + y][offset[0] + x] = color

            # Check for completed lines
            grid, lines_cleared = clear_lines(grid)
            if lines_cleared > 0:
                print(f"Lines cleared: {lines_cleared}")

            # Reset for next piece
            shape_index = random.randint(0, len(SHAPES) - 1)
            shape = SHAPES[shape_index]
            color = SHAPE_COLORS[shape_index]
            offset = [GRID_WIDTH // 2 - len(shape[0]) // 2, 0]

            # Check for game over
            if not is_valid_move(grid, shape, offset):
                game_over = True

        # Draw the grid and the current shape
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x]:
                    pygame.draw.rect(screen, grid[y][x],
                                     (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, color,
                                     ((offset[0] + x) * BLOCK_SIZE, (offset[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()

# Start the game
if __name__ == '__main__':
    main()