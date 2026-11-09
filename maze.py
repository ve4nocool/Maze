import pygame
pygame.mixer.init()
pygame.font.init()

class GS(pygame.sprite.Sprite):
    def __init__(self, fn, x, y, w, h, s):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(fn), (w,h))
        self.speed = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):    
        win.blit(self.image, self.rect)

class Player(GS):
    def update(self):
        ks = pygame.key.get_pressed()
        if ks[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x += self.speed
        if ks[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y += self.speed
        if ks[pygame.K_RIGHT] and self.rect.right < 700:
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x -= self.speed
        if ks[pygame.K_DOWN] and self.rect.bottom < 500:
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.y -= self.speed


class Enemy(GS):
    dr = 'left'
    def update(self,x1,x2):
        if self.dr == 'left':
            self.rect.x -= self.speed
        if self.dr == 'right':
            self.rect.x += self.speed
        if self.rect.left <= x1:
            self.dr = 'right'
        if self.rect.right >= x2:
            self.dr = 'left'

        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width):
        super().__init__()
        self.image = pygame.surface.Surface((width, height))
        self.image.fill((196, 227, 111))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):    
        win.blit(self.image, self.rect)


p = Player('hero.png', 40, 440, 50, 50, 5)
e = Enemy('cyborg.png', 630, 280, 50, 50, 3)
m = GS('treasure.png', 590, 390, 100, 100, 0)
w1 = Wall(100, 0, 400, 19)
w2 = Wall(200, 49, 401, 19)
w3 = Wall(300, 50, 400, 19)
w4 = Wall(400, 100, 400, 19)
w5 = Wall(400, 240, 19, 200)
w6 = Wall(200, 90, 19, 100)
w7 = Wall(540, 350, 150, 19)
w8 = Wall(600, 0, 19, 100)
w9 = Wall(681, 0, 100, 19)
fps = 60
win = pygame.display.set_mode(size=(700,500))
pygame.display.set_caption('Лабиринт')
bg = pygame.transform.scale(pygame.image.load('background.jpg'),(700,500))
c = pygame.time.Clock()
g = True
finish = False
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()
kick = pygame.mixer.Sound('kick.ogg')
money = pygame.mixer.Sound('money.ogg')
walls = pygame.sprite.Group()
walls.add(w1,w2,w3,w4,w5,w6,w7,w8,w9)
f1 = pygame.font.SysFont('Abadi',90).render('YOU WIN!',True,(255, 255, 0))
f2 = pygame.font.SysFont('Abadi',90).render('YOU LOSE!',True,(255, 255, 0))

def reset():
    global p, e, g, finish
    p = Player('hero.png', 40, 440, 50, 50, 5)
    e = Enemy('cyborg.png', 630, 280, 50, 50, 3)
    g = True
    finish = False

while g:
    win.blit(bg,(0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
    
    p.draw()
    e.draw()
    m.draw()
    walls.draw(win)
    
    if not finish:
        if pygame.sprite.collide_rect(p,m):
            win.blit(f1,(190,200))
            money.play()
            finish = True
        if pygame.sprite.collide_rect(p,e):
            win.blit(f2,(190,200))
            kick.play()
            finish = True
        e.update(430,690)
        p.update()
    pygame.display.update()
    c.tick(fps)