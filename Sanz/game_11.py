import pygame
import os
import time

##########################
pygame.init()
# 변수
image_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\Sanz\\source\\image")

# 스크린
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

arena_width = 300 # 700
arena_height = 300
arena_x = (screen_width - arena_width) / 2
arena_y = screen_height - (arena_height + 50)

arena = pygame.Rect(arena_x, arena_y, arena_width, arena_height, )


# 클래스
class Player:  # 플레이어
    def __init__(self, x, y):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = float(x)
        self.y = float(y)

    def move(self):
        to_x = 0
        to_y = 0

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_a] and self.rect.x >= arena_x + 5:
            to_x = -0.2

        if key_input[pygame.K_d] and self.rect.x <= (arena_x + arena_width) - (self.width + 5):
            to_x = 0.2

        if key_input[pygame.K_s] and self.rect.y <= (arena_y + arena_height) - self.height - 5:
            to_y = 0.2

        if key_input[pygame.K_w] and self.rect.y >= arena_y + 5:
            to_y = -0.2

        self.x += to_x
        self.y += to_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class RisingBone():
    def __init__(self, direction, warn_speed, speed, length):
        self.direction = direction
        self.warn_speed = warn_speed
        self.speed = speed
        self.length = length
        self.spawn_time = pygame.time.get_ticks()
        self.activate = False
        self.warn = None
        self.alive = True
        self.current_length = 0
        self.image = pygame.image.load(os.path.join(image_path, "Rising_bone.png")).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.base_image = self.image

    def build_warn(self):

        if self.direction == "up":
            self.warn = pygame.Rect(arena_x, arena_y, arena_width, self.length)

        if self.direction == "down":
            self.warn = pygame.Rect(arena_x, arena_y + arena_height - self.length, arena_width, self.length)

        if self.direction == "right":
            self.warn = pygame.Rect(arena_x + arena_width - self.length, arena_y, self.length, arena_height)

        if self.direction == "left":
            self.warn = pygame.Rect(arena_x, arena_y, self.length, arena_height)


    def update(self):
        #시간 체크 알고리즘
        now = pygame.time.get_ticks()
        if not self.activate and now - self.spawn_time >= self.warn_speed:
            self.activate = True
            self.spawn_time = now

        if self.activate and now - self.spawn_time >= self.speed:
            self.alive = False

        if self.activate and self.current_length <= self.length:
            self.current_length += 0.7


    def draw(self):
        pos = 0
        if not self.activate:
            pygame.draw.rect(screen, (255, 0, 0), self.warn, 3)

        else:
            #뼈 스케일링
            self.image = pygame.transform.scale(self.base_image, (arena_width, self.current_length))


            #뼈 그리기
            if self.direction == "up":
                pos = (arena_x, arena_y)

            if self.direction == "down":
                self.image = pygame.transform.rotate(self.image, 180)
                pos = (arena_x, arena_y + arena_height - self.current_length)

            if self.direction == "right":
                self.image = pygame.transform.rotate(self.image, -90)
                pos = (arena_x + arena_width - self.current_length, arena_y)

            if self.direction == "left":
                self.image = pygame.transform.rotate(self.image, 90)
                pos = (arena_x, arena_y)

            screen.blit(self.image, pos)



# 클래스 변수
player = Player(screen_width / 2, screen_height / 2 + 150)
rising_bone = None

# 매인
running = True
while running:

    # 이벤트 감지 동작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                rising_bone = RisingBone("up", 500, 300, 180)
                rising_bone.build_warn()

            if event.key == pygame.K_2:
                rising_bone = RisingBone("down", 500, 300, 180)
                rising_bone.build_warn()

            if event.key == pygame.K_3:
                rising_bone = RisingBone("right", 500, 300, 180)
                rising_bone.build_warn()

            if event.key == pygame.K_4:
                rising_bone = RisingBone("left", 500, 300, 180)
                rising_bone.build_warn()

    # 그리기
    screen.fill((0, 0, 0))

    player.move()
    player.draw()

    if rising_bone:
        rising_bone.update()

        if not rising_bone.alive:
            rising_bone = None
        else:
            rising_bone.draw()

    pygame.draw.rect(screen, (255, 255, 255), arena, 5)

    pygame.display.update()

pygame.quit()