import pygame
import time
import sys
import random
import os

pygame.init()

image_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\image")
sound_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\sound")
font_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\image\\font")

def speed():
    ball.count += 14
    ball.vel[1] = 0
    ball.vel[0] *= 5


def chang():
    ball.count += 14
    ball.vel[1] *= -1


def teleport():
    ball.count += 10
    ball.rect.y = random.randint(0, screen_height - ball.rect.height)
    ball.rect.x = random.randint(0, screen_width - ball.rect.width)


def slow():
    ball.count += 6
    ball.vel[1] *= 0.25
    ball.vel[0] *= 0.25
    ball.slow = True



def ilousion():
    ball.count += 1
    ball.vel[1] = random.choice([-ball.vel[1], ball.vel[1]])

    if ball.vel[1] >= 10:
        f_vel_y = -10
    else:
        f_vel_y = 10

    if ball.vel[0] >= 0:
        f_vel_x = 10
    else:
        f_vel_x = -10

    f_b = Fake_ball(ball.rect.x, ball.rect.y, [f_vel_x, f_vel_y])
    fake_ball_group.add(f_b)

    if ball.slow == True and f_b.slow == True:
        f_b.vel[0] *= 0.25
        f_b.vel[1] *= 0.25
        f_b.slow = False


######################################################################################################################

def speed_2():
    ball.count_2 += 15
    ball.vel[1] = 0
    ball.vel[0] *= 5


def chang_2():
    ball.count_2 += 15
    ball.vel[1] *= -1


def teleport_2():
    ball.count_2 += 10
    ball.rect.y = random.randint(0, screen_height - ball.rect.height)
    ball.rect.x = random.randint(0, screen_width - ball.rect.width)


def slow_2():
    ball.count_2 += 6
    ball.vel[1] *= 0.25
    ball.vel[0] *= 0.25
    ball.slow = True


def ilousion_2():
    ball.count_2 += 1
    ball.vel[1] = random.choice([-ball.vel[1], ball.vel[1]])

    if ball.vel[1] >= 0:
        f_vel_y = -10
    else:
        f_vel_y = 10

    if ball.vel[0] >= 0:
        f_vel_x = 10
    else:
        f_vel_x = -10

    f_b = Fake_ball(ball.rect.x, ball.rect.y, [f_vel_x, f_vel_y])
    fake_ball_group.add(f_b)

##################################################################################################################


skill_1 = 3#random.randint(0, 3)

class Board_1(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 0 + 75
        self.rect.y = (screen_height / 2) - (self.rect.height / 2)

    def update(self):
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_w] and self.rect.y >= 0:
            self.rect.y -= 10

        if keyinput[pygame.K_s] and self.rect.y + self.rect.height <= screen_height:
            self.rect.y += 10


class Board_2(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width - 75
        self.rect.y = (screen_height / 2) - (self.rect.height / 2)

    def update(self):
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_UP] and self.rect.y >= 0:
            self.rect.y -= 10

        if keyinput[pygame.K_DOWN] and self.rect.y + self.rect.height <= screen_height:
            self.rect.y += 10

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "ball_10.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.vel = [-10, -10]
        self.rect.x = screen_width / 2
        self.rect.y = screen_height / 2
        self.count = 0
        self.count_2 = 0
        self.clicked = False
        self.slow = False
        self.il = False


    def update(self):
        global score_1
        global score_2
        global screen_width

        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        if self.rect.left <= 0:
            score_2 += 1
            score.play()
            reset_1()

        if self.rect.right >= screen_width:
            score_1 += 1
            score.play()
            reset_2()

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.vel[1] *= -1
            pong.play()

        if pygame.sprite.collide_mask(board_1, ball):
            self.vel[0] *= -1
            pong.play()
        if pygame.sprite.collide_mask(board_2, ball):
            self.vel[0] *= -1
            pong.play()

        keyinput = pygame.key.get_pressed()

        if keyinput[pygame.K_RSHIFT] and self.clicked == False:
            self.clicked = True
            if ball.count < 100:

                if skill_1 == 0:
                    speed()
                if skill_1 == 1:
                    chang()
                if skill_1 == 2:
                    teleport()
                if skill_1 == 3:
                    slow()
                #if skill_1 == 4 and self.il == False:
                    #ilousion()
                    #self.il = True


        if keyinput[pygame.K_LSHIFT] and self.clicked == False:
            self.clicked = True
            if ball.count_2 < 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:

                if skill_2 == 0:
                    speed_2()
                if skill_2 == 1:
                    chang_2()
                if skill_2 == 2:
                    teleport_2()
                if skill_2 == 3:
                    slow_2()
                if skill_2 == 4 and self.il == False:
                    ilousion_2()
                    self.il = True

        if abs(self.vel[0]) <= 0.15625 and abs(self.vel[1]) <= 0.15625 and ready == True:
            time.sleep(1)
            self.rect.x = screen_width / 2
            self.rect.y = screen_height / 2
            self.vel[0] = random.choice([-10, 10])
            self.vel[1] = random.choice([-10, 10])
            fake_ball_group.empty()
            self.il = False

        if event.type == pygame.KEYUP:
            self.clicked = False

