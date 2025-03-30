import pygame
import sys
import math

pygame.init()

# настройка экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
DRAW_MODE = 'rectangle'  # дефолт это тікбұрыш
current_color = (0, 0, 0)  # қара это дефолд

# цветы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
colors = [RED, GREEN, BLUE, YELLOW, ORANGE]

# настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drawing Program")

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 24)


drawing_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
drawing_surface.fill(WHITE)

# -------------------
# функции
# -------------------

def draw_button(color, x, y, width, height, label):
    
    pygame.draw.rect(screen, color, (x, y, width, height))
    text = font.render(label, True, BLACK)
    screen.blit(text, (x + 10, y + 10))

def draw_shape(surface, shape, x, y, color, width=0, height=0):
    if shape == 'rectangle':
        pygame.draw.rect(surface, color, (x, y, width, height))
    elif shape == 'square':
        side = min(abs(width), abs(height))
        pygame.draw.rect(surface, color, (x, y, side, side))
    elif shape == 'circle':
        radius = int(((width ** 2 + height ** 2) ** 0.5) / 2)
        pygame.draw.circle(surface, color, (x, y), radius)
    elif shape == 'right_triangle':
        pygame.draw.polygon(surface, color, [(x, y), (x + width, y), (x, y + height)])
    elif shape == 'equilateral_triangle':
        h = (math.sqrt(3) / 2) * abs(width)
        apex_x = x + width / 2
        apex_y = y - h if height < 0 else y + h
        pygame.draw.polygon(surface, color, [(x, y), (x + width, y), (apex_x, apex_y)])
    elif shape == 'rhombus':
        pygame.draw.polygon(surface, color, [
            (x + width / 2, y),
            (x + width, y + height / 2),
            (x + width / 2, y + height),
            (x, y + height / 2)
        ])
    elif shape == 'pencil':
        pygame.draw.circle(surface, color, (x, y), 2)
    elif shape == 'erase':
        pygame.draw.circle(surface, WHITE, (x, y), 10)

# цикл игры
def game_loop():
    global DRAW_MODE, current_color
    drawing = False
    start_pos = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # мышка ивент если нажать то это будет
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # цвет в форма кнопки
                if event.button == 1:
                    if 10 <= mouse_x <= 110 and 10 <= mouse_y <= 50:
                        current_color = RED
                    elif 120 <= mouse_x <= 220 and 10 <= mouse_y <= 50:
                        current_color = GREEN
                    elif 230 <= mouse_x <= 330 and 10 <= mouse_y <= 50:
                        current_color = BLUE
                    elif 340 <= mouse_x <= 440 and 10 <= mouse_y <= 50:
                        current_color = YELLOW
                    elif 450 <= mouse_x <= 550 and 10 <= mouse_y <= 50:
                        current_color = ORANGE
                    elif 560 <= mouse_x <= 660 and 10 <= mouse_y <= 50:
                        DRAW_MODE = 'erase'
                    elif 670 <= mouse_x <= 770 and 10 <= mouse_y <= 50:
                        DRAW_MODE = 'rectangle'
                    elif 670 <= mouse_x <= 770 and 60 <= mouse_y <= 100:
                        DRAW_MODE = 'circle'
                    elif 670 <= mouse_x <= 770 and 110 <= mouse_y <= 150:
                        DRAW_MODE = 'pencil'
                    elif 10 <= mouse_x <= 110 and 60 <= mouse_y <= 100:
                        DRAW_MODE = 'square'
                    elif 120 <= mouse_x <= 220 and 60 <= mouse_y <= 100:
                        DRAW_MODE = 'right_triangle'
                    elif 230 <= mouse_x <= 330 and 60 <= mouse_y <= 100:
                        DRAW_MODE = 'equilateral_triangle'
                    elif 340 <= mouse_x <= 440 and 60 <= mouse_y <= 100:
                        DRAW_MODE = 'rhombus'
                    else:
                        drawing = True
                        start_pos = (mouse_x, mouse_y)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    width = mouse_x - start_pos[0]
                    height = mouse_y - start_pos[1]
                    # форма салуга условие
                    if DRAW_MODE not in ['pencil', 'erase']:
                        draw_shape(drawing_surface, DRAW_MODE, start_pos[0], start_pos[1], current_color, width, height)
                drawing = False
                start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing and start_pos:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    width = mouse_x - start_pos[0]
                    height = mouse_y - start_pos[1]
                    if DRAW_MODE in ['pencil', 'erase']:
                        draw_shape(drawing_surface, DRAW_MODE, mouse_x, mouse_y, current_color)

        # Рисовать интервейс и инструменты
        screen.fill(GRAY)
        screen.blit(drawing_surface, (0, 0))

        # проверка форму если не карандаш или стерка
        if drawing and start_pos and DRAW_MODE not in ['pencil', 'erase']:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            width = mouse_x - start_pos[0]
            height = mouse_y - start_pos[1]
            draw_shape(screen, DRAW_MODE, start_pos[0], start_pos[1], current_color, width, height)

        # рисовать кнопку цвета
        draw_button(RED, 10, 10, 100, 40, "Red")
        draw_button(GREEN, 120, 10, 100, 40, "Green")
        draw_button(BLUE, 230, 10, 100, 40, "Blue")
        draw_button(YELLOW, 340, 10, 100, 40, "Yellow")
        draw_button(ORANGE, 450, 10, 100, 40, "Orange")
        draw_button(WHITE, 560, 10, 100, 40, "Erase")
        
        # рисовать кнопку форм
        draw_button(GRAY, 670, 10, 100, 40, "Rectangle")
        draw_button(GRAY, 670, 60, 100, 40, "Circle")
        draw_button(GRAY, 670, 110, 100, 40, "Pencil")
        draw_button(GRAY, 10, 60, 100, 40, "Square")
        draw_button(GRAY, 120, 60, 100, 40, "R Triangle")
        draw_button(GRAY, 230, 60, 100, 40, "E Triangle")
        draw_button(GRAY, 340, 60, 100, 40, "Rhombus")

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()