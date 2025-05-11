from pygame import *
from random import randint
win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game.exe')
background = transform.scale(image.load('galaxy.jpg'),(win_width, win_height))

finish = False
clock = time.Clock()
run = True 
fps = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,saysx, saysy, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (saysx, saysy))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

x1=1
x2=1
y1=1
y2=1


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1


monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy('ufo.png', randint(40, 420),0 ,65, 65, 0.7)
    
    monsters.add(monster) 

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(40, 420),0 , 65, 65, 1)

    asteroids.add(asteroid)



score = 0 
lost = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)





fire_sound=mixer.Sound('fire.ogg')


ship = Player('rocket.png', 50, 520,65, 65, 5)

font.init()
font1 = font.SysFont("Arial", 36)
text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
font2 = font.SysFont("Arial", 36)

bullets = sprite.Group()

sprites_list = sprite.groupcollide(monsters, bullets, True, True)

win = font1.render('YOU WIN!' , True, (255, 255, 255))
lose = font1.render('YOU LOSE!' , True, (180,0,0))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key  == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background,(0, 0))
        ship.reset()
        bullets.draw(window)
        bullets.update()
        ship.update()
        monsters.update()
        asteroids.update()
        asteroids.draw(window)
        monsters.draw(window)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(40, 420),0 ,65, 65, randint(1, 2))
            monster.add(monsters)
        if score >= 30:  
                window.blit(win,(330,300))
                finish = True
        if lost >= 60:
                window.blit(lose,(330,300))
                finish = True
        text_lose = font2.render('Пропущено:' + str(lost), 1, (75, 0, 130))
        window.blit(text_lose,(10, 50))
        text_win = font2.render('Счёт:' + str(score), 1, (139, 0, 139))
        window.blit(text_win,(10, 30))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0 
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(30)
        for i in range(1,6):
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, 65, 65, 1)
            monsters.add(monster)
                
    
clock.tick(fps)
display.update()