import pygame

pygame.init() #초기화ㅓ
# 화면 크기 설정
screen_width = 1200 # 가로크기
screen_height = 800 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("KKLHY") # 게임 이름

# FPS
clock =pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("image/background.png")

# 캐릭터(스프라이트) 불러오기
character = pygame.image.load("image/character.png") # 121 / 113
character_size = character.get_rect().size # 캐릭터 가로,세로 크기 불러오기
character_width =character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = 0 # 화면 가로의 캐릭터 위치설정
character_y_pos = -80 + screen_height/2  # 화면 세로의 캐릭터 위치 설정

#이동할 좌표
to_x = 0
to_y = 0

#아이템 좌표
item_to_x= 0

#이동 속도
character_speed = 1

# 아이템 추가
item = pygame.image.load("image/item.png")
item_size = character.get_rect().size # 캐릭터 가로,세로 크기 불러오기
item_width =character_size[0] # 캐릭터의 가로 크기
item_height = character_size[1] # 캐릭터의 세로 크기
item_x_pos = 1200 - item_width/2 # 화면 가로의 캐릭터 위치설정
item_y_pos = screen_height/2 - item_height # 화면 세로의 캐릭터 위치 설정

#폰트 정의
game_font =pygame.font.Font(None, 40) # 폰트 객체  생성(폰트,크기)

# 총 시간
total_time = 100

# 시작 시간정보
start_ticks =pygame.time.get_ticks() # 시작 tick 을 받아옴


# 이벤트 루프
running = True # 게임이 진행중인가?
started = False # if 실행 제어조건
while running:
  dt =clock.tick(60) # 게임화면의 초당 프레임 수를 설정


  for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
    if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
      running = False # 게임이 진행중이 아님

    if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
      if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
        to_x -= character_speed # to_x = to_x - 5
      elif event.key == pygame.K_RIGHT: #캐릭터를 오른쪽으로
        to_x += character_speed
      elif event.key == pygame.K_UP: #캐릭터를 위로
        to_y -= character_speed
      elif event.key == pygame.K_DOWN: #캐릭터를 아래로
        to_y += character_speed

    if started == False and event.type == pygame.KEYDOWN:  #날라오는 시간 수정가능 할 때 하기
      if pygame.time.get_ticks() > 2000:
        item_to_x -= 10
        started = True


    if event.type == pygame.KEYUP: #방향키를 떼면 멈춤
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        to_x = 0
      elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        to_y = 0

  character_x_pos += to_x * dt
  character_y_pos += to_y * dt
  item_x_pos += item_to_x

  #캐릭터 화면 탈출 방지
  #가로 경계값 처리
  if character_x_pos <= 0: # = 추가
    character_x_pos = 0
  elif character_x_pos >= screen_width - character_width:
    character_x_pos =screen_width - character_width

  #세로 경계값처리
  if character_y_pos <= 0:
    character_y_pos = 0
  elif character_y_pos >= screen_height -character_height:
    character_y_pos = screen_height - character_height



  screen.blit(background,(0,0)) #배경 그리기
  screen.blit(character,(character_x_pos,character_y_pos)) # 캐릭터 그리기
  screen.blit(item, (item_x_pos, item_y_pos))  # 아이템 그리기

  # 타이머 집어 넣기
  # 경과 시간 계산
  elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
  # 시간단위가 ms 라서 1000으로 나누어 s 단위로 표시

  # 출력 할 글자 색상
  timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
  screen.blit(timer, (10, 10))

# 만약 시간이 0 이하이면 게임 종료
  if total_time - elapsed_time <= 0:
    running = False

  pygame.display.update() # 게임화면을 다시 그리기!

# 잠시 대기
pygame.time.delay(2000)

# pygame 종료!
pygame.quit()