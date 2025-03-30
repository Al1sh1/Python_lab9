import pygame
import random
import sys
import time

pygame.init()

# настройка
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
FPS = 30

# цвет
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

# характеристика жылана
SNAKE_SIZE = 10
SNAKE_SPEED = 10

# время игры 
clock = pygame.time.Clock()

# шрифт для очка и уровения
font = pygame.font.SysFont("Comicsans", 24)
font_small = pygame.font.SysFont("Comicsans", 16)  # Smaller font for instructions

# -------------------
# функции
# -------------------
def draw_text(text, font, color, surface, x, y):
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def generate_food(snake_body):
    food_x = random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    food_y = random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    while (food_x, food_y) in snake_body:  # перечь еды от теле жылана не появился что бы 
        food_x = random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    
    # Каждый продукт питания даст случайную оценку (от 1 до 5 баллов)
    food_weight = random.randint(1, 5)
    
    # Назначьте таймер для исчезновения еды через случайное время (от 3 до 6 секунд)
    food_timer = time.time()
    
    return food_x, food_y, food_weight, food_timer

def game_loop():
    # Исходное положение змеи и ее тело
    snake_x = SCREEN_WIDTH // 2
    snake_y = SCREEN_HEIGHT // 2
    snake_body = [(snake_x, snake_y)]
    snake_direction = "RIGHT"

    food_x, food_y, food_weight, food_timer = generate_food(snake_body)

    # игра сам
    score = 0
    level = 1
    speed = SNAKE_SPEED
    running = True

    while running:
        clock.tick(speed)

        # ивенты
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"

        #  жылан кимылдауы
        if snake_direction == "LEFT":
            snake_x -= SNAKE_SIZE
        elif snake_direction == "RIGHT":
            snake_x += SNAKE_SIZE
        elif snake_direction == "UP":
            snake_y -= SNAKE_SIZE
        elif snake_direction == "DOWN":
            snake_y += SNAKE_SIZE

        # добавление роста после еды
        new_head = (snake_x, snake_y)
        snake_body.insert(0, new_head)

        # сиел ли еду земя
        if snake_x == food_x and snake_y == food_y:
            score += food_weight  # добавлени массы еды для очка
            if score % 3 == 0:  # плюс уровень после трех еды
                level += 1
                speed += 3  # плюс скорость
            food_x, food_y, food_weight, food_timer = generate_food(snake_body)  # Generate new food
        else:
            snake_body.pop()  # убрать хвост если не сиел еду

        #граница
        if snake_x < 0 or snake_x >= SCREEN_WIDTH or snake_y < 0 or snake_y >= SCREEN_HEIGHT:
            running = False

        # удар тисе конец
        if (snake_x, snake_y) in snake_body[1:]:
            running = False

        # проверка еды что бы оно исчез после 5 сек игры
        if time.time() - food_timer > 5:
            food_x, food_y, food_weight, food_timer = generate_food(snake_body)  # Reset food

        # рисование поля
        screen.fill(BLACK)

        # рисование жылан
        for segment in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

        # рисование еды
        pygame.draw.rect(screen, RED, pygame.Rect(food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

        # поставить очко и уровень
        draw_text(f"Score: {score}", font, WHITE, screen, 70, 20)
        draw_text(f"Level: {level}", font, WHITE, screen, SCREEN_WIDTH - 70, 20)

        pygame.display.update()

    # конец игры
    screen.fill(BLACK)
    draw_text("GAME OVER", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(f"Final Score: {score}", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press Q to Quit or R to Restart", font_small, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    pygame.display.update()

    # ожидание рестарта или выхода
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    game_loop()  # рестарт игры

# -------------------
# Старт игры
# -------------------
if __name__ == "__main__":
    game_loop()
