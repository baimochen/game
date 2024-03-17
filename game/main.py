import pygame
import sys
import random
import time

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alien Invasion Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 5

enemy_size = 50
enemies = []

bullet_size = 5
bullet_speed = 7
bullet_cooldown = 0.5
last_shot_time = time.time()
bullets = []

score = 0
font = pygame.font.SysFont(None, 40)

player_img = pygame.image.load("my.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))

enemy_img = pygame.image.load("enemy16.png")
enemy_img = pygame.transform.scale(enemy_img, (enemy_size, enemy_size))

bg_img = pygame.image.load("bg.jpg")
bg_img = pygame.transform.scale(bg_img, (width, height))

game_active = True
restart_cooldown = 2
last_restart_time = 0

difficulty = 1
enemy_speeds = {1: 2, 2: 4, 3: 6}
enemy_spawn_rates = {1: 10, 2: 5, 3: 2}

# 新增变量：清空敌人技能使用次数
clear_enemies_skill_count = 3

def start_game():
    global player_x, player_y, player_speed, enemies, bullets, score, game_active, last_restart_time, clear_enemies_skill_count
    player_x = width // 2 - player_size // 2
    player_y = height - 2 * player_size
    player_speed = 5
    enemies = []
    bullets = []
    score = 0
    game_active = True
    last_restart_time = time.time()
    # 重置清空敌人技能使用次数
    clear_enemies_skill_count = 3

def show_difficulty_menu():
    global game_active, difficulty
    font = pygame.font.SysFont(None, 80)
    easy_text = font.render("1. Easy", True, white)
    medium_text = font.render("2. Medium", True, white)
    hard_text = font.render("3. Hard", True, white)

    screen.blit(easy_text, [width // 2 - 150, height // 2 - 100])
    screen.blit(medium_text, [width // 2 - 200, height // 2])
    screen.blit(hard_text, [width // 2 - 150, height // 2 + 100])

    pygame.display.flip()

    difficulty_selected = False
    while not difficulty_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 1
                    difficulty_selected = True
                elif event.key == pygame.K_2:
                    difficulty = 2
                    difficulty_selected = True
                elif event.key == pygame.K_3:
                    difficulty = 3
                    difficulty_selected = True
    pygame.event.clear()

# Display difficulty menu at the start
show_difficulty_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and clear_enemies_skill_count > 0:
                # 新增部分：按回车键清除所有敌人
                enemies = []
                clear_enemies_skill_count -= 1

    if not game_active:
        font = pygame.font.SysFont(None, 80)
        end_text = font.render("Game Over!", True, white)
        score_text = font.render("Score: " + str(score), True, white)
        play_again_text = font.render("Press R to play again", True, white)

        screen.blit(end_text, [width // 2 - 200, height // 2 - 100])
        screen.blit(score_text, [width // 2 - 150, height // 2])
        screen.blit(play_again_text, [width // 2 - 250, height // 2 + 100])

        current_time = time.time()
        if current_time - last_restart_time > restart_cooldown:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                start_game()
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < height - player_size:
            player_y += player_speed

        current_time = time.time()
        if keys[pygame.K_SPACE] and current_time - last_shot_time > bullet_cooldown:
            bullets.append([player_x + player_size // 2, player_y])
            last_shot_time = current_time

        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        if random.randint(1, 100) < enemy_spawn_rates[difficulty]:
            enemy_x = random.randint(0, width - enemy_size)
            enemy_y = 0
            enemies.append([enemy_x, enemy_y])

        for enemy in enemies:
            enemy[1] += enemy_speeds[difficulty]
            if enemy[1] > height:
                enemies.remove(enemy)
                score += 1

        # 修改部分：子弹和敌人碰撞检测
        for bullet in bullets.copy():
            bullet_rect = pygame.Rect(bullet[0] - bullet_size // 2, bullet[1] - bullet_size // 2, bullet_size, bullet_size)
            for enemy in enemies.copy():
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
            if player_rect.colliderect(enemy_rect):
                game_active = False

        screen.blit(bg_img, (0, 0))
        screen.blit(player_img, (player_x, player_y))

        for bullet in bullets:
            pygame.draw.circle(screen, red, bullet, bullet_size)

        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

        score_text = font.render("Score: " + str(score), True, white)
        screen.blit(score_text, [10, 10])

        # 显示清空敌人技能使用次数
        skill_count_text = font.render("Clear Enemies Skill: " + str(clear_enemies_skill_count), True, white)
        screen.blit(skill_count_text, [10, height - 40])

    pygame.display.flip()
    pygame.time.Clock().tick(60)
