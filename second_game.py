# Kevin Brown (kgb6fu) and Ailec Wu (aw5fa)
import sys
sys.path.insert(0, './ProjectDependencies')

import pygame
import gamebox
import random

# http://wallpaper.zone/img/16093.png
# megalovania = gamebox.load_sound("Undertale OST - Megalovania Extended.wav")
# megalovaniaplayer0 = megalovania.play()

# Camera Window
camera = gamebox.Camera(800,600)

# Player Sprites
p1 = gamebox.from_color(200, 50, "brown", 25, 25)

background = gamebox.from_color(400, 600, "light green", 800, 100)
ceiling = gamebox.from_color(400, -500, "white", 800, 1000)
black_bar = gamebox.from_color(600, 50, "black", 255, 30)

# Global Values
p1_score = 0
p1_health = 10

game_start = False
pause = False

p1.yspeed = 0

# Platforms
platforms = []

plat_count = 0

scroll_speed = 3

yellow_coins = []

bar = []

tick_count = 0
tick_count_2 = 0

up_last_pressed = False
was_touching = False

def platform_creator():
    global plat_count, scroll_speed, platforms
    height_position = random.randint(400, 500)
    platform_length = (600 - height_position)*2
    mirror_position = height_position - 350
    new_platform = gamebox.from_color(800, height_position, "green", 50, platform_length)
    mirror_platform = gamebox.from_color(800, mirror_position, "green", 50, mirror_position*2)
    if plat_count < 120:
        plat_count += 1
    if plat_count == 120:
        platforms.append(new_platform)
        platforms.append(mirror_platform)
        plat_count = 0
    for platform in platforms:
        platform.x -= scroll_speed
        if platform.x < -50:
            platforms.remove(platform)



def y_coins():
    global p1_score, platforms, yellow_coins, scroll_speed, p1_health, tick_count, tick_count_2
    # dict = {0: 1, 1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6, 12: 7, 13: 7, 14: 8, 15: 8, 16: 1,
    #         17: 1, 18: 2, 19: 2, 20: 3, 21: 3, 22: 4, 23: 4, 24: 5, 25: 5, 26: 6, 27: 6, 28: 7, 29: 7, 30: 8, 31: 8,
    #         32: 1, 33: 1, 34: 2, 35: 2, 36: 3, 37: 3, 38: 4, 39: 4, 40: 5, 41: 5, 42: 6, 43: 6, 44: 7, 45: 7, 46: 8,
    #         47: 8, 48: 1, 49: 1, 50: 2, 51: 2, 52: 3, 53: 3, 54: 4, 55: 4, 56: 5, 57: 5, 58: 6, 59: 6, 60: 7, 61: 7,
    #         62: 8, 63: 8}
    for platform in platforms[1::2]:
        if 600 <= platform.x < 600 + scroll_speed:
            coin_height = random.randint(150, 450)
            yellow_coin = gamebox.from_image(800, coin_height, "coin_1.png")
            # yellow_coin = gamebox.from_color(800, coin_height, "yellow", 10, 10)
            # if yellow_coin not in yellow_coins:
            yellow_coins.append(yellow_coin)
            if yellow_coin.touches(platform):
                yellow_coin.move_to_stop_overlapping(platform)
    for yellow_coin in yellow_coins:
        yellow_coin.image = "coin_"+str(tick_count_2+1)+".png"

        #yellow_coin.image = "coin_" + str(tick_count + 1) + ".png"
        yellow_coin.x -= scroll_speed
        if p1.touches(yellow_coin):
            yellow_coins.remove(yellow_coin)
            p1_score += 1
            music0 = gamebox.load_sound("hit_sound.wav")
            musicplayer0 = music0.play()
        if yellow_coin.x < -50:
            yellow_coins.remove(yellow_coin)

        tick_count = (tick_count+1)%128
        tick_count_2 = tick_count//16
        #print(tick_count_2)


def tick(keys):
    # Game Beginning Screen and Starting the Game
    global game_start, pause, p1_score, yellow_coins, y_c, platforms, p1_health, up_last_pressed, was_touching, bar

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
    # Health
        if p1_health > 10:
            p1_health = 10
        bar = [gamebox.from_color(1000 - (512-chunknum*25), 50, "red", 20, 20) for chunknum in range(p1_health)]
    # Score
        for platform in platforms:
            if platform.x == 200:
                p1_score += 0.5

    # Visuals
        if pause == False:
            camera.clear("light blue")
            camera.draw(background)
            camera.draw(gamebox.from_text(50, 50, str(int(p1_score)), "Arial", 30, "brown", True))
            # camera.draw(gamebox.from_text(400, 50, str(p1_health), "Arial", 30, "red", True))
            camera.draw(black_bar)
            for chunk in bar:
                camera.draw(chunk)
            for yellow_coin in yellow_coins:
                camera.draw(yellow_coin)
            camera.draw(p1)
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
    #print(len(yellow_coins))
    #print(str(len(platforms))+" platforms")

ticks_per_second = 60

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)