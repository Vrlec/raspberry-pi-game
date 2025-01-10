#!/usr/bin/env python
import pygame
import RPi.GPIO as GPIO
from time import sleep

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
        self.rect.x += dx
        self.rect.y += dy

player = Player(250, 500)


enemies = (
    pygame.Rect((150, 100, 50, 50)),
    pygame.Rect((50, 50, 50, 50)),
    pygame.Rect((25, 300, 50, 50)),
)

if __name__ == '__main__' :
    try:
        configure_channels()
        GPIO.add_event_detect(SW, GPIO.FALLING, callback = button_callback, bouncetime = 10)
        pygame.init()
        last_state = (GPIO.input(SIA), GPIO.input(SIB))

        while game_running:
            screen.fill((0, 0, 0))
            screen.blit(player.image, player.rect)

            for enemy in enemies:
                pygame.draw.rect(screen, (255, 0, 0), enemy)
                if enemy.y >= SCREEN_WIDTH:
                    enemy.move_ip(0, -600)
                else:
                    enemy.move_ip(0, 1)

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
            sleep(0.001)  # Debounce delay

        pygame.quit()

    except:
        pass
    finally:
        print("BYE BYE ^_^")