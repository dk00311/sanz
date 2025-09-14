import random
import math
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

arena_width = 700  # 700
arena_height = 300
arena_x = (screen_width - arena_width) / 2
arena_y = screen_height - (arena_height + 50)

arena = pygame.Rect(arena_x, arena_y, arena_width, arena_height, )
count = 0

is_jump= False
ouch = 0
myFont = pygame.font.SysFont(None, 50)


# 클래스
class Player:  # 플레이어
    def __init__(self, x, y):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = float(x)
        self.y = float(y)
        self.vel_y = 0
        self.color = (255, 0, 0)

        self.on_ground = False
        self.jump_pressed = False
        self.jump_time = 0.0
        self.gravity = 1500

        self.jump_force_max = 3000
        self.jump_force_rate = 4500
        self.jump_force_duration = 0.23

        self.hover_time_max = 0.2  # 현재 정점정지 남은 시간
        self.hover_time = 0
        self.is_hovering = False
        self.has_hovered = False

        self.enum = False
        self.enum_time = 0.07
        self.time = 0

        self.gravity = False
        self.surf = pygame.Surface((self.width, self.height))

    def move(self):
        to_x = 0
        to_y = 0
        self.color = (255, 0, 0)

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_a] and self.rect.x >= arena_x + 5:
            to_x = -300 * dt

        if key_input[pygame.K_d] and self.rect.x <= (arena_x + arena_width) - (self.width + 5):
            to_x = 300 * dt

        if key_input[pygame.K_s] and self.rect.y <= (arena_y + arena_height) - self.height - 5:
            to_y = 300 * dt

        if key_input[pygame.K_w] and self.rect.y >= arena_y + 5:
            to_y = -300 * dt

        if rb != None and rb.alive and not rb.activate and self.gravity == False:
            if rb.direction == "up":
                self.y = arena_y + 5
                self.gravity = True

            if rb.direction == "down":
                self.y = arena_y + arena_height - 5
                self.gravity = True

            if rb.direction == "left":
                self.x = arena_x + 5
                self.gravity = True

            if rb.direction == "right":
                self.x = arena_x + arena_width - 5
                self.gravity = True

        self.x += to_x
        self.y += to_y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.jump_pressed = True
            self.jump_time = 0
            self.vel_y = 0
            self.has_hovered = False

    def jump_cut(self):
        if (not self.on_ground) and (not self.has_hovered) and (self.vel_y < 0) and (self.type == "only_jump"):
            self.is_hovering = True
            self.hover_time = self.hover_time_max
            self.vel_y = 0
            self.has_hovered = True
        self.jump_pressed = False

    def jumping_move(self, type):
        self.color = (0, 0, 255)
        self.type = type
        self.gravity = 1500
        to_x = 0

        key_input = pygame.key.get_pressed()

        # 좌우 이동 가능 체크
        if self.type != "only_jump":
            if key_input[pygame.K_a] and self.rect.x >= arena_x + 5:
                to_x = -300 * dt

            if key_input[pygame.K_d] and self.rect.x <= (arena_x + arena_width) - (self.width + 5):
                to_x = 300 * dt

        # 점프
        if self.jump_pressed:
            self.jump_time += dt
            if self.jump_time < self.jump_force_duration:
                self.vel_y -= self.jump_force_rate * dt

                if self.vel_y < -self.jump_force_max:
                    self.vel_y = -self.jump_force_max

            else:
                self.jump_pressed = False

        # 호버링 & 중력
        if self.is_hovering and self.type == "only_jump":
            self.hover_time -= dt
            if self.hover_time <= 0:
                self.is_hovering = False

        else:
            self.vel_y += self.gravity * dt
            self.y += self.vel_y * dt

        self.x += to_x

        # 착지 판정
        if self.y + self.height >= arena_y + arena_height - 5:
            self.y = arena_y + arena_height - self.height - 5
            self.vel_y = 0
            self.on_ground = True

        # 중력 가속도 제한
        if self.vel_y >= 3000:
            self.vel_y = 3000

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def colid(self):
        global ouch
        self.mask = pygame.mask.from_surface(self.surf)

        for boone in bones:
            if self.rect.colliderect(boone.rect):
                if self.enum == False:
                    ouch += 1
                    self.enum = True

                else:

                    self.time += dt
                    if self.enum_time <= self.time:
                        self.enum = False
                        self.time = 0

        if rb != None and rb.activate and self.rect.colliderect(rb.rect):
            if self.enum == False:
                ouch += 1
                self.enum = True

            else:

                self.time += dt
                if self.enum_time <= self.time:
                    self.enum = False
                    self.time = 0.03




    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


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
            self.x = arena_x
            self.y = arena_y

        if self.direction == "down":
            self.warn = pygame.Rect(arena_x, arena_y + arena_height - self.length, arena_width, self.length)
            self.x = arena_x
            self.y = arena_y + arena_height - self.length

        if self.direction == "right":
            self.warn = pygame.Rect(arena_x + arena_width - self.length, arena_y, self.length, arena_height)
            self.x = arena_x + arena_width - self.length
            self.y = arena_y

        if self.direction == "left":
            self.warn = pygame.Rect(arena_x, arena_y, self.length, arena_height)
            self.x = arena_x
            self.y = arena_y

    def update(self):
        # 시간 체크 알고리즘
        now = pygame.time.get_ticks()
        if not self.activate and now - self.spawn_time >= self.warn_speed:
            self.activate = True
            self.spawn_time = now

        if self.activate and self.current_length <= self.length:
            self.current_length += self.grow_speed * dt

        if self.activate and now - self.spawn_time >= self.speed:
            self.alive = False
            player.gravity = False

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        pos = 0
        if not self.activate:
            pygame.draw.rect(screen, (255, 0, 0), self.warn, 3)

        else:
            # 뼈 스케일링
            self.scaled = pygame.transform.scale(self.base_image, (arena_width, self.current_length))

            # 뼈 그리기
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

        # rect 업데이트
        self.rect.topleft = (self.x, self.y)
        # 움직임
        if self.direction == "up":
            self.y -= self.speed * dt

        if self.direction == "down":
            self.y += self.speed * dt

        if self.direction == "right":
            self.x += self.speed * dt

        if self.direction == "left":
            self.x -= self.speed * dt

        # 화면 밖으로 나가면 kill
        if self.x <= arena_x or self.x >= (arena_x + arena_width):
            self.kill()

        if self.y <= arena_y or self.y >= (arena_y + arena_height):
            self.kill()


    def draw(self):
        screen.blit(self.image, self.rect)


