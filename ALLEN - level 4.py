import pygame
import random
pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('data/R1.png'), pygame.image.load('data/R2.png'), pygame.image.load('data/R3.png'), pygame.image.load('data/R4.png'), pygame.image.load('data/R5.png'), pygame.image.load('data/R6.png'), pygame.image.load('data/R7.png'), pygame.image.load('data/R8.png'), pygame.image.load('data/R9.png')]
walkLeft = [pygame.image.load('data/L1.png'), pygame.image.load('data/L2.png'), pygame.image.load('data/L3.png'), pygame.image.load('data/L4.png'), pygame.image.load('data/L5.png'), pygame.image.load('data/L6.png'), pygame.image.load('data/L7.png'), pygame.image.load('data/L8.png'), pygame.image.load('data/L9.png')]
bg = pygame.image.load('data/bg.jpg')
char = pygame.image.load('data/standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('data/bullet.mp3')
hitSound = pygame.mixer.Sound('data/hit.mp3')

music = pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(-1)

score = 0
life = 0
energy = 0
see = True

time_loop = pygame.USEREVENT + 1
class player(object):
    def __init__(self, x, y, width, height):
        global see
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.screenwidth = 500
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

        
    def draw(self, win):
        if see == True:
            if self.walkCount + 1 >= 27:
               self.walkCount = 0
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
            else:
            
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))

            self.hitbox = (self.x + 16.1, self.y + 11, 28.8, 52)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
                            
        
    def hit(self):
        see = False
        self.isJump = False
        self.jumpCount = 10
        #self.x = 10
        self.y = 405
        self.walkCount = 0
        
        if score >= 10:
            font1 = pygame.font.SysFont('comicsans', 100)
            text = font1.render('-10', 1, (255,0,0))
            win.blit(text, (250 - (text.get_width()/2),200))
            pygame.display.update()
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 101
                        pygame.quit()
                   


    

class projectile(object):
    def __init__(self, x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):         
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('data/R1E.png'), pygame.image.load('data/R2E.png'), pygame.image.load('data/R3E.png'), pygame.image.load('data/R4E.png'), pygame.image.load('data/R5E.png'), pygame.image.load('data/R6E.png'), pygame.image.load('data/R7E.png'), pygame.image.load('data/R8E.png'), pygame.image.load('data/R9E.png'), pygame.image.load('data/R10E.png'), pygame.image.load('data/R11E.png')]
    walkLeft = [pygame.image.load('data/L1E.png'), pygame.image.load('data/L2E.png'), pygame.image.load('data/L3E.png'), pygame.image.load('data/L4E.png'), pygame.image.load('data/L5E.png'), pygame.image.load('data/L6E.png'), pygame.image.load('data/L7E.png'), pygame.image.load('data/L8E.png'), pygame.image.load('data/L9E.png'), pygame.image.load('data/L10E.png'), pygame.image.load('data/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3.5
        self.hitbox = (self.x + 17, self.y + 2, 31, 52)
        self.health = 99
        self.visible = True

    def draw(self, win):
        self.move()
        
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,120,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.475 * (99 - self.health)), 10))
            if self.hitbox[2] > 100:
                pygame.draw.rect.color = (0,0,0)
            #self.hitbox = (self.x + 17, self.y + 2, 31, 52)
            self.hitbox = (self.x + 22, self.y + 11, 28, 52)
            
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            #if score > 99:
            #self.visible = False         
            self.y = 500
    
        

""" globlin 2 """
class enemy_2(object):
    walkRight = [pygame.image.load('data/R1E.png'), pygame.image.load('data/R2E.png'), pygame.image.load('data/R3E.png'), pygame.image.load('data/R4E.png'), pygame.image.load('data/R5E.png'), pygame.image.load('data/R6E.png'), pygame.image.load('data/R7E.png'), pygame.image.load('data/R8E.png'), pygame.image.load('data/R9E.png'), pygame.image.load('data/R10E.png'), pygame.image.load('data/R11E.png')]
    walkLeft = [pygame.image.load('data/L1E.png'), pygame.image.load('data/L2E.png'), pygame.image.load('data/L3E.png'), pygame.image.load('data/L4E.png'), pygame.image.load('data/L5E.png'), pygame.image.load('data/L6E.png'), pygame.image.load('data/L7E.png'), pygame.image.load('data/L8E.png'), pygame.image.load('data/L9E.png'), pygame.image.load('data/L10E.png'), pygame.image.load('data/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.end, self.x]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 52)
        self.visible = True
        self.health = 99

    def draw(self, win):
        self.move()
        
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,120,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.475 * (99 - self.health)), 10))
            if self.hitbox[2] > 100:
                pygame.draw.rect.color = (0,0,0)
            #self.hitbox = (self.x + 17, self.y + 2, 31, 52)
            self.hitbox = (self.x + 22, self.y + 11, 28, 52)
            
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1                
        else:
            #if score > 99:
            #self.visible = False
            self.y = 500
        if self.y == 500:
            energy = 50
    
