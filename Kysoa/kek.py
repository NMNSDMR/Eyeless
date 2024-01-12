import pygame
import random
import time

pygame.init()

width, height = 1600, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("'эщкере")

background_color = (255, 255, 255)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x, y = random.randint(50, width - 50), random.randint(50, height - 50)
    text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    font = pygame.font.Font(None, 36)
    text = font.render("ТЕКСТ", True, text_color) #вместо текста свою хуйню

    screen.blit(text, (x, y))

    pygame.display.flip()

    clock.tick(0.7)
    time.sleep(0.7)

pygame.quit()
#СОЗДАЕТ В РАНДОМНОМ МЕСТЕ ТЕКСТ РАЗНОГО ЦВЕТА 
