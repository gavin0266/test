import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Moving Box")
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 255))


class Label(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = ""
        self.center = (320, 240)
                
    def update(self):
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class Square(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image = self.image.convert()
        self.image.fill((random.randrange(255),0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(20,620)
        self.rect.centery = -20
        self.dy = 1

    def update(self):
        self.rect.centery += self.dy


class Circle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (255, 0, 255), (25, 25), 25, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (300,200)
        
    def update(self):
        x,y = pygame.mouse.get_pos()
        self.rect.centerx = x

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,15))
        self.image = self.image.convert()
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 10
        self.rect.centery = 400
        self.dx = 0
        self.dy = -5

    def update(self):
        self.rect.centery += self.dy
            
class Box(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image = self.image.convert()
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = random.randrange(1,400)
        self.dx = 1
        self.dy = 0
        
    def update(self):
        self.rect.centerx += self.dx
        if self.rect.right > screen.get_width():
            self.rect.left = 0
        



bounce = False

def main():
    box = pygame.Surface((25,25))
    box.fill((255,0,0))
    boxes = Box()
    box2 = Box()
    x,y = pygame.mouse.get_pos()
    box_x = 0
    box_y = 200

    ammo = 30
    block = Box()
    bullet = Bullet()
    clock = pygame.time.Clock()
    keepGoing = True
    score = 0
    leveltimer = 200
    ammoTime = 0
    levelcount = 0
    levels = 1
    
    labelLevel = Label()
    labelLevel.text = "Level: %d" %levels
    labelLevel.center = (500, 50)
    
    label1 = Label()
    label1.text = "Score: %d" %score
    label1.center = (100,100)

    label2 = Label()
    label2.text = "Hi, I'm another label"
    label2.center = (500,100)
    circ = Circle()

    labelAmmo = Label()
    labelAmmo.center =(500,400)
    labelAmmo.text = "Ammo: %d" %ammo
    labelEvent = Label()
    labelEvent.center = (320, 400)
    labelCollide = Label()
    labelCollide.center = (300,100)
    collide_list = []
    bullet_list = []
    pygame.mouse.set_visible(False)
    allSprites = pygame.sprite.Group(labelLevel, labelAmmo, labelCollide, circ,label1,label2, labelEvent)
    block_list = pygame.sprite.Group()
    timeren = 0
    square = Square()
        
    
    while keepGoing:
        clock.tick(100)
        timeren += 1
        label1.text = "Score: %d" %score
        labelLevel.text = "Level: %d" %levels
        if timeren > leveltimer:
            square = Square()
            collide_list.append(square)
            allSprites.add(collide_list)
            timeren = 0
            levelcount += 1
            print levelcount
        if ammo < 1:
            ammoTime += 1
            labelEvent.text = "Reloading..."
            if ammoTime > 200:
                ammo += 5
                ammoTime = 0
                labelEvent.text = "..."
        if levelcount >= 10:
            levelcount = 0
            if leveltimer > 50:
                leveltimer -= 10
                print "Next Level..."
                levels += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                print "key pressed:", keyName
                labelEvent.text = "Key pressed: %s" %keyName
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    pygame.quit()
                """if event.key == pygame.K_r and ammo < 30:
                    if ammo > 27:
                        ammo = 30
                    else:
                        ammo += 3"""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ammo > 0:
                    bullet = Bullet()
                    x,y = pygame.mouse.get_pos()
                    bullet.rect.center = (x, 400)
                    allSprites.add(bullet)
                    bullet_list.append(bullet)
                    ammo -= 1
            elif event.type == pygame.MOUSEBUTTONUP:
                continue
            elif event.type == pygame.MOUSEMOTION:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                #labelEvent.text = 'mouse: (%d %d)' % (mouseX, mouseY)
                
        box_x += 0.5
        for d in collide_list:
            if pygame.sprite.collide_rect(circ, d):
                allSprites.remove(d)
                collide_list.remove(d)
                label2.text = "You're Dead"
                print 'dead'
            if d.rect.centery > 485:
                if ammo > 0:
                    ammo -= 1
                score -= 50
                allSprites.remove(d)
                collide_list.remove(d)
        if box_x > screen.get_width():
            box_x = 0
        if pygame.sprite.collide_rect(square, circ) == True:
            labelCollide.text = "collision"
            """block = Box()            
            block.rect.centerx = random.randrange(screen.get_width())
            colour = (random.randrange(255),random.randrange(255),random.randrange(255))
            block.image.fill(colour)
            block_list.add(block)
            allSprites.add(block)"""
        else:
            labelCollide.text = "No collision"
            circ.rect.center = (x,400)
        for n in bullet_list:
            for i in collide_list:
                if pygame.sprite.collide_rect(n, i):
                    score += 100
                    allSprites.remove(i)
                    collide_list.remove(i)
                    allSprites.remove(n)
                    bullet_list.remove(n)
                    ammo += random.randrange(1,3)
            if n.rect.centery < -50:
                allSprites.remove(n)

        labelAmmo.text = "Ammo: %d" %ammo
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