class Fake_ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vel):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "ball_10.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.vel = vel
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global screen_width
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]


        if self.rect.left <= 0:
            self.kill()
            ball.il = False

        if self.rect.right >= screen_width:
            self.kill()
            ball.il = False

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.vel[1] *= -1
            pong.play()



class Menu_ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "ball_10.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.vel = [-7, -7]
        self.rect.x = screen_width / 2
        self.rect.y = screen_height / 2

    def update(self):
        global screen_width
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]


        if self.rect.left <= 0:
            self.vel[0] *= -1

            pong_2.play()

        if self.rect.right >= screen_width:
            self.vel[0] *= -1
            pong_2.play()

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.vel[1] *= -1
            pong_2.play()
class SKill_bar_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sk_count = 0
        self.sk_list = [
            pygame.image.load(os.path.join(image_path, "speed.png")).convert_alpha(),
            pygame.image.load(os.path.join(image_path, "curve.png")).convert_alpha(),
            pygame.image.load(os.path.join(image_path, "tp.png")).convert_alpha(),
            pygame.image.load(os.path.join(image_path, "slow.png")).convert_alpha(), ]

        self.image = self.sk_list[self.sk_count]
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 200
        self.click = False

    def update(self):
        keyinput = pygame.key.get_pressed()

        if keyinput[pygame.K_UP] and self.click == False:
            self.click = True

            if self.sk_count == 0:
                self.sk_count = 0
            else:
                self.sk_count -= 1

        if keyinput[pygame.K_DOWN] and self.click == False:
            self.click = True

            if self.sk_count == 3:
                self.sk_count = 3
            else:
                self.sk_count += 1

        if event.type == pygame.KEYUP:
            self.click = False

        self.image = self.sk_list[self.sk_count]


class SKill_bar_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sk_count = 0
        self.sk_list = [
            pygame.image.load(os.path.join(image_path, "speed.png")).convert_alpha(),
            pygame.image.load(os.path.join(image_path, "curve.png")).convert_alpha(),
            pygame.image.load(os.path.join(image_path, "tp.png")).convert_alpha(),
            pygame.image.load(os.path.join(image_path, "slow.png")).convert_alpha(), ]

        self.image = self.sk_list[self.sk_count]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.click = False

    def update(self):
        keyinput = pygame.key.get_pressed()

        if keyinput[pygame.K_w] and self.click == False:
            self.click = True

            if self.sk_count == 0:
                self.sk_count = 0
            else:
                self.sk_count -= 1

        if keyinput[pygame.K_s] and self.click == False:
            self.click = True

            if self.sk_count == 3:
                self.sk_count = 3
            else:
                self.sk_count += 1

        if event.type == pygame.KEYUP:
            self.click = False

        self.image = self.sk_list[self.sk_count]


screen_width = 1280
screen_height = 720

white = (255, 255, 255)

clock = pygame.time.Clock()

score_1 = 0
score_2 = 0

fb_b = False

game_over = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

fake_ball_group = pygame.sprite.Group()

score_font = pygame.font.SysFont("Bit Cheese10", 200)

game_over_font = pygame.font.SysFont("arialrounded", 60)

board_1 = Board_1(10, 100, white)
board_2 = Board_2(10, 100, white)
ball = Ball()
menu_ball = Menu_ball()

pong = pygame.mixer.Sound(os.path.join(sound_path, "pong.mp3"))
pong.set_volume(0.3)

pong_2 = pygame.mixer.Sound(os.path.join(sound_path, "pong.mp3"))
pong_2.set_volume(0.1)

score = pygame.mixer.Sound(os.path.join(sound_path, "score.mp3"))
score.set_volume(0.7)

result = str()
dt = int()
ready = True

def reset_1():
    ball.vel = [-10, -10]
    ball.rect.x = screen_width / 2
    ball.rect.y = screen_height / 2
    pygame.time.delay(1000)
def reset_2():
    ball.vel = [10, -10]
    ball.rect.x = screen_width / 2
    ball.rect.y = screen_height / 2
    pygame.time.delay(1000)

def display_score():
    global score_2
    global score_1
    score_font_1 = score_font.render(str(score_1), True, (255, 255, 255))
    score_font_2 = score_font.render(str(score_2), True, (255, 255, 255))

    screen.blit(score_font_1, (400, 50))
    screen.blit(score_font_2, (800, 50))




def display_game_over():
    global game_over, ready, resuit
    ready = False

    game_over_font = pygame.font.SysFont("arialrounded", 60)
    txt_game_over = game_over_font.render(result, True, (255, 255, 255))
    rect_game_over = txt_game_over.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(txt_game_over, rect_game_over)

    font = pygame.font.SysFont("헤드라인", 50)
    over_text = font.render(f"please, space key..", True, (255, 255, 255))
    screen.blit(over_text, (int(screen_width / 2 - over_text.get_width() / 2), int(screen_height / 4 * 2.5)))

    ball.vel = [0, 0]
    game_over = True

