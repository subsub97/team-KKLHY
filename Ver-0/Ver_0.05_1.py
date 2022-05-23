import pygame
import random

pygame.init()

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("KKLHY_stage2")

clock = pygame.time.Clock()

score = 0
total_time = 100
start_ticks = pygame.time.get_ticks()

game_font = pygame.font.Font(None, 40)
background = pygame.image.load("0_image/Yang/background.png")

character = pygame.image.load("0_image/Yang/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = (screen_height / 2) - (character_height / 2)

character_speed = 0.4

character_to_x = 0
character_to_y = 0

enemy_list = list()   # 적 생성할 때마다 enemy_class 객체 하나씩 담기
# 적이 맵 밖으로 나갔을 경우 해당 객체 리스트에서 삭제


class enemy_class:
    enemy_image = pygame.image.load("0_image/HO/item.png")
    enemy_size = enemy_image.get_rect().size
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_x_pos = 0
    enemy_y_pos = 0

    enemy_rect = enemy_image.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    def __init__(self):
        self.enemy_speed = random.choice(
            [0.5, 1.0, 1.3, 1.5, 2.0, 2.5, 3.0])   # 적 스피드 랜덤
        self.enemy_spawnPoint = random.choice(
            ['UP', 'DOWN', 'LEFT', 'RIGHT'])    # 적 스폰지점 랜덤

        # 스폰지점 설정
        if self.enemy_spawnPoint == 'LEFT':
            self.enemy_x_pos = -self.enemy_width
            self.enemy_y_pos = random.randint(
                0, screen_height - self.enemy_height)
            self.enemy_dx = random.randint(-3, 3)
            self.enemy_dy = random.randint(-3, 3)
        elif self.enemy_spawnPoint == 'RIGHT':
            self.enemy_x_pos = screen_width
            self.enemy_y_pos = random.randint(
                0, screen_height - self.enemy_height)
            self.enemy_dx = random.randint(-3, 3)
            self.enemy_dy = random.randint(-3, 3)
        elif self.enemy_spawnPoint == 'UP':
            self.enemy_x_pos = random.randint(
                0, screen_width - self.enemy_width)
            self.enemy_y_pos = -self.enemy_height
            self.enemy_dx = random.randint(-3, 3)
            self.enemy_dy = random.randint(-3, 3)
        elif self.enemy_spawnPoint == 'DOWN':
            self.enemy_x_pos = random.randint(
                0, screen_width - self.enemy_width)
            self.enemy_y_pos = screen_height
            self.enemy_dx = random.randint(-3, 3)
            self.enemy_dy = random.randint(-3, 3)

    def enemy_move(self):   # 매 프레임마다 적 각도에 따라 enemy 객체의 xy 좌표를 이동시킴
        self.enemy_x_pos += self.enemy_dx
        self.enemy_y_pos += self.enemy_dy
        global score

        def boundary_UP():    # 화면 넘어갔는지 확인
            if self.enemy_y_pos < -self.enemy_height:
                return True

        def boundary_DOWN():
            if self.enemy_y_pos > screen_height:
                return True

        def boundary_LEFT():
            if self.enemy_x_pos < -self.enemy_width:
                return True

        def boundary_RIGHT():
            if self.enemy_x_pos > screen_width:
                return True

        if self.enemy_spawnPoint == 'UP':
            if boundary_LEFT() or boundary_RIGHT() or boundary_DOWN():    # 화면 넘어갔다면 객체 지우고 점수+1
                enemy_list.remove(self)
                score += 1

        if self.enemy_spawnPoint == 'DOWN':
            if boundary_LEFT() or boundary_RIGHT() or boundary_UP():
                enemy_list.remove(self)
                score += 1

        if self.enemy_spawnPoint == 'LEFT':
            if boundary_UP() or boundary_DOWN() or boundary_RIGHT():
                enemy_list.remove(self)
                score += 1

        if self.enemy_spawnPoint == 'RIGHT':
            if boundary_UP() or boundary_DOWN() or boundary_LEFT():
                enemy_list.remove(self)
                score += 1

    def enemy_coll(self):   # 충돌판정을 위해 enemy_rect 최신화
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.left = self.enemy_x_pos
        self.enemy_rect.top = self.enemy_y_pos


game_result = "Game Over"

running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            if event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            if event.key == pygame.K_UP:
                character_to_y -= character_speed
            if event.key == pygame.K_DOWN:
                character_to_y += character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                character_to_y = 0

    character_x_pos += character_to_x * dt
    character_y_pos += character_to_y * dt

    # 캐릭터 경계값 설정
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(
        int(total_time - elapsed_time)), True, (255, 255, 255))

    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    # 적 생성
    if elapsed_time < total_time:
        if len(enemy_list) <= 80:
            enemy_list.append(enemy_class())

    # 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for i in enemy_list:
        i.enemy_coll()
        if character_rect.colliderect(i.enemy_rect):
            print("충돌")
            print("점수 : ", score)
            running = False

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for i in enemy_list:
        i.enemy_move()
        screen.blit(i.enemy_image, (i.enemy_x_pos, i.enemy_y_pos))

    total_score = game_font.render(
        "Score : {}".format(int(score)), True, (255, 255, 255))
    screen.blit(total_score, (screen_width - 150, 10))

    screen.blit(timer, (10, 10))

    pygame.display.update()

pygame.time.delay(2000)

pygame.quit()
