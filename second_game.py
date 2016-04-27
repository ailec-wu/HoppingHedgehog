# Kevin Brown (kgb6fu) and Ailec Wu (aw5fa)
import sys
sys.path.insert(0, './ProjectDependencies')

import pygame
import gamebox
import random

# megalovania = gamebox.load_sound("Undertale OST - Megalovania Extended.wav")
# megalovaniaplayer0 = megalovania.play()

# Camera Window
camera = gamebox.Camera(800,600)

# Player Sprites
p1 = gamebox.from_color(200, 50, "brown", 25, 25)

background = gamebox.from_color(400, 600, "light green", 800, 100)
ceiling = gamebox.from_color(400, -500, "white", 800, 1000)

# Global Values
p1_score = 0
p1_health = 10

game_start = False
pause = False

p1.yspeed = 0

# Platforms
platforms = []

i = 0

scroll_speed = 3

yellow_coins = []

mirrored_platforms = []

def platform_creator():
    global i, platforms, mirrored_platforms, scroll_speed
    height_position = random.randint(400, 500)
    platform_length = (600 - height_position)*2
    mirror_position = height_position - 350
    new_platform = gamebox.from_color(800, height_position, "green", 50, platform_length)
    mirror_platform = gamebox.from_color(800, mirror_position, "green", 50, mirror_position*2)
    if i < 120:
        i += 1
    if i == 120:
        platforms.append(new_platform)
        mirrored_platforms.append(mirror_platform)
        i = 0
    for platform in platforms:
        platform.x -= scroll_speed
        if platform.x < -50:
            platforms.remove(platform)
    for mirror in mirrored_platforms:
        mirror.x -= scroll_speed
        if mirror.x < -50:
            mirrored_platforms.remove(mirror)

def y_coins():
    global p1_score, mirrored_platforms, yellow_coins

    for mirror in mirrored_platforms:
            mirror_position = mirror.y
            yellow_coin = gamebox.from_color(mirror.x, (mirror_position*2) + 50, "yellow", 10, 10)
            yellow_coins.append(yellow_coin)

    for yellow_coin in yellow_coins:
        yellow_coin.x -= scroll_speed
        if p1.touches(yellow_coin):
            yellow_coins.remove(yellow_coin)
            p1_score += 1
            music0 = gamebox.load_sound("hit_sound.wav")
            musicplayer0 = music0.play()
        if yellow_coin.x < -50:
            yellow_coins.remove(yellow_coin)



def tick(keys):
    # Game Beginning Screen and Starting the Game
    global game_start, pause, p1_score, yellow_coins, y_c, platforms, mirrored_platforms, p1_health
    if game_start == False:
        camera.clear("light blue")
        camera.draw(gamebox.from_text(400, 300, str("PRESS SPACE BAR TO START!"), "Arial", 50, "white", True))
        camera.display()
        if pygame.K_SPACE in keys:
            game_start = True
    if game_start == True:
    # Player 1 Collisions with objects
        p1.yspeed += 1
        p1.y = p1.y + p1.yspeed
        if pygame.K_UP in keys:
            p1.yspeed -= 5
            music_jump1 = gamebox.load_sound("Jump.wav")
            musicplayer3 = music_jump1.play()
        for platform in platforms:
            if p1.touches(platform):
                p1.move_to_stop_overlapping(platform)
                p1_health -= 1
                p1.x += 65
        if p1.x > 200:
            p1.x -= scroll_speed
        if p1.touches(background):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(background)
            if pygame.K_UP in keys:
                p1.yspeed -= 5
        if p1.touches(ceiling):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(ceiling)
    # Platform Creation and Removal
        platform_creator()
    # Coin Creation and Removal
        y_coins()


    # Visuals
        if pause == False:
            camera.clear("light blue")
            camera.draw(background)
            camera.draw(gamebox.from_text(50, 50, str(p1_score), "Arial", 30, "brown", True))
            camera.draw(gamebox.from_text(400, 50, str(p1_health), "Arial", 30, "red", True))
            camera.draw(p1)
            for yellow_coin in yellow_coins:
                camera.draw(yellow_coin)
            for platform in platforms:
                camera.draw(platform)
            for mirror in mirrored_platforms:
                camera.draw(mirror)
            camera.display()

    # Game Ending and Restarting
        if p1_health == 0 and pause == False:
            camera.clear("light blue")
            camera.draw(gamebox.from_text(400, 200, str("GAME OVER"), "Arial", 100, "gray", True))
            camera.draw(gamebox.from_text(400, 300, str("Score: " + str(p1_score)), "Arial", 50, "brown"))
            camera.draw(gamebox.from_text(400, 370, str("Play again?"), "Arial", 50, "gray"))
            camera.draw(gamebox.from_text(400, 410, str("(press the space bar)"), "Arial", 20, "gray"))
            camera.display()
            pause = True                # Freeze the Game Over menu

        if pygame.K_SPACE in keys and pause == True:
            platforms = []
            mirrored_platforms = []
            yellow_coins = []
            p1_health = 10
            p1.y = 50
            p1_score = 0
            game_start = False      # Restart the game
            pause = False           # Unfreeze the game


ticks_per_second = 30

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)