class Blaster(pygame.sprite.Sprite):
    def __init__(self, pos, move_pos, move_ms, fire_ms, waiting_ms, rotate, size=1):
        super().__init__()
        # 위치(부동소수점 중심)
        self.start_pos  = pygame.Vector2(pos)
        self.target_pos = pygame.Vector2(move_pos)
        self.pos        = pygame.Vector2(pos)

        # 시간(초)
        self.move_ms    = float(move_ms) / 1000.0
        self.fire_ms    = float(fire_ms) / 1000.0
        self.waiting_ms = float(waiting_ms) / 1000.0
        self.t          = 0.0

        self.state   = "charge"
        self.size    = size
        self.rotate  = float(rotate)     # 0=아래, +CW
        self.thickness = 0

        # 본체 이미지
        raw = pygame.image.load(os.path.join(image_path, "blaster.png")).convert_alpha()
        self.base_image = pygame.transform.scale(raw, (100 * self.size, 240 * self.size))
        self.image = self.base_image
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

        # 총구(중앙 아래) 기준 오프셋
        self.gun_offset = pygame.Vector2(0, self.base_image.get_height() / 2)

        # 빔 기본 이미지(투명 포함)
        self.beam_base = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.beam_base.fill((255, 255, 255))


        self.beam_mask = None
        self.beam_rect = None

    # ---------------- core helpers ----------------
    def _update_transform(self):
        # 규약: 0=아래, +CW → rotate(-angle)로 통일
        self.image = pygame.transform.rotate(self.base_image, self.rotate)
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def _muzzle_world(self):
        # 총구: base_image의 중앙 아래에서 -rotate만큼 회전한 오프셋을 pos에 더함
        off = self.gun_offset.rotate(-self.rotate)
        return pygame.Vector2(self.pos.x + off.x, self.pos.y + off.y)

    def _draw_beam(self, screen, muzzle, length, thickness):
        if thickness <= 0:
            self.beam_mask = None
            self.beam_rect = None
            return
        L = max(1, int(length))
        T = max(1, int(thickness))

        scaled  = pygame.transform.smoothscale(self.beam_base, (T, L))
        self.rotated = pygame.transform.rotate(scaled, self.rotate)

        # 미회전 기준 (0, L/2) 오프셋을 -rotate로 돌려서 center를 총구에 정렬
        off = pygame.Vector2(0, L/2).rotate(-self.rotate)
        center = (muzzle.x + off.x, muzzle.y + off.y)

        rect = self.rotated.get_rect(center=(int(center[0]), int(center[1])))
        screen.blit(self.rotated, rect.topleft)

        self.beam_rect = rect
        self.beam_mask = pygame.mask.from_surface(self.rotated)

    def hits_player_rect(self, player_rect: pygame.Rect) -> bool:
        if not self.beam_mask or not self.beam_rect:
            return False
        # 플레이어를 꽉 찬 사각형 마스크로 한 번만 만들거나, 아래처럼 매번 만들어도 됨
        psurf = pygame.Surface((player_rect.w, player_rect.h), pygame.SRCALPHA)
        psurf.fill((255, 255, 255, 255))
        pmask = pygame.mask.from_surface(psurf)

        # other(플레이어)를 this(빔) 기준으로 이동시키는 오프셋
        offset = (player_rect.x - self.beam_rect.x,
                  player_rect.y - self.beam_rect.y)
        return self.beam_mask.overlap(pmask, offset) is not None


    # ---------------- state machine ----------------
    def update(self):
        self.t += dt

        if self.state == "charge":
            if self.t >= self.move_ms:
                self.pos.update(self.target_pos)
                self.state, self.t = "wait", 0.0
            else:
                progress = min(1.0, self.t / self.move_ms)
                self.pos = self.start_pos.lerp(self.target_pos, progress)

        elif self.state == "wait":
            if self.t >= self.waiting_ms:
                self.state, self.t = "fire", 0.0

        elif self.state == "fire":
            if self.t >= self.fire_ms:
                self.state, self.t = "done", 0.0
            else:
                # 두께 이징(초반만 커지게)
                progress = self.t / self.fire_ms
                max_thickness = int((100 * self.size) * 6 / 5)
                if progress < 0.1:
                    self.thickness = int(max_thickness * (progress / 0.1))
                else:
                    self.thickness = max_thickness

        elif self.state == "done":
            if self.t >= self.move_ms:
                self.pos.update(self.start_pos)
                self.kill()
                return
            else:
                progress = min(1.0, self.t / self.move_ms)
                self.pos = self.target_pos.lerp(self.start_pos, progress)
                # 마지막 30%에서 서서히 얇아지기
                max_thickness = int((100 * self.size) * 6 / 5)
                if progress >= 0.7:
                    fade = (progress - 0.7) / 0.3
                    self.thickness = max(0, int((1.0 - fade) * max_thickness))
                else:
                    self.thickness = max_thickness

        # 항상 마지막에 변환 갱신 (rect는 여기서만 만질 것!)
        self._update_transform()

    def draw(self):
        # 레이저 먼저(또는 나중) 그려도 OK
        if self.state in ("fire", "done") and self.thickness > 0:
            muzzle = self._muzzle_world()
            self._draw_beam(screen, muzzle, length=1000, thickness=self.thickness)

        # 본체
        screen.blit(self.image, self.rect)

    def look_at(self, player_pos):
        # 0=아래, +CW 규약에 맞춘 각도
        dx = player_pos[0] - self.pos.x
        dy = player_pos[1] - self.pos.y
        self.rotate = math.degrees(math.atan2(dx, dy))


