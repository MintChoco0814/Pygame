import random
import pygame
import time


WHITE = (255,255,255)
WindowWidth = 480 # Window의 가로길이
WindowHeight = 640 # Window의 세로길이
# 객체를 드로잉
def drawObject(obj,x,y):
    global Window
    Window.blit(obj,(x,y))
def drawScore(Score):
    global Window
    font = pygame.font.SysFont("impact",20 ,0 ,0)
    text = font.render("SCORE : " + str(Score), True, (255,255,255))
    Window.blit(text,(10,0))
def initGame():
    global Window, clock, background, player, bullet, bullet_Sound, explosion,icon
    pygame.init() # 파이게임 초기화
    Window = pygame.display.set_mode((WindowWidth, WindowHeight))
    background = pygame.image.load("Ocean.png") # 배경 그림
    player = pygame.image.load("Plane.png") # 비행기 그림
    bullet = pygame.image.load('bullet.png') # 총알 사진
    bullet = pygame.transform.scale(bullet,[10,20]) # 사진 크기 조정
    bullet_Sound = pygame.mixer.Sound("bulletSound.wav") # 총알 사운드
    explosion = pygame.image.load('Explosion.png') # 폭발 사진
    explosion = pygame.transform.scale(explosion, [40,40]) # 크기 조정
    pygame.display.set_caption("Shooting Game") # 타이틀 이름
    icon = pygame.image.load('Jet_Icon.png') # 아이콘 그림
    pygame.display.set_icon(icon) # 아이콘 지정
    clock = pygame.time.Clock() # FPS


def runGame():
    global Window, clock, background, player, bullet, enemy, bullet_Sound, explosion
    # 비행기 크기
    player = pygame.transform.scale(player,[40,40])
    playerSize = player.get_rect().size
    playerWidth = playerSize[0]
    playerHeight = playerSize[1]
    # 비행기 위치
    player_x_pos = (WindowWidth / 2) - (playerWidth / 2)
    player_y_pos = WindowHeight - playerHeight
    player_x = 0
    player_y = 0
    playerSpeed = 5

    # 총알
    bullets = []

    # 적
    enemy = pygame.image.load("Enemy.png")
    enemy = pygame.transform.scale(enemy, [40, 40])
    enemySize = enemy.get_rect().size  # 적 크기
    enemyWidth = enemySize[0]
    enemyHeight = enemySize[1]
    enemyX = random.randrange(0, WindowWidth-enemyWidth)
    enemyY = 0
    enemySpeed = 2
    enemySound = pygame.mixer.Sound("enemydestroy.wav")
    # 충돌
    isShot = False
    Score = 0

    play = True
    while play:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                play = False
            # 키 입력
            if event.type in [pygame.KEYDOWN]: #키가 눌렸을때
                if event.key == pygame.K_LEFT: # 왼쪽
                    player_x -= playerSpeed
                elif event.key == pygame.K_RIGHT: # 오른쪽
                    player_x += playerSpeed
                elif event.key == pygame.K_UP: # 위
                    player_y -= playerSpeed
                elif event.key == pygame.K_DOWN: # 아래
                    player_y += playerSpeed
                elif event.key == pygame.K_SPACE: # 스페이스
                    bullet_Sound.play()
                    bulletX = player_x_pos + playerWidth/2
                    bulletY = player_y_pos - playerHeight
                    bullets.append([bulletX,bulletY])
                    
            if event.type in [pygame.KEYUP]: # 키가 때졌을떄
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_y = 0
        # 캐릭터 위치
        player_x_pos += player_x
        player_y_pos += player_y
        if player_x_pos < 0:
            player_x_pos = 0
        elif player_x_pos > WindowWidth - playerWidth:
            player_x_pos = WindowWidth - playerWidth
        if player_y_pos < 0:
            player_y_pos = 0
        elif player_y_pos > WindowHeight - playerHeight:
            player_y_pos = WindowHeight - playerHeight

        Window.fill(WHITE)
        # 객체 그리기
        drawObject(background, 0,0) # 배경화면
        drawObject(player, player_x_pos, player_y_pos)
        # 총알 그리기
        if len(bullets) != 0:
            for i, bxy in enumerate(bullets):
                bxy[1] -= 10
                bullets[i][1] = bxy[1]
                # 총알에 적 비행기가 맞았다면
                if bxy[1] < enemyY:
                    if bxy[0] > enemyX and bxy[0] < enemyX + enemyWidth:
                        bullets.remove(bxy)
                        isShot = True
                        Score += 100
            if bxy[1] <= 0: # 미사일이 화면 밖에 닿으면
                try:
                    bullets.remove(bxy) # 미사일제거
                except:
                    pass
        if len(bullets) != 0:
            for bx, by in bullets:
                drawObject(bullet, bx, by)
        # 적 그리기
        # 점수
        drawScore(Score)
        enemyY += enemySpeed # 적이 아래로 떨어짐
        if enemyY > WindowHeight:
            # 새로운 적
            enemy = pygame.image.load("Enemy.png")
            enemy = pygame.transform.scale(enemy, [40, 40])
            enemySize = enemy.get_rect().size  # 적 크기
            enemyWidth = enemySize[0]
            enemyHeight = enemySize[1]
            enemyX = random.randrange(0, WindowWidth - enemyWidth)
            enemyY = 0
        drawObject(enemy, enemyX, enemyY)
        # 충돌
        if isShot:
            drawObject(explosion, enemyX, enemyY)
            enemySound.play()
            # 새로운 적 생성
            enemy = pygame.image.load("Enemy.png")
            enemy = pygame.transform.scale(enemy, [40, 40])

            enemySize = enemy.get_rect().size  # 적 크기
            enemyWidth = enemySize[0]
            enemyHeight = enemySize[1]
            enemyX = random.randrange(0, WindowWidth - enemyWidth)
            enemyY = 0
            isShot = False
        drawObject(enemy, enemyX, enemyY)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

initGame()
runGame()
