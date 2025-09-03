import pygame
import os

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
        self.on_ground = False
        self.vel_y = 0

    def move(self):
        to_x = 0
        to_y = 0

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_a] and self.rect.x >= arena_x + 5:
            to_x = -0.3 * dt

        if key_input[pygame.K_d] and self.rect.x <= (arena_x + arena_width) - (self.width + 5):
            to_x = 0.3 * dt

        if key_input[pygame.K_s] and self.rect.y <= (arena_y + arena_height) - self.height - 5:
            to_y = 0.3 * dt

        if key_input[pygame.K_w] and self.rect.y >= arena_y + 5:
            to_y = -0.3 * dt

        self.x += to_x
        self.y += to_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.vel_y = -15

    def jump_cut(self):
        if self.vel_y < -1:
            self.vel_y = -1

    def jumping_move(self, type):
        self.type = type
        to_x = 0

        event = pygame.event.poll()
        key_input = pygame.key.get_pressed()

        #좌우 이동 가능 체크
        if self.type != "no_jump":
            if key_input[pygame.K_a] and self.rect.x >= arena_x + 5:
                to_x = -0.3 * dt

            if key_input[pygame.K_d] and self.rect.x <= (arena_x + arena_width) - (self.width + 5):
                to_x = 0.3 * dt

        #점핑
        if key_input[pygame.K_SPACE]:
            self.jump()
        else:
            self.jump_cut()

        gravity = 0.1

        self.vel_y += gravity * dt

        self.x += to_x
        self.y += self.vel_y

        #착지 판정
        if self.y + self.height >= arena_y + arena_height-5:
            self.y = arena_y + arena_height - self.height - 5
            self.vel_y = 0
            self.on_ground = True

        # 중력 가속도 제한
        if self.vel_y >= 10:
            self.vel_y = 10

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class RisingBone():
    def __init__(self, direction, speed, length, grow_speed):
        self.direction = direction
        self.warn_speed = speed[0]
        self.speed = speed[1]
        self.length = length
        self.spawn_time = pygame.time.get_ticks()
        self.activate = False
        self.warn = None
        self.alive = True
        self.grow_speed = grow_speed
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
            self.current_length += self.grow_speed * dt


    def draw(self):
        pos = 0
        if not self.activate:
            pygame.draw.rect(screen, (255, 0, 0), self.warn, 3)

        else:
            #뼈 스케일링
            self.scaled = pygame.transform.scale(self.base_image, (arena_width, self.current_length))


            #뼈 그리기
            if self.direction == "up":
                self.image = self.scaled
                pos = (arena_x, arena_y)

            if self.direction == "down":
                self.image = pygame.transform.rotate(self.scaled, 180)
                pos = (arena_x, arena_y + arena_height - self.current_length)

            if self.direction == "right":
                self.image = pygame.transform.rotate(self.scaled, -90)
                pos = (arena_x + arena_width - self.current_length, arena_y)

            if self.direction == "left":
                self.image = pygame.transform.rotate(self.scaled, 90)
                pos = (arena_x, arena_y)

            screen.blit(self.image, pos)

class Bone(pygame.sprite.Sprite):
    def __init__(self, pos, direction, rotate, size, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.direction = direction
        self.rotate = rotate
        self.size = size
        self.speed = speed
        self.image = pygame.image.load(os.path.join(image_path, "bone.png")).convert_alpha()
        self.base_image = self.image

    def make_bone(self):
        self.scaled = pygame.transform.scale(self.image, self.size)
        self.image = pygame.transform.rotate(self.scaled, self.rotate)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):

        #rect 업데이트
        self.rect.topleft = (self.x, self.y)
        #움직임
        if self.direction == "up":
            self.y -= self.speed * dt

        if self.direction == "down":
            self.y += self.speed * dt

        if self.direction == "right":
            self.x += self.speed * dt

        if self.direction == "left":
            self.x -= self.speed * dt

        #화면 밖으로 나가면 kill
        if self.x <= arena_x or self.x >= (arena_x + arena_width):
            self.kill()

        if self.y <= arena_y or self.y >= (arena_y + arena_height):
            self.kill()


    def draw(self):
        screen.blit(self.image, self.rect)



def pattern_1():
    for i in range(6):
        boone = Bone((arena_x+15 + i * 50, arena_y), "down", 180, (20, 100), 0.3)
        boone.make_bone()
        boone.add(bones)

def pattern_2():
    for i in range(6):
        boone = Bone((arena_x+30 + i * 50, arena_y+arena_height-100), "up", 0, (20, 100), 0.3)
        boone.make_bone()
        boone.add(bones)


# 클래스 변수
player = Player(screen_width / 2, screen_height / 2 + 150)
rising_bone = None

bones = pygame.sprite.Group()


clock = pygame.time.Clock()

# 매인
running = True
while running:
    dt = clock.tick(120)

    # 이벤트 감지 동작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                pattern_1()
                pattern_2()

    # 그리기
    screen.fill((0, 0, 0))

    player.jumping_move("jump")
    player.draw()

    for b in bones:
        b.update()
        b.draw()


    pygame.draw.rect(screen, (255, 255, 255), arena, 5)

    pygame.display.update()

pygame.quit()