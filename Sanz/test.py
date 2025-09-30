import pygame, os
pygame.init()

font_path = os.path.join("C:\\Users\\USER\\PycharmProjects\\pythonProject\\Sanz\\source\\font\\comicsans.ttf")
timer = pygame.time.Clock()
messages = ['Here we go',
           'hahaha']
myFont = pygame.font.Font("C:\\Users\\USER\\PycharmProjects\\pythonProject\\Sanz\\source\\font\\comicsans.ttf", 25)
snip = myFont.render("", True, (255, 255, 255))

screen = pygame.display.set_mode([800, 500])
counter = 0
speed = 30
active_message = 0
done = False

running = True
while running:
    message = messages[active_message]

    screen.fill((50, 50, 50))
    timer.tick(60)
    pygame.draw.rect(screen, (0, 0, 0), [0, 300, 800, 200])

    if counter < speed * len(message):
        counter += 1
    elif counter >= speed * len(message):

        if active_message >= len(messages) - 1:
            done = True
        else:
            active_message += 1
            counter = 0
            speed = 30


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    snip = myFont.render(message[0:int(counter//speed)], True, (255, 255, 255))
    screen.blit(snip, (0, 330))

    pygame.display.update()
pygame.quit()
