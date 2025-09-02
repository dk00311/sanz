import pygame, os, random
from pygame import mixer




mixer.init()
pygame.init()

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(image_path, "jump.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.y_vel = 0
        self.flip = False
        self.to_y = 0
        self.to_x = 0
        self.clicked = False

    def move(self):
        scroll = 0
        to_y = 0
        to_x = 0
        global gravity, game_over, score, skill, out


        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_a] and self.rect.x >= 0:
            to_x = -10
            self.flip = True

        if keyinput[pygame.K_d] and self.rect.x <= screen_width - self.width:
            to_x = 10
            self.flip = False

        if keyinput[pygame.K_LSHIFT] and skill > 1500 and self.clicked == False:  # 고칠거
            audio[2].play()
            skill -= 1500
            self.y_vel = -30
            self.clicked = True

        if keyinput[pygame.K_s] and self.clicked == False:
            audio[5].play()
            blade = Blade(self.rect.x + (self.width / 2) - (self.width / 4), self.rect.y)
            blade_group.add(blade)

            self.clicked = True


        if event.type == pygame.KEYUP and self.clicked == True:
            self.clicked = False




        self.y_vel += gravity
        to_y += self.y_vel

        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + to_y, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.y_vel > 0:
                        if out == False:
                            if platform.spike == 1:
                                self.image = pygame.image.load(os.path.join(image_path, "fall.png")).convert_alpha()
                                self.image = pygame.transform.scale(self.image, (45, 45))
                                audio[3].play()
                                game_over = True

                            elif platform.broken == 1:
                                audio[4].play()
                                to_y = 0
                                self.y_vel = -20
                                platform.kill()

                            else:
                                audio[0].play()
                                to_y = 0
                                self.y_vel = -20




        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect.x, self.rect.y + to_y, self.width, self.height):
                game_over = True

        for e_blade in e_blade_group:
            if e_blade.rect.colliderect(self.rect.x, self.rect.y + to_y, self.width, self.height):
                game_over = True




        if self.rect.top <= scroll_thresh:
            if self.y_vel < 0:
                scroll = -to_y

        if self.rect.bottom >= screen_height - 50:
            audio[3].play()
            self.image = pygame.image.load(os.path.join(image_path, "fall.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (45, 45))
            game_over = True



        self.rect.x += to_x
        self.rect.y += to_y + scroll

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5 ))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving, spike, broken):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "wood.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, 10))
        self.spike = spike

        if self.spike == 1:
            self.image = pygame.image.load(os.path.join(image_path, "spike.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, 10))

        self.broken = broken

        if self.broken == 1:
            self.image = pygame.image.load(os.path.join(image_path, "broken.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, 10))


        self.moving = moving
        self.moving_counter = random.randint(0, 500)
        self.speed = random.randint(1, 2)
        self.direction = random.choice([-1, 1])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



    def update(self, scroll):
        if self.moving == 1:
            self.moving_counter += self.speed
            self.rect.x += self.direction

        if self.moving_counter >= 100 or self.rect.left < 0 or self.rect.right > screen_width:
            self.direction *= -1
            self.moving_counter = 0



        self.rect.y += scroll

        if self.rect.top > screen_height:
            self.kill()

class Blade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "blade.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.speed = 15
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global out
        self.rect.y -= self.speed

        if self.rect.top <= 0:
            self.kill()


        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect):
                enemy.kill()
                e_blade_group.empty()
                jumpy.y_vel = -30

        for e_blade in e_blade_group:
            if self.rect.colliderect(e_blade.rect):
                e_blade.kill()




class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, e_type):
        pygame.sprite.Sprite.__init__(self)
        self.e = e_type

        if self.e == 1:
            self.image = pygame.image.load(os.path.join(image_path, "enemy_3.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (45, 45))

        if self.e == 2:
            self.image = pygame.image.load(os.path.join(image_path, "enemy_2.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (45, 45))

        if self.e == 3:
            self.image = pygame.image.load(os.path.join(image_path, "enemy_1.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (45, 45))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice([-2, 2])
        self.speed = 2

    def update(self, scroll):
        global start_ticks

        if self.e == 1:

            self.rect.x += self.direction

            if self.rect.left < 0 or self.rect.right > screen_width:
                self.direction *= -1

        elif self.e == 2:

            self.rect.x += self.direction

            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

            if total_time - elapsed_time <= 0:
                e_blade = E_blade(self.rect.x + (self.rect.width / 2) - (self.rect.width / 4), self.rect.y)
                e_blade_group.add(e_blade)
                start_ticks = pygame.time.get_ticks()

            if self.rect.left < 0 or self.rect.right > screen_width:
                self.direction *= -1

        elif self.e == 3:

            if self.rect.x > jumpy.rect.x:
                self.rect.x -= self.speed

            if self.rect.x <= jumpy.rect.x:
                self.rect.x += self.speed

            if self.rect.y <= jumpy.rect.y:
                self.rect.y += self.speed

            if self.rect.y > jumpy.rect.y:
                self.rect.y -= self.speed

        self.rect.y += scroll

        if self.rect.top > screen_height:
            self.kill()


class E_blade(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, "enemy_3.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.speed = 10
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom <= 0:
            self.kill()




image_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\image")
sound_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\sound")

screen_width = 400
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("frog jump")

fps = 60
total_time = 10
clock = pygame.time.Clock()

gravity = 1
max_platforms = 10
max_enemy = 10
scroll_thresh = 200
scroll = 0
skill = 0
enemy_append = 0
s = False
out = False

start = True
game_over = False
restart = False

score = 0
high_score = 0

sk_img = pygame.image.load(os.path.join(image_path, "jump.png")).convert_alpha()
sk_img = pygame.transform.scale(sk_img, (25, 25))


sk_img_2 = pygame.image.load(os.path.join(image_path, "jump.png")).convert_alpha()
sk_img_2 = pygame.transform.scale(sk_img, (25, 25))


sk_img_3 = pygame.image.load(os.path.join(image_path, "jump.png")).convert_alpha()
sk_img_3 = pygame.transform.scale(sk_img, (25, 25))


#pygame.mixer.music.load(os.path.join(sound_path, "music.mp3"))
pygame.mixer.music.set_volume(30)
#pygame.mixer.music.play(-1, 0.0, )

audio = [pygame.mixer.Sound(os.path.join(sound_path, "jump.mp3")),
         pygame.mixer.Sound(os.path.join(sound_path, "super.mp3")),
         pygame.mixer.Sound(os.path.join(sound_path, "s_jump.mp3")),
         pygame.mixer.Sound(os.path.join(sound_path, "death.mp3")),
         pygame.mixer.Sound(os.path.join(sound_path, "broke.mp3")),
         pygame.mixer.Sound(os.path.join(sound_path, "throwing.mp3"))]


audio[0].set_volume(0.5)
audio[1].set_volume(1)
audio[2].set_volume(0.5)
audio[3].set_volume(0.5)
audio[4].set_volume(0.1)
audio[5].set_volume(0.3)

if os.path.exists('score.txt'):
    with open('score.txt', 'r')as file:
        high_score = int(file.read())
else:
    high_score = 0

white = (255, 255, 255)

jumpy = Player(screen_width // 2, screen_height - 200)
enemy = Enemy(0, 100, 1)
platform = Platform((screen_width / 2) - 25, screen_height - 150, 50, 0, 0, 0)
e_t = E_blade(0, 0)

total_time = 1
start_ticks = pygame.time.get_ticks()

platform_group = pygame.sprite.Group()
blade_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
e_blade_group = pygame.sprite.Group()

platform_group.add(platform)

font_small = pygame.font.SysFont('Bit Cheese10', 30)

def ending():
    global  restart, scroll, high_score
    restart = True
    font_1 = pygame.font.SysFont("arialrounded", 60)
    font_2 = pygame.font.SysFont("arialrounded", 40)
    message = font_1.render("Game Over", True, white)
    message_2 = font_2.render(f"score : {score}", True, white)
    message_3 = font_2.render("Please space key...", True, white)

    screen.blit(message, (50, 100))
    screen.blit(message_2, (100, 150))
    screen.blit(message_3, (30, 400))

    if score > high_score:
        high_score = score
        with open('score.txt', 'w')as file:
            file.write(str(high_score))

def display_score():
    global score
    over_1 = pygame.font.SysFont("arialrounded", 40)
    message = over_1.render(f" {score}", True, white)
    screen.blit(message, (5, 10))


running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            running = False

    if not restart:
        if len(platform_group) < max_platforms:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, screen_width - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(0, 100)
            if s == True:
                p_type = 0
                s = False

            if p_type in range(0, 35):
                platform = Platform(p_x, p_y, p_w, 0, 0, 0)
                platform_group.add(platform)

            elif p_type in range(36, 60) and score >= 500:
                platform = Platform(p_x, p_y, p_w, 0, 0, 1)
                platform_group.add(platform)


            elif p_type in range(61, 89) and score >= 2000:
                platform = Platform(p_x, p_y, p_w, 0, 1, 0)
                platform_group.add(platform)
                s = True


            elif p_type in range(90, 100) and score >= 1000:
                platform = Platform(p_x, p_y, p_w, 1, 0, 0)
                platform_group.add(platform)

        if len(enemy_group) == 0 and enemy_append >= random.randint(1000, 1700):

            if score >= 10000:
                enemy_append = 0
                for x in range(2):
                    enemy = Enemy(random.randint(0, screen_width - enemy.rect.width), -45, random.choice([1, 2, 3]))
                    enemy_group.add(enemy)



            if score >= 6000:
                enemy_append = 0
                enemy = Enemy(random.randint(0, screen_width - enemy.rect.width), -45, 3)
                enemy_group.add(enemy)

            elif score >= 3000:
                enemy_append = 0
                enemy = Enemy(random.randint(0, screen_width - enemy.rect.width), -45, 2)
                enemy_group.add(enemy)

            elif score >= 1000:
                enemy_append = 0
                enemy = Enemy(random.randint(0, screen_width - enemy.rect.width), -45, 1)
                enemy_group.add(enemy)



        enemy_append += scroll

        if scroll > 0:
            score += scroll
            skill += scroll

        if skill >= 4500:
            skill = 4500

        if score > 500:
            pass

        scroll = jumpy.move()

        screen.fill((121, 237, 255))

        display_score()

        platform_group.update(scroll)
        enemy_group.update(scroll)
        e_blade_group.update()
        blade_group.update()

        if skill >= 1500 and skill < 3000:
            screen.blit(sk_img, (screen_width - 30, 0))

        if skill >= 3000 and skill < 4500:
            screen.blit(sk_img, (screen_width - 30, 0))
            screen.blit(sk_img_2, (screen_width - 60, 0))

        if skill >= 4500 and skill < 6000:
            screen.blit(sk_img, (screen_width - 30, 0))
            screen.blit(sk_img_2, (screen_width - 60, 0))
            screen.blit(sk_img_3, (screen_width - 90, 0))

        pygame.draw.line(screen, white, (0, score - high_score + scroll_thresh),
                         (screen_width, score - high_score + scroll_thresh))

        best_message = font_small.render("best score!!!", True, white)
        screen.blit(best_message, (screen_width - 125, score - high_score + scroll_thresh))

        platform_group.draw(screen)
        blade_group.draw(screen)
        enemy_group.draw(screen)
        e_blade_group.draw(screen)
        jumpy.draw()

        if game_over:
            ending()

    else:

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            jumpy.image = pygame.image.load(os.path.join(image_path, "jump.png")).convert_alpha()
            jumpy.image = pygame.transform.scale(jumpy.image, (45, 45))

            game_over = False
            restart = False
            out = False

            score = 0
            scroll = 0
            skill = 0
            enemy_append = 0

            jumpy.rect.center = (screen_width // 2, screen_height - 250)

            platform_group.empty()
            blade_group.empty()
            enemy_group.empty()
            e_blade_group.empty()

            platform = Platform((screen_width / 2) - 25, screen_height - 200, 50, 0, 0, 0)
            platform_group.add(platform)


    pygame.display.update()

pygame.quit()