def start_pattern(pattern, interval, loops):
    global count

    pygame.time.set_timer(pattern, interval, loops=loops)
    count = 0


def stop_pattern(pattern):
    pygame.time.set_timer(pattern, 0)


def spawn_bone_pattern_1():  # 800
    boone = Bone((arena_x + 7, arena_y + arena_height - 50), "right", 0, (20, 50), 200)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x + 7, arena_y + 5), "right", 180, (20, arena_height - 50 - player.height - 20), 200)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x - 7 - 20 + arena_width, arena_y + arena_height - 50), "left", 0, (20, 50), 200)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x - 7 - 20 + arena_width, arena_y + 5), "left", 180,
                 (20, arena_height - 50 - player.height - 20), 200)
    boone.make_bone()
    boone.add(bones)


def spawn_bone_pattern_2():  # 1000
    height = random.choice([20, 50, 80])

    boone = Bone((arena_x + 7, arena_y + arena_height - height), "right", 0, (20, height), 200)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x + 7, arena_y + 5), "right", 180, (20, arena_height - height - player.height - 20), 200)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x - 7 - 20 + arena_width, arena_y + arena_height - height), "left", 0, (20, height), 200)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x - 7 - 20 + arena_width, arena_y + 5), "left", 180,
                 (20, arena_height - height - player.height - 20), 200)
    boone.make_bone()
    boone.add(bones)


