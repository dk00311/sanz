import random
import math
import pygame
import os

##########################
pygame.init()
# 변수
image_path = os.path.join("source\\image")
font_path = os.path.join("source\\font\\comicsans.ttf")

sans = pygame.image.load(os.path.join(image_path, "sans.png"))
sans = pygame.transform.scale(sans, (200, 200))

# 스크린
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

arena_width = 300  # 700
arena_height = 300
arena_x = (screen_width - arena_width) / 2
arena_y = screen_height - (arena_height + 150) + 70
count = 0

is_jump= False
ouch = 0
myFont = pygame.font.Font(font_path, 25)

pos = [1, 2, 3]

speed = 10
counter = 0
Opening_font = pygame.font.Font(font_path, 50)
message = "Here we go"
####################################################
# 클래스
class Player(pygame.sprite.Sprite):  # 플레이어
    def __init__(self, x, y):
        super().__init__()
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.x = float(x)
        self.y = float(y)
        self.vel_y = 0
        self.color = (255, 0, 0)

        if self.y >= arena_y + arena_height - 7:
            self.on_ground = True
        else:
            self.on_ground = False

        self.jump_pressed = False
        self.jump_time = 0.0
        self.gravity = 1500

        self.jump_force_max = 2800
        self.jump_force_rate = 4000
        self.jump_force_duration = 0.28

        self.hover_time_max = 0.2  # 현재 정점정지 남은 시간
        self.hover_time = 0
        self.is_hovering = False
        self.has_hovered = False

        self.enum = False
        self.enum_time = 0.07
        self.time = 0

        self.gravity = False
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 255))  # 불투명 흰색으로 채움
        self.mask = pygame.mask.from_surface(self.surf)
        self.mask = pygame.mask.from_surface(self.surf)

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
                to_y = 0
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
        self.mask = pygame.mask.from_surface(self.surf)

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
        self.mask = pygame.mask.from_surface(self.surf)

    def colid(self):
        global ouch

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


        for bs in blasters:
            if bs.check_hit(self):
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


class Blaster(pygame.sprite.Sprite):   # size = 100, 240
    def __init__(self, pos, move_pos, move_ms, fire_ms, waiting_ms, rotate, size):
        super().__init__()
        self.start_pos  = pygame.Vector2(pos)
        self.target_pos = pygame.Vector2(move_pos)
        self.pos        = pygame.Vector2(pos)

        self.move_ms    = float(move_ms) / 1000.0
        self.fire_ms    = float(fire_ms) / 1000.0
        self.waiting_ms = float(waiting_ms) / 1000.0
        self.t          = 0.0

        self.state   = "charge"
        self.size = size
        self.rotate  = float(rotate)     # 0=아래, +CW
        self.thickness = 0

        raw = pygame.image.load(os.path.join(image_path, "blaster.png")).convert_alpha()
        self.base_image = pygame.transform.scale(raw, size)
        self.image = self.base_image
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

        self.gun_offset = pygame.Vector2(0, self.base_image.get_height() / 2)

        self.beam_base = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.beam_base.fill((255, 255, 255))

        self.mask = None        # 현재 빔의 mask
        self.beam_rect = None   # 현재 빔의 rect

    # ---------------- core helpers ----------------
    def _update_transform(self):
        self.image = pygame.transform.rotate(self.base_image, self.rotate)
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def _muzzle_world(self):
        off = self.gun_offset.rotate(-self.rotate)
        return pygame.Vector2(self.pos.x + off.x, self.pos.y + off.y)

    def _draw_beam(self, screen, muzzle, length, thickness):
        if thickness <= 0:
            self.mask = None
            self.beam_rect = None
        L = max(1, min(1500, int(length)))  # 길이 클램프
        T = max(1, min(256, int(thickness)))  # 두께 클램프 (너무 크지 않게)

        # 굳이 smoothscale 필요 없으면 일반 scale이 더 안전/빠름
        scaled = pygame.transform.scale(self.beam_base, (T, L))
        rotated = pygame.transform.rotate(scaled, self.rotate)

        off = pygame.Vector2(0, L/2).rotate(-self.rotate)
        center = (muzzle.x + off.x, muzzle.y + off.y)

        rect = rotated.get_rect(center=(int(center[0]), int(center[1])))
        screen.blit(rotated, rect.topleft)

        # 여기서 beam용 mask와 rect 저장
        self.mask = pygame.mask.from_surface(rotated)
        self.beam_rect = rect

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
                progress = self.t / self.fire_ms
                max_thickness = int(self.size[0] * 6 / 5)
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
                max_thickness = int(self.size[0] * 6 / 5)
                if progress >= 0.7:
                    fade = (progress - 0.7) / 0.3
                    self.thickness = max(0, int((1.0 - fade) * max_thickness))
                else:
                    self.thickness = max_thickness

        self._update_transform()

    def draw(self, screen):
        if self.state in ("fire", "done") and self.thickness > 0:
            muzzle = self._muzzle_world()
            self._draw_beam(screen, muzzle, length=1000, thickness=self.thickness)
        else:
            self.mask = None
            self.beam_rect = None

        screen.blit(self.image, self.rect)

    def look_at(self, player_pos):
        dx = player_pos[0] - self.pos.x
        dy = player_pos[1] - self.pos.y
        self.rotate = math.degrees(math.atan2(dx, dy))

    # ---------------- 충돌 체크 ----------------
    def check_hit(self, player):
        if self.mask and self.beam_rect and player.mask:
            offset = (player.rect.x - self.beam_rect.x,
                      player.rect.y - self.beam_rect.y)
            return self.mask.overlap(player.mask, offset) is not None
        return False


