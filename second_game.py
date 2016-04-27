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

up_last_pressed = False
was_touching = False

def platform_creator():
    global i, scroll_speed, platforms, yellow_coins
    height_position = random.randint(400, 500)
    platform_length = (600 - height_position)*2
    mirror_position = height_position - 350
    new_platform = gamebox.from_color(800, height_position, "green", 50, platform_length)
    mirror_platform = gamebox.from_color(800, mirror_position, "green", 50, mirror_position*2)
    if i < 120:
        i += 1
    if i == 120:
        platforms.append(new_platform)
        platforms.append(mirror_platform)
        i = 0
    for platform in platforms:
        platform.x -= scroll_speed
        if platform.x < -50:
            platforms.remove(platform)



def y_coins():
    global p1_score, platforms, yellow_coins
    for platform in platforms[1::2]:
        if platform.x == 700:
            yellow_coin = gamebox.from_color(800, random.randint(150,450), "yellow", 10, 10)
            if yellow_coin not in yellow_coins:
                yellow_coins.append(yellow_coin)
            if yellow_coin.touches(platform):
                yellow_coin.move_to_stop_overlapping(platform)
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
    global game_start, pause, p1_score, yellow_coins, y_c, platforms, p1_health, up_last_pressed, was_touching

    if game_start == False:
        camera.clear("light blue")
        camera.draw(gamebox.from_text(400, 300, str("PRESS SPACE BAR TO START!"), "Arial", 50, "white", True))
        camera.display()
        if pygame.K_SPACE in keys:
            game_start = True
    if game_start == True:
    # Player 1 Collisions with objects
        p1.yspeed += 0.5
        p1.y = p1.y + p1.yspeed
        if pygame.K_UP in keys and not up_last_pressed:
            p1.yspeed = -8
            music_jump1 = gamebox.load_sound("Jump.wav")
            musicplayer3 = music_jump1.play()
            up_last_pressed = True
        if not pygame.K_UP in keys:
            up_last_pressed = False

        nothing_touched = True  # check if nothing is touched
        for platform in platforms:
            if p1.touches(platform):
                if not was_touching:
                    p1_health -= 1
                p1.x += 65
                was_touching = True
                nothing_touched = False
        if nothing_touched:
            was_touching = False

        if p1.x > 200:
            p1.x -= scroll_speed
        if p1.touches(background):
            was_touching = True
            p1.yspeed = 0
            p1.y -= 100
            p1_health -= 1
            if pygame.K_UP in keys:
                p1.yspeed -= 5
        if p1.touches(ceiling):
            p1.yspeed = 0
            p1.move_to_stop_overlapping(ceiling)
    # Platform Creation and Removal
        platform_creator()
    # Coin Creation and Removal
        y_coins()
    # Score
        for platform in platforms:
            if platform.x == 200:
                p1_score += 0.5

    # Visuals
        if pause == False:
            camera.clear("light blue")
            camera.draw(background)
            camera.draw(gamebox.from_text(50, 50, str(int(p1_score)), "Arial", 30, "brown", True))
            camera.draw(gamebox.from_text(400, 50, str(p1_health), "Arial", 30, "red", True))
            camera.draw(p1)
            for yellow_coin in yellow_coins:
                camera.draw(yellow_coin)
            for platform in platforms:
                camera.draw(platform)
            camera.display()

    # Game Ending and Restarting
        if p1_health == 0 and pause == False:
            camera.clear("light blue")
            camera.draw(gamebox.from_text(400, 200, str("GAME OVER"), "Arial", 100, "gray", True))
            camera.draw(gamebox.from_text(400, 300, str("Score: " + str(int(p1_score))), "Arial", 50, "brown"))
            camera.draw(gamebox.from_text(400, 370, str("Play again?"), "Arial", 50, "gray"))
            camera.draw(gamebox.from_text(400, 410, str("(press the space bar)"), "Arial", 20, "gray"))
            camera.display()
            pause = True                # Freeze the Game Over menu

        if pygame.K_SPACE in keys and pause == True:
            platforms = []
            yellow_coins = []
            p1_health = 10
            p1.y = 50
            p1_score = 0
            game_start = False      # Restart the game
            pause = False           # Unfreeze the game
    #print(was_touching)
    print(len(yellow_coins))
    #print(str(len(platforms))+" platforms")

ticks_per_second = 60

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)