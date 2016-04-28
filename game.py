# Kevin Brown (kgb6fu) and Ailec Wu (aw5fa)
import sys
sys.path.insert(0, './ProjectDependencies')

import pygame
import gamebox
import random

# http://wallpaper.zone/img/16093.png
# http://www.appsrox.com/screenshots/flappychick/Flappy_Pipe.png
# megalovania = gamebox.load_sound("Undertale OST - Megalovania Extended.wav")
# megalovaniaplayer0 = megalovania.play()
# http://us.123rf.com/450wm/anastasiaromb/anastasiaromb1603/anastasiaromb160300021/53104705-cute-set-of-forest-wild-animals-nature-fauna-collection.jpg?ver=6
# Camera Window
camera = gamebox.Camera(800,600)

# Player Sprites
p1 = gamebox.from_image(200, 50, "hedgehog.png")

background1 = gamebox.from_image(800, 300, "background.png")
background2 = gamebox.from_image(2400, 300, "background.png")
ground = gamebox.from_color(400, 600, "light green", 800, 100)
ceiling = gamebox.from_color(400, -500, "white", 800, 1000)
black_bar = gamebox.from_color(500, 50, "black", 255, 30)

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

time = 0

def platform_creator():
    global plat_count, scroll_speed, platforms
    height_position = random.randint(400, 700)
    mirror_position = height_position - 500
    new_platform = gamebox.from_image(800, height_position, "pipe_b.png")
    mirror_platform = gamebox.from_image(800, mirror_position, "pipe_u.png")
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
    for platform in platforms[::2]:
        if 200 <= platform.x < 200 + scroll_speed:
            platform.x -= scroll_speed



def y_coins():
    global p1_score, platforms, yellow_coins, scroll_speed, p1_health, tick_count, tick_count_2
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
    global game_start, pause, p1_score, yellow_coins, y_c, platforms, p1_health, up_last_pressed, was_touching, bar, background1, time

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
        if p1.touches(ground):
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
        bar = [gamebox.from_color(900 - (512-chunknum*25), 50, "red", 20, 20) for chunknum in range(p1_health)]
    # Score
        for platform in platforms[1::2]:
            if 200 <= platform.x < 200 + scroll_speed:
                p1_score += 1
    # Background
        background1.x -= scroll_speed
        if background1.x <= -(800 - scroll_speed):
            background1.x = 2400
        background2.x -= scroll_speed
        if background2.x <= -(800 - scroll_speed):
            background2.x = 2400
        time += 1

    # Visuals
        if pause == False:
            camera.clear("light blue")
            camera.draw(ground)
            camera.draw(background1)
            camera.draw(background2)
            camera.draw(gamebox.from_text(50, 50, str(int(p1_score)), "Arial", 30, "brown", True))
            camera.draw(gamebox.from_text(750, 50, str(time//ticks_per_second), "Arial", 30, "black", True))
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
            camera.draw(gamebox.from_text(400, 200, str("GAME OVER"), "Arial", 100, "black", True))
            camera.draw(gamebox.from_text(400, 300, str("Score: " + str(int(p1_score))), "Arial", 50, "brown"))
            camera.draw(gamebox.from_text(400, 350, str("You lasted: " + str(time//ticks_per_second) + " seconds"), "Arial", 50, "black"))
            camera.draw(gamebox.from_text(400, 400, str("Play again?"), "Arial", 50, "black"))
            camera.draw(gamebox.from_text(400, 440, str("(press the space bar)"), "Arial", 20, "black"))
            camera.display()
            pause = True                # Freeze the Game Over menu

        if pygame.K_SPACE in keys and pause == True:
            platforms = []
            yellow_coins = []
            p1_health = 10
            p1.y = 50
            p1_score = 0
            time = 0
            game_start = False      # Restart the game
            pause = False           # Unfreeze the game
    #print(was_touching)
    #print(len(yellow_coins))
    #print(str(len(platforms))+" platforms")


ticks_per_second = 60

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)