class PatternManager:
    def __init__(self):
        # (func, interval_ms, loops, min_clear_ms, delay_ms)
        self.queue = []
        self.i = -1
        self.active_func = None
        self.count = 0
        self.started_at = 0
        self.loops = 0
        self.state = "idle"
        self.wait_until = 0

    def add(self, func, interval_ms, loops, min_clear_ms=0, delay_ms=0):
        """delay_ms = 패턴 종료 후 다음 패턴 시작까지의 대기시간"""
        self.queue.append((func, interval_ms, loops, min_clear_ms, delay_ms))

    def start(self):
        self.i = -1
        self.next()

    def next(self):
        global is_jump, type
        self.i += 1
        if self.i >= len(self.queue):
            pygame.time.set_timer(PATTERN_EVENT, 0)
            self.active_func = None
            self.state = "idle"
            print("\033[96m" + "축하해!" + "\033[97m" + "가서 맛있는 간식을 받도록 해! :)")
            return

        func, interval, loops, min_clear_ms, delay_ms = self.queue[self.i]
        self.active_func = func

        if self.active_func == spawn_bone_pattern_3 or self.active_func == spawn_bone_pattern_5_1 or self.active_func == spawn_bone_pattern_5_2:
            is_jump = True
            type = "A"

        elif self.active_func == spawn_bone_pattern_1 or self.active_func ==  spawn_bone_pattern_2:
            is_jump = True
            type = "only_jump"

        else:
            is_jump = False

        # if self.active_func == spawn_bone_pattern_1 or spawn_bone_pattern_2:
        #     is_jump = True
        #     type = "only_jump"
        #
        # elif self.active_func == spawn_bone_pattern_3 or spawn_bone_pattern_5 or spawn_bs_pattern_6:
        #     is_jump = True
        #     type = "a"
        # else:
        #     is_jump = False

        self.count = 0
        self.loops = loops
        self.started_at = pygame.time.get_ticks()
        self.state = "active"
        self.delay_ms = delay_ms
        pygame.time.set_timer(PATTERN_EVENT, interval, loops=loops)

    def on_event(self):
        if self.state == "active" and self.active_func:
            self.active_func()
            self.count += 1


    def update(self, bones, blasters, rb):
        global count
        now = pygame.time.get_ticks()

        if self.state == "waiting":
            if now >= self.wait_until:
                self.next()
            return

        if self.state == "active" and self.active_func:
            _, _, loops, min_clear_ms, delay_ms = self.queue[self.i]

            finished_loops = (self.count >= loops)
            cleared = (len(bones) == 0) and (len(blasters) == 0) and (rb is None)
            enough_time = (now - self.started_at) >= min_clear_ms

            if finished_loops and cleared and enough_time:
                # 대기 상태로 전환
                self.state = "waiting"
                count = 0
                self.wait_until = now + delay_ms
                pygame.time.set_timer(PATTERN_EVENT, 0)  # 이벤트 정지




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

    length = (60 * math.sin(count / 5) + 80)
    boone = Bone((arena_x + 7, arena_y + arena_height - 5 - length), "right", 0, (20, length), 1000)
    boone.make_bone()
    boone.add(bones)

    length_2 = (-60 * math.sin(count / 5) + 130)
    boone = Bone((arena_x + 7, arena_y + 5), "right", 180, (20, length_2), 1000)
    boone.make_bone()
    boone.add(bones)

