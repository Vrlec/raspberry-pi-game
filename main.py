#!/usr/bin/env python
import pygame
import RPi.GPIO as GPIO
import random
# =====================================================================
# Pin configuration
# =====================================================================
SIA = 40
SIB = 38
SW = 36

# GPIO setup
def configure_channels():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SIA, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(SIB, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# =====================================================================
# Pygame configuration
# =====================================================================
game_running = True
FPS = 120
SCREEN_WIDTH,SCREEN_HEIGHT = 600, 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raspberry Pi Projekt für die Petrus")

# =====================================================================
# Controls functions
# =====================================================================
def button_callback(asdfsdfasdf):
    print("Button pressed!")

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
MAX_STARS = 50
MIN_STAR_WIDTH, MAX_STAR_WIDTH = 1, 7
MIN_STAR_LENGTH, MAX_STAR_LENGTH = 25, 125
stars = [pygame.Rect((random.randint(0, SCREEN_WIDTH), random.randint(-10, SCREEN_HEIGHT), random.randint(MIN_STAR_WIDTH, MAX_STAR_WIDTH), random.randint(MIN_STAR_LENGTH, MAX_STAR_LENGTH))) for i in range(MAX_STARS)]


if __name__ == '__main__' :
    try:
        configure_channels()
        GPIO.add_event_detect(SW, GPIO.FALLING, callback = button_callback, bouncetime = 10)
        pygame.init()
        clock = pygame.time.Clock()
        last_state = (GPIO.input(SIA), GPIO.input(SIB))

        while game_running:
            screen.fill((0, 0, 0))

            for star in stars:
                pygame.draw.rect(screen, (255, 255, 255), star)
                if star.y >= SCREEN_WIDTH:
                    star.move_ip(0, -745)
                else:
                    star.move_ip(0, 1)

            screen.blit(player.image, player.rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False

            current_state = (GPIO.input(SIA), GPIO.input(SIB))
            if current_state != last_state:  # Detect state change
                if last_state == (0, 0) and current_state == (0, 1):
                    print("asdfasdf")
                    player.move(45, 0)

                elif last_state == (0, 0) and current_state == (1, 0):
                    player.move(-45, 0)
                    print("öööö")

            # Update the last state
            last_state = current_state

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    except:
        pass
    finally:
        print("BYE BYE ^_^")