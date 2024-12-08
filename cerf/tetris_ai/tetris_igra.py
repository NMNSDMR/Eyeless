import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

COLORS = [
    (0, 0, 0), 
    (255, 0, 0),  
    (0, 255, 0), 
    (0, 0, 255), 
    (255, 255, 0), 
    (255, 0, 255), 
    (0, 255, 255), 
]

SHAPES = [
    [[1, 1, 1, 1]], I
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]], 
    [[0, 1, 1], [1, 1, 0]], 
    [[1, 1, 0], [0, 1, 1]],  
]

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.randint(1, len(COLORS) - 1)
        self.x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.y = 0
        self.game_over = False

    def can_move(self, dx, dy, shape=None):
        shape = shape or self.current_shape
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True

    def lock_shape(self):
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.y + i][self.x + j] = self.current_color
        self.clear_lines()
        self.spawn_new_shape()

    def clear_lines(self):
        self.grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        while len(self.grid) < GRID_HEIGHT:
            self.grid.insert(0, [0] * GRID_WIDTH)

    def spawn_new_shape(self):
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.randint(1, len(COLORS) - 1)
        self.x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.y = 0
        if not self.can_move(0, 0):
            self.game_over = True

    def step(self, action):
        if action == 0 and self.can_move(-1, 0):
            self.x -= 1
        elif action == 1 and self.can_move(1, 0):
            self.x += 1
        elif action == 2 and self.can_move(0, 1):
            self.y += 1
        elif action == 3:
            rotated = rotate_shape(self.current_shape)
            if self.can_move(0, 0, rotated):
                self.current_shape = rotated

        if self.can_move(0, 1):
            self.y += 1
        else:
            self.lock_shape()

    def render(self, screen):
        screen.fill((0, 0, 0))
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        COLORS[cell],
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        COLORS[self.current_color],
                        (
                            (self.x + j) * BLOCK_SIZE,
                            (self.y + i) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )
        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    tetris = Tetris()

    while not tetris.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tetris.step(0)
        if keys[pygame.K_RIGHT]:
            tetris.step(1)
        if keys[pygame.K_DOWN]:
            tetris.step(2)
        if keys[pygame.K_UP]:
            tetris.step(3)

        tetris.step(-1)
        tetris.render(screen)
        clock.tick(10)

    print("Game Over")

if __name__ == "__main__":
    main()
