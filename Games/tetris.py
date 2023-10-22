import pygame
import random
import copy

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Определение размеров окна
size = (500, 500)

# Определение размеров и положения области для отображения сохраненной фигуры
SAVED_FIGURE_AREA_X = 20
SAVED_FIGURE_AREA_Y = 60
SAVED_FIGURE_AREA_WIDTH = 6
SAVED_FIGURE_AREA_HEIGHT = 6

# Определение размеров и положения области для отображения следующих фигур
NEXT_FIGURES_AREA_X = 340
NEXT_FIGURES_AREA_Y = 60
NEXT_FIGURES_AREA_WIDTH = 6
NEXT_FIGURES_AREA_HEIGHT = 12

# Инициализация Pygame
pygame.init()

# Установка заголовка окна
pygame.display.set_caption("Tetris")

# Определение класса Figure
class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

# Определение класса Tetris
class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.saved_figure = None
        self.next_figures = [Figure(0, 0) for _ in range(5)]

        self.height = height
        self.width = width
        self.field = []
        self.state = "start"
        self.tetris_bonus = 1500  # Бонус за Тетрис
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = self.next_figures.pop(0)
        self.next_figures.append(Figure(0, 0))

    def save_figure(self):
        if self.saved_figure is None:
            self.saved_figure = Figure(0, 0)
            self.new_figure()
        else:
            self.figure, self.saved_figure = self.saved_figure, self.figure
            self.figure.x, self.figure.y = 3, 0
            self.figure.rotation = 0

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def add_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 700
        elif lines_cleared == 4:
            self.score += self.tetris_bonus

    def break_lines(self):
        lines_cleared = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines_cleared += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.add_score(lines_cleared)

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def update_next_figures(self):
        for i in range(4):
            self.next_figures[i] = self.next_figures[i + 1]
        self.next_figures[4] = Figure(0, 0)

    def ghost_intersects(self, ghost_figure):
        for i in range(4):
            for j in range(4):
                if (
                    i * 4 + j in ghost_figure.image()
                    and (
                        i + ghost_figure.y > self.height - 1
                        or j + ghost_figure.x > self.width - 1
                        or j + ghost_figure.x < 0
                        or self.field[i + ghost_figure.y][j + ghost_figure.x] > 0
                    )
                ):
                    return True
        return False

# Определение переменных
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

# Определение основного цикла
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 10
game = Tetris(20, 10)
pressing_down = False
done = False

auto_move_down_counter = 0

while not done:
    if game.figure is None:
        game.new_figure()

    auto_move_down_counter += 1
    if auto_move_down_counter >= (fps // game.level // 1):
        game.go_down()
        auto_move_down_counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
            if event.key == pygame.K_TAB:
                game.save_figure()

    screen.fill(DARK_GRAY)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        # Отрисовка "призрака" фигуры
        ghost_figure = copy.deepcopy(game.figure)
        while not game.ghost_intersects(ghost_figure):
            ghost_figure.y += 1
        ghost_figure.y -= 1
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in ghost_figure.image():
                    pygame.draw.rect(screen, (GRAY[0], GRAY[1], WHITE[2], 100), [game.x + game.zoom * (j + ghost_figure.x) + 1, game.y + game.zoom * (i + ghost_figure.y) + 1, game.zoom - 2, game.zoom - 2])
        
        # Отрисовка текущей фигуры
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * (j + game.figure.x) + 1, game.y + game.zoom * (i + game.figure.y) + 1, game.zoom - 2, game.zoom - 2])

    # Отображение сохраненной фигуры слева от игрового поля
    saved_figure = game.saved_figure
    if saved_figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in saved_figure.image():
                    pygame.draw.rect(screen, WHITE, [SAVED_FIGURE_AREA_X + game.zoom * j + 1, SAVED_FIGURE_AREA_Y + game.zoom * i + 1, game.zoom - 2, game.zoom - 2])

    # Отображение следующих 5 фигур справа от игрового поля (сверху вниз)
    for i, next_figure in enumerate(game.next_figures):
        for j in range(4):
            for k in range(4):
                p = j * 4 + k
                if p in next_figure.image():
                    pygame.draw.rect(screen, WHITE, [NEXT_FIGURES_AREA_X + k * game.zoom, NEXT_FIGURES_AREA_Y + i * (4 * game.zoom) + j * game.zoom, game.zoom - 2, game.zoom - 2])

    # Отображение счета
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {game.score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
