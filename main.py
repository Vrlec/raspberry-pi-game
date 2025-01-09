#!/usr/bin/env python
import pygame
import RPi.GPIO as GPIO
import sys
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

def pygame_configure():
    pygame.init()

# =====================================================================
# Drawing fucntions
# =====================================================================
player = pygame.Rect((300, 250, 50, 50))

def draw_window():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), player)

# =====================================================================
# Controls functions
# =====================================================================
def button_callback():
    player.size(255, 255)
    print("Button pressed!")

def generate_callback():
    GPIO.add_event_detect(SW, GPIO.FALLING, callback = button_callback, bouncetime=10)

# =====================================================================
# Game loop
# =====================================================================
def game_loop():
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        current_state = (GPIO.input(SIA), GPIO.input(SIB))
        if current_state != last_state:  # Detect state change
            if last_state == (0, 0) and current_state == (0, 1):
                player.move_ip(45, 0)

            elif last_state == (0, 0) and current_state == (1, 0):
                player.move_ip(-45, 0)
        # Update the last state
        last_state = current_state

        pygame.display.flip()
        sleep(0.001)  # Debounce delay

    pygame.quit()

if __name__ == '__main__' :
    try:
        configure_channels()
        pygame.init()
        generate_callback()
        last_state = (GPIO.input(SIA), GPIO.input(SIB))
        game_loop()

    except:
        pass