def spawn_bone_pattern_5_1():
    global count
    count += 1

    if count <= 15:
        length = 130
    else:
        length = 30

    boone = Bone((arena_x + 7, arena_y + arena_height - length), "right", 0, (20, length), 900)

    boone.make_bone()
    boone.add(bones)


def spawn_bone_pattern_5_2():
    global count
    count += 1
    if count <= 15:
        length = 130
    else:
        length = 30

    boone = Bone((arena_x - 27 + arena_width, arena_y + arena_height - length), "left", 0, (20, length), 900)
    boone.make_bone()
    boone.add(bones)


def spawn_bs_pattern_1():
    bs = Blaster((arena_x + arena_width - 70, -100), (arena_x + arena_width - 70, 200), 400, 600, 400, 0, (70, 210))
    bs.add(blasters)

    bs = Blaster((arena_x + 70, -100), (arena_x + 70, 200), 400, 600, 400, 0, (70, 210))
    bs.add(blasters)

    bs = Blaster((-100, arena_y + 70), (200, arena_y + 70), 400, 600, 400, 90, (70, 210))
    bs.add(blasters)

    bs = Blaster((-100, arena_y + arena_height - 70), (200, arena_y + arena_height - 70), 400, 600, 400, 90, (70, 210))
    bs.add(blasters)

def spawn_bs_pattern_2():
    bs = Blaster((arena_x - 500, arena_y - 500), (arena_x - 100, arena_y - 100), 400, 600, 400, 45, (100, 240))
    bs.add(blasters)

    bs = Blaster((arena_x + arena_width + 500, arena_y - 500), (arena_x + arena_width + 100, arena_y - 100), 400, 600, 400, -45, (100, 240))
    bs.add(blasters)

def spawn_bs_pattern_3():
    bs = Blaster((-100, arena_y + arena_height / 2), (200, arena_y + arena_height / 2), 400, 800, 700, 90, (200, 480))
    bs.add(blasters)

    bs = Blaster((screen_width + 100, arena_y + arena_height / 2), (screen_width - 200, arena_y + arena_height / 2), 400, 800, 700, -90, (200, 480))
    bs.add(blasters)

def spawn_bs_pattern_4():
    direction = random.choice([1, 2, 3, 4])
    if direction == 1:
        bs = Blaster((screen_width + 100, -100), (arena_x + arena_width, arena_y), 400, 500, 600, 90, (100, 240))
        bs.look_at(player.rect.center)
        bs.add(blasters)

    if direction == 2:
        bs = Blaster((-100, -100), (arena_x, arena_y), 400, 500, 600, 90, (100, 240))
        bs.look_at(player.rect.center)
        bs.add(blasters)

    if direction == 3:
        bs = Blaster((-100, screen_height + 100), (arena_x, arena_y + arena_height), 400, 500, 600, 90, (100, 240))
        bs.look_at(player.rect.center)
        bs.add(blasters)

    if direction == 4:
        bs = Blaster((screen_width + 100, screen_height + 100), (arena_x + arena_width, arena_y + arena_height), 400, 500, 600, 90, (100, 240))
        bs.look_at(player.rect.center)
        bs.add(blasters)

def spawn_bs_pattern_5():
    global pos

    direction = random.choice(pos)
    if direction == 1:
        bs = Blaster((-240, arena_height + arena_y - 30), (0, arena_height + arena_y - 30), 400, 500, 400, 90, (100, 240))
        bs.add(blasters)
        pos = [2, 3]

    if direction == 2:
        bs = Blaster((-240, arena_height/2 + arena_y), (0, arena_height/2 + arena_y), 400, 500, 400, 90, (100, 240))
        bs.add(blasters)
        pos = [1, 3]

    if direction == 3:
        bs = Blaster((-240, arena_y + 30), (0, arena_y + 30), 400, 500, 400, 90, (100, 240))
        bs.add(blasters)
        pos = [1, 2]

def spawn_bs_pattern_6():
    for i in range(9):
        p_x = player.x
        p_y = player.y

        x = -500 * math.sin(i / 3) + p_x
        y = -500 * math.cos(i / 3) + p_y

        bs = Blaster((-100, -100), (x, y), 400, 500, 600, i * 19, (35, 150))
        bs.add(blasters)



def spawn_bs_pattern_7():
    global count
    count += 1
    bs = Blaster((arena_x + count * 70, -100), ((arena_x + count * 70, 100)), 100, 800, 0, 0, (70, 240))
    bs.add(blasters)