""" globlin 3 """
class enemy_3(object):
    walkRight = [pygame.image.load('data/R1E.png'), pygame.image.load('data/R2E.png'), pygame.image.load('data/R3E.png'), pygame.image.load('data/R4E.png'), pygame.image.load('data/R5E.png'), pygame.image.load('data/R6E.png'), pygame.image.load('data/R7E.png'), pygame.image.load('data/R8E.png'), pygame.image.load('data/R9E.png'), pygame.image.load('data/R10E.png'), pygame.image.load('data/R11E.png')]
    walkLeft = [pygame.image.load('data/L1E.png'), pygame.image.load('data/L2E.png'), pygame.image.load('data/L3E.png'), pygame.image.load('data/L4E.png'), pygame.image.load('data/L5E.png'), pygame.image.load('data/L6E.png'), pygame.image.load('data/L7E.png'), pygame.image.load('data/L8E.png'), pygame.image.load('data/L9E.png'), pygame.image.load('data/L10E.png'), pygame.image.load('data/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.end, self.x]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 52)
        self.visible = True
        self.health = 99

    def draw(self, win):
        self.move()
        
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,120,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.475 * (99 - self.health)), 10))
            if self.hitbox[2] > 100:
                pygame.draw.rect.color = (0,0,0)
            #self.hitbox = (self.x + 17, self.y + 2, 31, 52)
            self.hitbox = (self.x + 22, self.y + 11, 28, 52)
            
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1                
        else:
            #if score > 99:
            #self.visible = False
            self.y = 500
        if self.y == 500:
            energy = 50
           
""" globlin 4 """
class enemy_4(object):
    walkRight = [pygame.image.load('data/R1E.png'), pygame.image.load('data/R2E.png'), pygame.image.load('data/R3E.png'), pygame.image.load('data/R4E.png'), pygame.image.load('data/R5E.png'), pygame.image.load('data/R6E.png'), pygame.image.load('data/R7E.png'), pygame.image.load('data/R8E.png'), pygame.image.load('data/R9E.png'), pygame.image.load('data/R10E.png'), pygame.image.load('data/R11E.png')]
    walkLeft = [pygame.image.load('data/L1E.png'), pygame.image.load('data/L2E.png'), pygame.image.load('data/L3E.png'), pygame.image.load('data/L4E.png'), pygame.image.load('data/L5E.png'), pygame.image.load('data/L6E.png'), pygame.image.load('data/L7E.png'), pygame.image.load('data/L8E.png'), pygame.image.load('data/L9E.png'), pygame.image.load('data/L10E.png'), pygame.image.load('data/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.end, self.x]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 52)
        self.visible = True
        self.health = 99

    def draw(self, win):
        self.move()
        
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,120,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (0.475 * (99 - self.health)), 10))
            if self.hitbox[2] > 100:
                pygame.draw.rect.color = (0,0,0)
            #self.hitbox = (self.x + 17, self.y + 2, 31, 52)
            self.hitbox = (self.x + 22, self.y + 11, 28, 52)
            
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)


    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1                
        else:
            #if score > 99:
            #self.visible = False
            self.y = 500
        if self.y == 500:
            energy = 50
            
                     
        
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('score: ' + str(score), 1, (0,0,0))
    win.blit(text, (380,10))
    man.draw(win)
    goblin.draw(win)
    goblin_2.draw(win)
    goblin_3.draw(win)
    goblin_4.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

  

