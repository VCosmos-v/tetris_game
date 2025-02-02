import pygame
import random
import os
import sqlite3
import time

# Параметры игры
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

# Фигуры Тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Индексы для фигур
SHAPE_COLORS = [
    0,  # I
    1,  # O
    2,  # T
    3,  # L
    4,  # J
    5,  # S
    6   # Z
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font2 = pygame.font.Font(None, 28)

        # Загрузка изображений блоков
        self.block_images = self.load_block_images()

        self.high_score = self.load_high_score()  # Загрузка максимального счета
        self.show_start_screen()

        self.start_time = time.time()  # Начало отсчета времени

    def load_block_images(self):
        # Загрузка изображений блоков из папки data
        block_images = []
        data_dir = os.path.join(os.path.dirname(__file__), 'data')

        # Список имен файлов изображений
        block_filenames = [
            'line.png',
            'cube.png',
            't_shape.png',
            'g_shape1.png',
            'g_shape2.png',
            'z_shape1.png',
            'z_shape2.png'
        ]

        for filename in block_filenames:
            try:
                image_path = os.path.join(data_dir, filename)
                image = pygame.image.load(image_path).convert_alpha()
                # Изменяем размер изображения под размер сетки
                image = pygame.transform.scale(image, (GRID_SIZE - 1, GRID_SIZE - 1))
                block_images.append(image)
            except Exception as e:
                print(f"Ошибка загрузки изображения {filename}: {e}")
                # Если изображение не загрузилось, используем цветной прямоугольник
                block_image = pygame.Surface((GRID_SIZE - 1, GRID_SIZE - 1))
                block_image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
                block_images.append(block_image)

        return block_images

    def load_high_score(self):
        # Загрузка максимального счета из файла
        try:
            with open('max_score.txt', 'r') as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return 0  # Если файл не найден, возвращаем 0
        except ValueError:
            return 0  # Если файл пустой или содержит некорректные данные

    def save_score(self, score):
        # Сохранение счета в базу данных
        conn = sqlite3.connect('tetris_results.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO result (score) VALUES (?)', (score,))
        conn.commit()
        conn.close()

    def show_start_screen(self):
        while True:
            self.screen.fill(BLACK)
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render('TETRIS', True, WHITE)
            easy_text = self.font.render('1. Легкая', True, WHITE)
            medium_text = self.font.render('2 . Средняя', True, WHITE)
            hard_text = self.font.render('3. Сложная', True, WHITE)
            instructions_text1 = self.font.render('Нажмите 1, 2, или 3', True, WHITE)
            instructions_text2 = self.font.render('для выбора сложности', True, WHITE)
            instructions_text3 = self.font.render('^', True, WHITE)
            instructions_text4 = self.font.render('| для поворота фигуры', True, WHITE)
            instructions_text5 = self.font.render('<- | -> для перемещения фигуры', True, WHITE)
            instructions_text6 = self.font2.render('v', True, WHITE)

            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))
            self.screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, SCREEN_HEIGHT // 2 - 110))
            self.screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))
            self.screen.blit(instructions_text1,
                             (SCREEN_WIDTH // 2 - instructions_text1.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(instructions_text2,
                             (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(instructions_text3,
                             (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2 - 4, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(instructions_text4,
                             (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2, SCREEN_HEIGHT // 2 + 90))
            self.screen.blit(instructions_text5,
                             (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2 - 65, SCREEN_HEIGHT // 2 + 130))
            self.screen.blit(instructions_text6,
                             (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2 - 38, SCREEN_HEIGHT // 2 + 145))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.fall_speed = 0.7  # Легкий уровень
                        self.reset_game()
                        return
                    elif event.key == pygame.K_2:
                        self.fall_speed = 0.4  # Средний уровень
                        self.reset_game()
                        return
                    elif event.key == pygame.K_3:
                        self.fall_speed = 0.2  # Сложный уровень
                        self.reset_game()
                        return

    def reset_game(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()  # Получаем следующий блок
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.fall_time = 0
        self.start_time = time.time()  # Сброс времени при перезапуске игры

    def get_new_piece(self):
        shape = random.choice(SHAPES)
        color_index = SHAPE_COLORS[SHAPES.index(shape)]  # Получаем индекс цвета для фигуры
        return shape, color_index

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    (x + 6) * GRID_SIZE,
                    y * GRID_SIZE,
                    GRID_SIZE - 1,
                    GRID_SIZE - 1
                )
                if self.grid[y][x] is not None:
                    block_image = self.block_images[self.grid[y][x]]
                    self.screen.blit(block_image, rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect, 1)

    def draw_sidebar(self):
        # Рисуем серый прямоугольник слева
        sidebar_rect = pygame.Rect(0, 0, 180, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, sidebar_rect)

        # Отрисовка счета
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f'Счёт:', True, WHITE)
        score_value_text = score_font.render(f'{self.score}', True, WHITE)

        # Отображение максимального счета
        high_score_text = score_font.render('Рекорд:', True, WHITE)
        high_score_value_text = score_font.render(f'{self.high_score}', True, WHITE)

        next_text = score_font.render('Далее:', True, WHITE)

        # Позиционирование текста
        self.screen.blit(score_text, (10, 50))
        self.screen.blit(score_value_text, (10, 90))

        self.screen.blit(high_score_text, (10, 150))
        self.screen.blit(high_score_value_text, (10, 190))

        self.screen.blit(next_text, (10, 250))

        # Отрисовка следующей фигуры
        self.draw_next_piece_sidebar()

        # Отображение времени
        elapsed_time = int(time.time() - self.start_time)
        time_text = score_font.render(f'Время: {elapsed_time} сек', True, WHITE)
        self.screen.blit(time_text, (10, 220))

    def draw_next_piece_sidebar(self):
        next_shape, next_color_index = self.next_piece
        for y, row in enumerate(next_shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (x + 1) * GRID_SIZE,
                        (y + 10) * GRID_SIZE,
                        GRID_SIZE - 1,
                        GRID_SIZE - 1
                    )
                    block_image = self.block_images[next_color_index]
                    self.screen.blit(block_image, rect)

    def draw_current_piece(self):
        shape, color_index = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (self.piece_x + x + 6) * GRID_SIZE,
                        (self.piece_y + y) * GRID_SIZE,
                        GRID_SIZE - 1,
                        GRID_SIZE - 1
                    )
                    block_image = self.block_images[color_index]
                    self.screen.blit(block_image, rect)

    def is_valid_move(self, dx, dy):
        shape, _ = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.piece_x + x + dx
                    new_y = self.piece_y + y + dy

                    if (new_x < 0 or new_x >= GRID_WIDTH or
                            new_y >= GRID_HEIGHT or
                            (new_y >= 0 and self.grid[new_y][new_x] is not None)):
                        return False
        return True

    def lock_piece(self):
        shape, color_index = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.piece_y + y][self.piece_x + x] = color_index

        self.clear_lines()
        self.current_piece = self.next_piece  # Устанавливаем следующий блок как текущий
        self.next_piece = self.get_new_piece()  # Получаем новый следующий блок
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0

        if not self.is_valid_move(0, 0):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
                lines_cleared += 1

        score_multipliers = {
            1: 100,
            2: 300,
            3: 500,
            4: 800
        }

        if lines_cleared > 0:
            self.score += score_multipliers.get(lines_cleared, 50)

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)

            # Рисуем боковую панель
            self.draw_sidebar()

            # Рисуем игровое поле и фигуры
            self.draw_grid()
            self.draw_current_piece()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.is_valid_move(-1, 0):
                        self.piece_x -= 1
                    if event.key == pygame.K_RIGHT and self.is_valid_move(1, 0):
                        self.piece_x += 1
                    if event.key == pygame.K_DOWN and self.is_valid_move(0, 1):
                        self.piece_y += 1
                        self.score += 1
                    if event.key == pygame.K_UP:
                        self.current_piece = self.rotate_piece()

            self.fall_time += self.clock.get_time()
            if self.fall_time > 1000 * self.fall_speed:
                if self.is_valid_move(0, 1):
                    self.piece_y += 1
                else:
                    self.lock_piece()
                self.fall_time = 0

            pygame.display.flip()
            self.clock.tick(60)

        self.update_high_score()  # Обновляем максимальный счет, если необходимо
        self.save_score(self.score)  # Сохраняем текущий счет в базу данных
        self.show_game_over()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score  # Обновляем максимальный счет
            with open('max_score.txt', 'w') as f:
                f.write(str(self.high_score))  # Записываем новый рекорд в файл

    def show_game_over(self):
        self.screen.fill(BLACK)
        game_over_font = pygame.font.Font(None, 48)
        score_font = pygame.font.Font(None, 36)

        game_over_text = game_over_font.render('GAME OVER', True, WHITE)
        score_text = score_font.render(f'Ваш счёт: {self.score}', True, WHITE)
        high_score_text = score_font.render(f'Рекорд: {self.high_score}', True, WHITE)  # Отображаем максимальный счет

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(high_score_text, high_score_rect)

        self.save_score(self.score)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        waiting = False

        pygame.quit()

    def rotate_piece(self):
        shape, color_index = self.current_piece
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        if self.is_valid_move(0, 0):
            return rotated_shape, color_index
        return shape, color_index


if __name__ == "__main__":
    game = Tetris()
    game.run()