def spawn_bone_pattern_3():  # 900
    boone = Bone((arena_x + 7, arena_y + arena_height - 30), "right", 0, (20, 30), 150)
    boone.make_bone()
    boone.add(bones)

    boone = Bone((arena_x - 27 + arena_width, arena_y + 5), "left", 180, (20, 270), 150)
    boone.make_bone()
    boone.add(bones)


def spawn_bone_pattern_4():  # 50, 45 / length = 60, 50, 45    /length = 60, 30, 100
    global count
    count += 1

    length = (60 * math.sin(count / 5) + 70)
    boone = Bone((arena_x + 7, arena_y + arena_height - 5 - length), "right", 0, (20, length), 1000)
    boone.make_bone()
    boone.add(bones)

    length_2 = (-60 * math.sin(count / 5) + 120)
    boone = Bone((arena_x + 7, arena_y + 5), "right", 180, (20, length_2), 1000)
    boone.make_bone()
    boone.add(bones)

def spawn_bone_pattern_5(direction):
    global count
    count += 1

    if count <= 15:
        length = 130
    else:
        length = 30

    if direction == "left":
        boone = Bone((arena_x + 7, arena_y + arena_height - length), "right", 0, (20, length), 900)
    else:
        boone = Bone((arena_x - 27 + arena_width, arena_y + arena_height - length), "left", 0, (20, length), 900)

    boone.make_bone()
    boone.add(bones)

def spawn_bs_pattern_1():
    bs = Blaster((arena_x + arena_width / 3, -100), (arena_x + arena_width / 3, 200), 400, 800, 700, 0)
    bs.add(blasters)

    bs = Blaster((arena_x + arena_width / 3 * 2, -100), (arena_x + arena_width / 3 * 2, 200), 400, 800, 700, 0)
    bs.add(blasters)

    bs = Blaster((-100, arena_y + 30), (200, arena_y + 30), 400, 800, 700, 90)
    bs.add(blasters)

    bs = Blaster((-100, arena_y + arena_height - 30), (200, arena_y + arena_height - 30), 400, 800, 700, 90)
    bs.add(blasters)

def spawn_bs_pattern_2():
    bs = Blaster((arena_x - 500, arena_y - 500), (arena_x - 100, arena_y - 100), 400, 800, 700, 45)
    bs.add(blasters)

    bs = Blaster((arena_x + arena_width + 500, arena_y - 500), (arena_x + arena_width + 100, arena_y - 100), 400, 800, 700, -45)
    bs.add(blasters)

def spawn_bs_pattern_3():
    bs = Blaster((-100, arena_y + arena_height / 2), (200, arena_y + arena_height / 2), 400, 800, 700, 90, 2)
    bs.add(blasters)

    bs = Blaster((screen_width + 100, arena_y + arena_height / 2), (screen_width - 200, arena_y + arena_height / 2), 400, 800, 700, -90, 2)
    bs.add(blasters)

