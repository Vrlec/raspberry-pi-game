#!/usr/bin/env python
import pygame
import RPi.GPIO as GPIO
import random
import sys
# =====================================================================
# GPIO setup
# =====================================================================
SIA = 40
SIB = 38
SW = 36

def configure_channels():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SIA, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(SIB, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# =====================================================================
# Pygame configuration
# =====================================================================
game_running = True
FPS = 150
SCREEN_WIDTH,SCREEN_HEIGHT = 600, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raspberry Pi Projekt")

# =====================================================================
# Player
# =====================================================================
class Player(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()  # Do not pass self here
        self.image = pygame.image.load("./assets/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx: float, dy: float):
        if 50 <= self.rect.x + dx <= SCREEN_HEIGHT - 50:
            self.rect.x += dx
        self.rect.y += dy

player = Player(250, 500)

# =========================================================
# Background stars
# =====================================================================
MAX_STARS = 75
MIN_STAR_WIDTH, MAX_STAR_WIDTH = 1, 5
MIN_STAR_LENGTH, MAX_STAR_LENGTH = 25, 125
stars = [pygame.Rect((random.randint(0, SCREEN_WIDTH), random.randint(-10, SCREEN_HEIGHT), random.randint(MIN_STAR_WIDTH, MAX_STAR_WIDTH), random.randint(MIN_STAR_LENGTH, MAX_STAR_LENGTH))) for i in range(MAX_STARS)]

# =========================================================
# Enemies
# =====================================================================
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()  # Do not pass self here
        self.passed_player_state_now = False
        self.passed_player_state_before = False
        self.image = pygame.image.load("./assets/enemy.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx: float, dy: float):
        enemies_dodged = 0
        self.passed_player_state_now = self.rect.y >= 500
        if self.passed_player_state_now and self.passed_player_state_before != self.passed_player_state_now:
            enemies_dodged += 1

        if 50 <= self.rect.x + dx <= SCREEN_HEIGHT - 50:
            self.rect.x += dx
        if self.rect.y > SCREEN_HEIGHT + 50:
            self.rect.x = random.randint(50, SCREEN_WIDTH + 50)
            self.rect.y = random.randint(-350, -50)
        else:
            self.rect.y += dy
        self.passed_player_state_before = self.passed_player_state_now
        return enemies_dodged

enemies = [Enemy(random.randint(50, 550), random.randint(-400, -10)) for asdf in range(10)]
enemies_dodged = 0
alive = True

if __name__ == '__main__' :
    configure_channels()
    pygame.init()
    clock = pygame.time.Clock()
    last_state = (GPIO.input(SIA), GPIO.input(SIB))
    font_path = pygame.font.match_font("arial")
    font = pygame.font.Font(font_path, 74)

    while game_running:
        screen.fill((0, 0, 0))
        death_surface = font.render("you died.", True, (255, 0, 0))
        death_rect = death_surface.get_rect(center = (300, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        if GPIO.input(SW) == 0:
            player = Player(250, 500)
            stars = [pygame.Rect((random.randint(0, SCREEN_WIDTH), random.randint(-10, SCREEN_HEIGHT), random.randint(MIN_STAR_WIDTH, MAX_STAR_WIDTH), random.randint(MIN_STAR_LENGTH, MAX_STAR_LENGTH))) for i in range(MAX_STARS)]
            enemies = [Enemy(random.randint(50, 550), random.randint(-300, -25)) for asdf in range(10)]
            enemies_dodged = 0
            alive = True

        if alive == True:
            for star in stars:
                pygame.draw.rect(screen, (75, 75, 75), star)
                if star.y >= SCREEN_WIDTH:
                    star.move_ip(0, -745)
                else:
                    star.move_ip(0, random.randint(5, 6))
            for enemy in enemies:
                screen.blit(enemy.image, enemy.rect)
                enemies_dodged += enemy.move(0, random.randint(1, 2))
                if pygame.sprite.collide_rect(player, enemy):
                    alive = False      

            screen.blit(player.image, player.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
            current_state = (GPIO.input(SIA), GPIO.input(SIB))
            if current_state != last_state:  # Detect state change
                if last_state == (0, 0) and current_state == (0, 1):
                    player.move(45, 0)
                elif last_state == (0, 0) and current_state == (1, 0):
                    player.move(-45, 0)
            last_state = current_state
        else:
            screen.blit(death_surface, death_rect)

        number_surface = font.render(str(enemies_dodged), True, (255, 255, 255))
        number_rect = number_surface.get_rect(topleft = (100, 100))
        
        screen.blit(number_surface, number_rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()