def spawn_bs_pattern_8():
    global count
    count += 1

    x = -600 * math.sin(count / 3) + arena_x + arena_width / 2
    y = -600 * math.cos(count / 3) + arena_y + arena_height / 2

    start_x = -800 * math.sin(count / 3) + screen_width / 2
    start_y = -800 * math.cos(count / 3) + screen_height / 2

    dx = arena_x + arena_width / 2 - x
    dy = arena_y + arena_height / 2 - y
    rotate = math.degrees(math.atan2(dx, dy))

    bs = Blaster((start_x, start_y), (x, y), 400, 300, 100, rotate, (35, 150))
    bs.add(blasters)

#########################################################

def increase_arena():
    global  count, arena_width, message, counter
    message = "haha"
    counter = 0
    count += 1
    arena_width = count + 300

def wait():
    global arena_width
    arena_width = 300



# 클래스 변수
player = Player(screen_width / 2, screen_height / 2 + 150)
rb = None
type = "jump"
x = 0
y = 0

bones = pygame.sprite.Group()
clock = pygame.time.Clock()
blasters = pygame.sprite.Group()
PATTERN_EVENT = pygame.USEREVENT + 99

manager = PatternManager()
manager.add(wait, 1, 1, delay_ms = 2000)
manager.add(spawn_bone_pattern_4, 30, 100)
manager.add(spawn_bs_pattern_1, 1, 1)
manager.add(spawn_bs_pattern_2, 1, 1)
manager.add(spawn_bs_pattern_1, 1, 1)
manager.add(spawn_bs_pattern_3, 100, 1, delay_ms=1000)
manager.add(increase_arena, 1, 400, delay_ms=1000)

manager.add(spawn_bone_pattern_1, 800, 10, delay_ms=2000)
manager.add(spawn_bone_pattern_2, 800, 10, delay_ms=2000)
manager.add(spawn_bs_pattern_5, 1000, 10, delay_ms=2000)
manager.add(spawn_bone_pattern_3, 900, 10, delay_ms=5000)

manager.add(spawn_bone_pattern_1, 800, 15, delay_ms=2000)
manager.add(spawn_bone_pattern_2, 800, 20)
manager.add(spawn_bs_pattern_4, 1000, 10)
manager.add(spawn_bone_pattern_5_1, 30, 30)
manager.add(spawn_bone_pattern_5_2, 30, 30)

manager.add(spawn_bs_pattern_7, 120, 9)
manager.add(spawn_bs_pattern_3, 30, 1)
manager.add(wait, 1, 1, delay_ms=2000)
manager.add(spawn_bs_pattern_8, 110, 19)
manager.start()



def end():
    global running
    speed = 3
    counter = 0
    Opening_font = pygame.font.Font(font_path, 50)
    message = "Game Over"
    done = False

    running = True
    while running:
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    break

        if counter < speed * len(message):
            counter += 1
        else:
            pass

        snip = Opening_font.render(message[0:int(counter // speed)], True, (255, 255, 255))
        screen.blit(snip, (450, 200))

        pygame.display.update()
    pygame.quit()

# 매인
running = True
while running:
    dt = clock.tick(120) / 1000

    # 이벤트 감지 동작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #보스전 패턴
        if event.type == PATTERN_EVENT:
            manager.on_event()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and player.on_ground == True:
                player.jump()

            if event.key == pygame.K_r:
                ouch = 0

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_SPACE:
                player.jump_cut()

    if manager != None:
        manager.update(bones, blasters, rb)

    # 그리기
    screen.fill((0, 0, 0))
    screen.blit(sans, (550, 100))

    if counter < speed * len(message):
        counter += 1
    else:
        pass

    snip = Opening_font.render(message[0:int(counter // speed)], True, (255, 255, 255))
    screen.blit(snip, (800, 150))

    if player != None:

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
        bs.draw(screen)

    ouch_text = myFont.render(str(100-ouch) + "/100", True, (255, 255, 255))

    arena_x = (screen_width - arena_width) / 2
    arena = pygame.Rect(arena_x, arena_y, arena_width, arena_height)
    pygame.draw.rect(screen, (255, 255, 255), arena, 5)

    hp_x = (screen_width - arena_width) / 2
    hp_y = arena_y + arena_height + 40
    pygame.draw.rect(screen, (255, 0, 0), (hp_x, hp_y, 200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 0), (hp_x, hp_y, 200 - ouch*2, 20), 0)

    screen.blit(ouch_text, (hp_x + 210, hp_y))

    if ouch >= 100:
        screen.fill((0, 0, 0))
        end()
        break

    pygame.display.update()




pygame.quit()