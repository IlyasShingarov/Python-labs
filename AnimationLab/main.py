import pygame
import random
import math

WIDTH = 800
HEIGHT = 600


class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('AnimationLab\\images\\fish{}.png'.format(random.randint(1,6)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(80, 600), random.randint(130, 500))
        self.speed = random.randint(1,2)
        self.func = random.randint(0,2)
        
    def update(self):
        self.rect.x += self.speed
        if self.func == 0:
            self.rect.y -= math.cos(0.08 * self.rect.x) + math.cos(0.04 * self.rect.x) - 0.5
        elif self.func == 1:
            self.rect.y -= math.cos(0.08 * self.rect.x) - 0.5
        else:
            self.rect.y -= math.sin(0.08 * self.rect.x) - math.cos(0.04 * self.rect.x) - 0.5


        if self.rect.left > WIDTH:
            self.rect.right = 0
            self.rect.top = random.randint(130, 500)
            self.speed = random.randint(1,2)
            self.image = pygame.image.load('AnimationLab\\images\\fish{}.png'.format(random.randint(1,6)))

class Bubble_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('AnimationLab\\images\\bubble{}.png'.format(random.randint(1,4)))
        self.rect = self.image.get_rect()
        self.rect.center = (250 + random.randint(-10, 10),445)
        self.speed = random.randint(1,3)
        
    def update(self):
        self.rect.y -= self.speed
        self.rect.x += math.sin(0.008 * self.rect.y) - 0.5 * math.cos(0.008 * self.rect.y)
        if self.rect.top <= 0:
            self.rect.center = (250 + random.randint(-10, 10),445)
            self.speed = random.randint(10, 50)/20

class Bubble_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('AnimationLab\\images\\bubble{}.png'.format(random.randint(2,4)))
        self.rect = self.image.get_rect()
        self.rect.center = (400 + random.randint(-5, 5),475)
        self.speed = random.randint(10, 70)/20
        
    def update(self):
        self.rect.x += math.sin(0.008 * self.rect.y)
        self.rect.y -= self.speed
        if self.rect.top <= 0:
            self.rect.center = (400 + random.randint(-5, 5),475)
            self.speed = random.randint(10, 70)/20


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background_image = pygame.image.load('AnimationLab\\images\\background.jpg')
foreground_image = pygame.image.load('AnimationLab\\images\\background1.png')

fishes = pygame.sprite.Group()
back_bubbles = pygame.sprite.Group()
fore_bubbles = pygame.sprite.Group()


fish1 = Fish()
fish2 = Fish()
fish3 = Fish()


fore_bubble_1_1 = Bubble_1()
fore_bubble_1_2 = Bubble_1()
fore_bubble_1_3 = Bubble_1()
fore_bubble_1_4 = Bubble_1()
fore_bubble_1_5 = Bubble_1()
fore_bubble_1_6 = Bubble_1()

fore_bubble_2_1 = Bubble_2()
fore_bubble_2_2 = Bubble_2()
fore_bubble_2_3 = Bubble_2()
fore_bubble_2_4 = Bubble_2()
fore_bubble_2_5 = Bubble_2()
fore_bubble_2_6 = Bubble_2()

back_bubble_1_1 = Bubble_1()
back_bubble_1_2 = Bubble_1()
back_bubble_1_3 = Bubble_1()
back_bubble_1_4 = Bubble_1()
back_bubble_1_5 = Bubble_1()
back_bubble_1_6 = Bubble_1()

back_bubble_2_1 = Bubble_2()
back_bubble_2_2 = Bubble_2()
back_bubble_2_3 = Bubble_2()
back_bubble_2_4 = Bubble_2()
back_bubble_2_5 = Bubble_2()
back_bubble_2_6 = Bubble_2()




fishes.add(fish1, fish2, fish3)

fore_bubbles.add(fore_bubble_1_1, fore_bubble_1_2, fore_bubble_1_3, fore_bubble_1_4, fore_bubble_1_5, fore_bubble_1_6,
fore_bubble_2_1, fore_bubble_2_2, fore_bubble_2_3, fore_bubble_2_4, fore_bubble_2_5, fore_bubble_2_6)

back_bubbles.add(back_bubble_1_1, back_bubble_1_2, back_bubble_1_3, back_bubble_1_4, back_bubble_1_5, back_bubble_1_6,
back_bubble_2_1, back_bubble_2_2, back_bubble_2_3, back_bubble_2_4, back_bubble_2_5, back_bubble_2_6)


isOn = True
while isOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isOn = False

    screen.blit(background_image, (0, 0))
    back_bubbles.draw(screen)
    fishes.draw(screen)
    fore_bubbles.draw(screen)
    screen.blit(foreground_image, (0, 0))


    pygame.display.update()
    fishes.update()
    back_bubbles.update()
    fore_bubbles.update()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()