def restart_game():
    global game_over, score_1, score_2, skill_1, skill_2
    game_over = False
    ball.vel = [-10, -10]
    ball.count = 0
    ball.count_2 = 0
    score_1 = 0
    score_2 = 0


def main_menu():
    global dt, event, score_1, score_2
    ball.count = 0
    ball.count_2 = 0
    score_1 = 0
    score_2 = 0
    ball.rect.x = screen_width / 2
    ball.rect.y = screen_height / 2

    main_font = pygame.font.SysFont("arialrounded", 100)
    main_font_2 = pygame.font.SysFont("arialrounded", 50)

    main_txt_1 = main_font.render("PONG", True, (255, 255, 255))
    main_txt_2 = main_font_2.render("Start", True, (255, 255, 255))
    main_txt_3 = main_font_2.render("Exit", True, (255, 255, 255))
    click = False

    start = main_txt_2.get_rect()
    exit = main_txt_3.get_rect()

    start.x = 550
    start.y = 300
    exit.x = 550
    exit.y = 400



    while True:
        dt = clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        if start.collidepoint((mx, my)) and click == True:
            time.sleep(0.01)
            side_menu()

        if exit.collidepoint((mx, my)) and click == True:
                time.sleep(1)
                sys.exit()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        screen.fill((0, 0, 0))

        screen.blit(main_txt_1, (500, 100))
        screen.blit(main_txt_2, (550, 300))
        screen.blit(main_txt_3, (550, 400))

        menu_ball.update()
        screen.blit(menu_ball.image, menu_ball.rect)
        screen.blit(menu_ball.image, menu_ball.rect)

        pygame.display.update()



def side_menu():
    global dt, event
    global skill_1, skill_2
    side_font = pygame.font.SysFont("arialrounded", 70)

    start_txt = side_font.render("start", True, (255, 255, 255))
    start_txt_2 = side_font.render("Chose Skill!", True, (241, 213, 105))
    click = False

    start = start_txt.get_rect()

    start.x = 550
    start.y = 525
    sk_bar_1 = SKill_bar_1()
    sk_bar_2 = SKill_bar_2()


    while True:
        dt = clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        if start.collidepoint((mx, my)) and click == True:
            skill_1 = sk_bar_1.sk_count
            skill_2 = 4#sk_bar_2.sk_count
            time.sleep(0.01)
            game()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        screen.fill((0, 0, 0))

        screen.blit(start_txt, (550, 525))
        screen.blit(start_txt_2, (450, 100))

        sk_bar_1.update()
        screen.blit(sk_bar_1.image, sk_bar_1.rect)

        sk_bar_2.update()
        screen.blit(sk_bar_2.image, sk_bar_2.rect)

        pygame.display.update()



def pause():
    global dt, event
    main_font = pygame.font.SysFont("arialrounded", 80)
    main_font_2 = pygame.font.SysFont("arialrounded", 50)

    main_txt_1 = main_font.render("Pause", True, (255, 255, 255))
    main_txt_2 = main_font_2.render("Restart", True, (255, 255, 255))
    main_txt_3 = main_font_2.render("Exit", True, (255, 255, 255))
    click = False

    restart = main_txt_2.get_rect()
    exit = main_txt_3.get_rect()

    restart.x = 150
    restart.y = 300
    exit.x = 150
    exit.y = 400



    while True:
        dt = clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        if restart.collidepoint((mx, my)) and click == True:
            break

        if exit.collidepoint((mx, my)) and click == True:
            main_menu()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        screen.fill((0, 0, 0))

        screen.blit(main_txt_1, (70, 50))
        screen.blit(main_txt_2, (150, 300))
        screen.blit(main_txt_3, (150, 400))

        pygame.display.update()




def game():
    global result, ready, dt
    global event
    while True:

        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            key_event = pygame.key.get_pressed()
            if key_event[pygame.K_SPACE] and game_over:
                restart_game()

            if key_event[pygame.K_ESCAPE]:
                pause()

        if pygame.sprite.collide_mask(board_1, ball):
            if ball.slow:

                ball.vel[0] = 10
                if ball.vel[1] > 0:
                    ball.vel[1] = 10

                else:
                    ball.vel[1] = -10
                ball.slow = False

        if pygame.sprite.collide_mask(board_2, ball):
            if ball.slow:

                ball.vel[0] = 10
                if ball.vel[1] > 0:
                    ball.vel[1] = 10

                else:
                    ball.vel[1] = -10
                ball.slow = False

        screen.fill((0, 0, 0))

        board_1.update()
        screen.blit(board_1.image, board_1.rect)

        board_2.update()
        screen.blit(board_2.image, board_2.rect)

        ball.update()
        screen.blit(ball.image, ball.rect)

        fake_ball_group.update()
        fake_ball_group.draw(screen)

        display_score()

        if score_1 >= 10:
            result = "player1 win!"
            ready = False
            display_game_over()

        if score_2 >= 10:
            result = "player2 win!"
            ready = False
            display_game_over()

        pygame.draw.line(screen, white, [screen_width / 2, 0], [screen_width / 2, screen_height], 2)

        pygame.display.update()


main_menu()