def spawn_bs_pattern_4():
    direction = random.choice([1, 2, 3, 4])
    if direction == 1:
        bs = Blaster((screen_width + 100, -100), (arena_x + arena_width, arena_y), 400, 500, 600, 90, 1)
        bs.look_at(player.rect.center)
        bs.add(blasters)

    if direction == 2:
        bs = Blaster((-100, -100), (arena_x, arena_y), 400, 500, 600, 90, 1)
        bs.look_at(player.rect.center)
        bs.add(blasters)

    if direction == 3:
        bs = Blaster((-100, screen_height + 100), (arena_x, arena_y + arena_height), 400, 500, 600, 90, 1)
        bs.look_at(player.rect.center)
        bs.add(blasters)

    if direction == 4:
        bs = Blaster((screen_width + 100, screen_height + 100), (arena_x + arena_width, arena_y + arena_height), 400, 500, 600, 90, 1)
        bs.look_at(player.rect.center)
        bs.add(blasters)


# 클래스 변수
player = Player(screen_width / 2, screen_height / 2 + 150)
rb = None
type = "jump"

bones = pygame.sprite.Group()
clock = pygame.time.Clock()
blasters = pygame.sprite.Group()

# 보스 패턴 관련 변수
bone_pattern_1 = pygame.USEREVENT + 1
bone_pattern_2 = pygame.USEREVENT + 2
bone_pattern_3 = pygame.USEREVENT + 3
bone_pattern_4 = pygame.USEREVENT + 4
bone_pattern_5 = pygame.USEREVENT + 5

blaster_pattern_1 = pygame.USEREVENT + 10
blaster_pattern_2 = pygame.USEREVENT + 11

# 매인
running = True
while running:
    dt = clock.tick(120) / 1000

    # 이벤트 감지 동작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #보스전 패턴
        if event.type == bone_pattern_1:
            spawn_bone_pattern_1()
            player.x = screen_width / 2
            type = "only_jump"

        if event.type == bone_pattern_2:
            spawn_bone_pattern_2()
            player.x = screen_width / 2
            type = "only_jump"

        if event.type == bone_pattern_3:
            spawn_bone_pattern_3()
            type = "jump"

        if event.type == bone_pattern_4:
            spawn_bone_pattern_4()

        if event.type == bone_pattern_5:
            spawn_bone_pattern_5("left")

        if event.type == blaster_pattern_1:
            spawn_bs_pattern_4()

        if event.type == pygame.KEYDOWN:

           if event.key == pygame.K_1:
                start_pattern(blaster_pattern_1, 800, 10)

           if event.key == pygame.K_2:
                start_pattern(bone_pattern_2, 800, 10)
                is_jump = True
                type = "only_jump"

           if event.key == pygame.K_3:
                rb = RisingBone("up", (300, 500), 150, 500)
                is_jump = False
                rb.build_warn()

           if event.key == pygame.K_4:
                is_jump = True
                type = "aa"
                start_pattern(bone_pattern_3, 900, 10)

           if event.key == pygame.K_5:
                start_pattern(bone_pattern_4, 30, 45)
                is_jump = False

           if event.key == pygame.K_6:
                start_pattern(bone_pattern_5, 30, 30)
                is_jump = True
                type = "aa"

           if event.key == pygame.K_r:
                ouch = 0

           if event.key == pygame.K_SPACE and player.on_ground == True:
                player.jump()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE:
                player.jump_cut()

    # 그리기
    screen.fill((0, 0, 0))

    if is_jump == True:
        player.jumping_move(type)
    else:
        player.move()


    player.draw()
    player.colid()

    for b in bones:
        b.update()
        b.draw()

    if rb:
        rb.update()

        if not rb.alive:
            rb = None
        else:
            rb.draw()

    for bs in blasters:
        bs.update()
        bs.draw()

    ouch_text = myFont.render(str(ouch), True, (255, 0, 0))
    screen.blit(ouch_text, (0, 0))

    pygame.draw.rect(screen, (255, 255, 255), arena, 5)

    pygame.display.update()

pygame.quit()