#mainloop
font = pygame.font.SysFont('comicsans', 20, True)
man = player(210, 405, 64, 64)
goblin = enemy(0, 410, 64, 64, 450)
goblin_2 = enemy_2(350, 410, 64, 64, 0)
goblin_3 = enemy_3(200, 410, 64, 64, 0)
goblin_4 = enemy_4(400, 410, 64, 64, 200)
bullets = []
shootLoop = 0
run = True
while run:
    clock.tick(27)
    
    if goblin.y == 500:
        life = 50
        
    if goblin_2.y == 500:
        energy = 50
        
    
    """ if life == 50:
        print("boo yeah")
        
    if energy == 50:
        print("good") """
    
    if life == 50 and energy == 50:
        font2 = pygame.font.SysFont('comicsans', 70)
        text = font2.render('YOU WIN!', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        c = 0
        while c < 200:
            pygame.time.delay(10)
            c += 1 
            for event in pygame.event.get():                       
                c = 201
                pygame.quit()
                #run = True  
                    
    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] :
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                hitSound.play()
                random_number = random.randint(50, 100)
                man.x = (random.randint(30, 400))
                if score < 0:
                    times = score = 0
                    pygame.time.set_timer(times, 10)
                else:
                    if score > 0:
                        score -= 10
                        goblin.health += 10
                        if score < 0:
                            times = score = 0
                            pygame.time.set_timer(times, 10)
                
                
    
    if goblin_2.visible == True :
        if man.hitbox[1] < goblin_2.hitbox[1] + goblin_2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin_2.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin_2.hitbox[0] and man.hitbox[0] < goblin_2.hitbox[0] + goblin_2.hitbox[2]:
                man.hit()
                hitSound.play()               
                random_number = random.randint(50, 100)
                man.x = (random.randint(30, 400))
                if score < 0:
                    times = score = 0
                    pygame.time.set_timer(times, 10)
                else:
                    if score  > 0:
                        score -= 10   
                        goblin_2.health += 10
                        if score < 0:
                            times = score = 0         
                            pygame.time.set_timer(times, 10)    
                
    if goblin_3.visible == True :
        if man.hitbox[1] < goblin_3.hitbox[1] + goblin_3.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin_3.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin_3.hitbox[0] and man.hitbox[0] < goblin_3.hitbox[0] + goblin_3.hitbox[2]:
                man.hit()
                hitSound.play()               
                random_number = random.randint(50, 100)
                man.x = (random.randint(30, 400))
                if score < 0:
                    times = score = 0
                    pygame.time.set_timer(times, 10)
                else:
                    if score  > 0:
                        score -= 10   
                        goblin_3.health += 10
                        if score < 0:
                            times = score = 0         
                            pygame.time.set_timer(times, 10)    

    if goblin_4.visible == True :
        if man.hitbox[1] < goblin_4.hitbox[1] + goblin_4.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin_4.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin_4.hitbox[0] and man.hitbox[0] < goblin_4.hitbox[0] + goblin_4.hitbox[2]:
                man.hit()
                hitSound.play()               
                random_number = random.randint(50, 100)
                man.x = (random.randint(30, 400))
                if score < 0:
                    times = score = 0
                    pygame.time.set_timer(times, 10)
                else:
                    if score  > 0:
                        score -= 10   
                        goblin_4.health += 10
                        if score < 0:
                            times = score = 0         
                            pygame.time.set_timer(times, 10)  
                

                
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()   
                if score < 0:
                    score = 0
                else:
                    score += 1
                 
                bullets.pop(bullets.index(bullet))

        
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin_2.hitbox[1] + goblin_2.hitbox[3] and bullet.y + bullet.radius > goblin_2.hitbox[1]:
                if bullet.x + bullet.radius > goblin_2.hitbox[0] and bullet.x - bullet.radius < goblin_2.hitbox[0] + goblin_2.hitbox[2]:
                    hitSound.play()
                    goblin_2.hit()
                    if score < 0:
                        score = 0
                    else:
                        score += 1
                    
                    
                    bullets.pop(bullets.index(bullet))

            
            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        for bullet in bullets:
            if bullet.y - bullet.radius < goblin_3       .hitbox[1] + goblin_3       .hitbox[3] and bullet.y + bullet.radius > goblin_3       .hitbox[1]:
                if bullet.x + bullet.radius > goblin_3       .hitbox[0] and bullet.x - bullet.radius < goblin_3       .hitbox[0] + goblin_3       .hitbox[2]:
                    hitSound.play()
                    goblin_3       .hit()
                    if score < 0:
                        score = 0
                    else:
                        score += 1
                    
                    
                    bullets.pop(bullets.index(bullet))

            
            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        for bullet in bullets:
            if bullet.y - bullet.radius < goblin_4       .hitbox[1] + goblin_4       .hitbox[3] and bullet.y + bullet.radius > goblin_4       .hitbox[1]:
                if bullet.x + bullet.radius > goblin_4       .hitbox[0] and bullet.x - bullet.radius < goblin_4       .hitbox[0] + goblin_4       .hitbox[2]:
                    hitSound.play()
                    goblin_4       .hit()
                    if score < 0:
                        score = 0
                    else:
                        score += 1
                    
                    
                    bullets.pop(bullets.index(bullet))

            
            if bullet.x < 500 and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
    
        else:
            facing = 1
          
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

        shootLoop = 1
        
    
        
    if keys[pygame.K_LEFT] and man.x > man.vel:    
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        
    elif keys[pygame.K_RIGHT] and man.x < man.screenwidth - man.width - man.vel:    
         man.x += man.vel
         man.left = False
         man.right = True
         man.standing = False
    else:
         man.standing = True
         man.walkCount = 0
    if not (man.isJump):    
        #if keys[pygame.K_UP] and man.y > man.vel:    
            # man.y-= man.vel
        #if keys[pygame.K_DOWN] and man.y < man.screenwidth - man.height - man.vel:    
             #man.y += man.vel
        if keys[pygame.K_UP] :
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
            
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()

pygame.quit()
