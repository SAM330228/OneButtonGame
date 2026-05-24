from pygame import *
from random import *
Finished = False
x = 700
y = 500
screen = display.set_mode((x,y))
display.set_caption('DinoRun')
background = transform.scale(image.load('clouds.png'),(x,y))
font.init()
font1 = font.SysFont('Arial', 36)
score = 0

mixer.init()
mixer.music.load('burmalda-fon.mp3')
mixer.music.play() #! имбулька-барабулька


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)
        self.velocity = 0 
        self.gravity = 0.6 
        self.jump_power = -10

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.y > 435:
            self.rect.y = 435
            self.velocity = 0

        keys = key.get_pressed()
        if (keys[K_SPACE]) and self.rect.y > 200:
            self.velocity = self.jump_power

class Wall(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)

    def spawn1(self):
        self.rect.x = randint(500,700) + 150
        self.rect.y = randint(200, 300)
    
    def spawn2(self):
        global score
        self.rect.x = randint(500,700) + 150
        self.rect.y = randint(400, 500)
        score = score + 1

    def update1(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.spawn1()

    def update2(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.spawn2()

Dinoss = Wall('Dinoss.png', randint(500, 700), randint(100, 150), 75, 75, randint(4, 15))
Square = Wall('square.png', 700, randint(450, 470), 75, 75, randint(4, 4))

Dino = Player('Pony.jpg', 100, 250, 50, 50, 50)

clock = time.Clock()
FPS = 60
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not Finished:

        screen.blit(background,(0,0))

        Dino.update()
        Dino.reset()

        Dinoss.update1()
        Dinoss.reset()

        Square.update2()
        Square.reset()

        draw.rect(screen, (0, 0, 255), Dinoss.rect, 2)
        draw.rect(screen, (0, 0, 255), Square.rect, 2)
        draw.rect(screen, (200, 0, 100), Dino.rect, 2)

        scored = font1.render(f"Счет: {score}", True, (200, 200, 200))
        screen.blit(scored, (10, 10))

        if sprite.collide_rect(Dino, Dinoss) or sprite.collide_rect(Dino, Square):
            Finished = True
    else:
        lose = font1.render("Вы проиграли", True, (128, 0, 0))
        screen.blit(lose, (x // 2 - 125, y // 2 - 50))

    display.update()
    clock.tick(FPS)
