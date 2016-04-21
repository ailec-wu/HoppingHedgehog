# Kevin Brown (kgb6fu) and Ailec Wu (aw5fa)

import pygame
import gamebox
import random

# megalovania = gamebox.load_sound("Undertale OST - Megalovania Extended.wav")
# megalovaniaplayer0 = megalovania.play()

# Camera Window
camera = gamebox.Camera(800,600)

# Player Sprites
p1 = gamebox.from_color(750, 50, "purple", 25, 25)

# Global Values
p1_score = 0


game_start = False
pause = False

p1.yspeed = 0

# Platforms
platforms = [gamebox.from_color(-100, 1090, "green", 3000, 1000), gamebox.from_color(50, 220, "gray", 100, 15),
             gamebox.from_color(625, 120, "gray", 100, 15), gamebox.from_color(50, 450, "gray", 100, 15),
             gamebox.from_color(750, 220, "gray", 100, 15), gamebox.from_color(750, 450, "gray", 100, 15),
             gamebox.from_color(400, 450, "gray", 300, 15), gamebox.from_color(400, 220, "gray", 300, 15),
             gamebox.from_color(175, 120, "gray", 100, 15), gamebox.from_color(175, 350, "gray", 100, 15),
             gamebox.from_color(625, 350, "gray", 100, 15), gamebox.from_color(-100, -490, "green", 3000, 1000),
             gamebox.from_color(-490, -100, "green", 1000, 3000), gamebox.from_color(1290, -100, "green", 1000, 3000)]


def y_coins():
    global y_c, p1_score, p2_score
    if y_c < 30:
        y_c += 1
    elif y_c >= 30:
        y_c = 0
        for platform in platforms:
            yellow_coin = gamebox.from_color(platform.x, platform.y, "yellow", 10, 10)
            yellow_coins.append(yellow_coin)

    for yellow_coin in yellow_coins:
        for platform in platforms:
            if yellow_coin.touches(platform):
                yellow_coin.move_to_stop_overlapping(platform)
        if p1.touches(yellow_coin):
            yellow_coins.remove(yellow_coin)
            p1_score += 1
            music0 = gamebox.load_sound("hitsound.wav")
            musicplayer0 = music0.play()



def tick(keys):
    # Game Beginning Screen and Starting the Game
    global game_start, pause, p1_score, p2_score, yellow_coins, red_coins, blue_coins, y_c, r_c, b_c
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
            p1.y -= 5
            music_jump1 = gamebox.load_sound("SFX_Jump_31.wav")
            musicplayer3 = music_jump1.play()
        for platform in platforms:
            if p1.touches(platform):
                p1.move_to_stop_overlapping(platform)
                # Health - 1 part


    # Coin Creation and Removal
    #     y_coins()


    # Visuals
        if pause == False:
            camera.clear("black")
            camera.draw(gamebox.from_text(750, 50, str(p1_score), "Arial", 30, "purple", True))
            camera.draw(p1)
            for yellow_coin in yellow_coins:
                camera.draw(yellow_coin)
            for platform in platforms:
                camera.draw(platform)
            camera.display()

    # Game Ending and Restarting
        if p1_score >= 50 and pause == False:
            camera.clear("black")
            camera.draw(gamebox.from_text(400, 200, str("GAME OVER"), "Arial", 100, "gray", True))
            camera.draw(gamebox.from_text(400, 300, str("Player 1 wins!"), "Arial", 50, "purple"))
            camera.draw(gamebox.from_text(400, 370, str("Try again?"), "Arial", 50, "gray"))
            camera.draw(gamebox.from_text(400, 410, str("(press the space bar)"), "Arial", 20, "gray"))
            camera.display()
            pause = True                # Freeze the Game Over menu

        if pygame.K_SPACE in keys and pause == True:
            game_start = False      # Restart the game
            pause = False           # Unfreeze the game


ticks_per_second = 30

# keep this line the last one in your program
gamebox.timer_loop(ticks_per_second, tick)
