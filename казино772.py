import pygame
import random

# Настройки
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Слот-Машина")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 60)
small_font = pygame.font.SysFont("Arial", 28)

# Игровые переменные
symbols = ['1', '2', '3', '4', '5', '7']
reels = ['1', '1', '1']
lever_angle = 0
lever_target = 0
blink = False
money = 1000
lever_position = 0

# Таблица выигрышей
payouts = [
    (['7', '7', '7'], 500),
    (['5', '5', '5'], 300),
    (['4', '4', '4'], 200)
]

def draw_interface():
    screen.fill(GRAY)

    # Заголовок
    title = small_font.render("Классическая Слот-Машина", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

    # Барабаны
    for i in range(3):
        pygame.draw.rect(screen, WHITE, (200 + i*130, 200, 100, 100))
        sym = font.render(reels[i], True, RED if blink else BLACK)
        screen.blit(sym, (220 + i*130, 215))

    # Рычаг с анимацией
    pygame.draw.line(screen, BLACK, (700, 200), (700 + int(30 * lever_position), 300), 5)
    pygame.draw.circle(screen, RED, (700 + int(30 * lever_position), 300), 20)

    # Баланс
    balance = small_font.render(f"Баланс: {money}₴", True, WHITE)
    screen.blit(balance, (20, 20))

    # Инструкция
    inst = small_font.render("Нажмите ЛКМ для игры (20₴)", True, WHITE)
    screen.blit(inst, (20, HEIGHT - 40))

    # Таблица выигрышей
    win_table = [
        "777 — 500₴",
        "555 — 300₴",
        "444 — 200₴",
        "3 одинаковых — 100₴",
        "2 '7' — 50₴",
        "2 одинаковых — 20₴"
    ]
    for i, line in enumerate(win_table):
        txt = small_font.render(line, True, YELLOW)
        screen.blit(txt, (500, 350 + i*30))

def get_reward(slots):
    for combo, reward in payouts:
        if slots == combo:
            return reward
    if slots[0] == slots[1] == slots[2]:
        return 100
    if slots.count('7') == 2:
        return 50
    for sym in symbols:
        if slots.count(sym) == 2:
            return 20
    return 0

def animate_lever():
    global lever_position
    for i in range(10):
        lever_position = i / 10.0
        draw_interface()
        pygame.display.flip()
        clock.tick(60)
    for i in range(10):
        lever_position = 1.0 - (i / 10.0)
        draw_interface()
        pygame.display.flip()
        clock.tick(60)
    lever_position = 0

def spin():
    global reels, blink
    animate_lever()
    result = []
    roll = random.random()
    if roll < 0.109:
        result = ['7', '7', '7']
    elif roll < 0.16:
        result = ['5', '5', '5']
    elif roll < 0.20:
        result = ['4', '4', '4']
    else:
        for _ in range(15):
            reels = [random.choice(symbols) for _ in range(3)]
            draw_interface()
            pygame.display.flip()
            clock.tick(30)
        result = [random.choice(symbols) for _ in range(3)]

    reels = result
    reward = get_reward(reels)
    if reels == ['7', '7', '7']:
        blink_effect()
    return reward

def blink_effect():
    global blink
    for _ in range(6):
        blink = not blink
        draw_interface()
        pygame.display.flip()
        pygame.time.delay(200)
    blink = False

running = True
while running:
    draw_interface()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if money >= 20:
                money -= 20
                reward = spin()
                money += reward

    clock.tick(60)

pygame.quit()
