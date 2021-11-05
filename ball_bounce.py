#basic stuff
import pygame, sys, random

pygame.init()
window=pygame.display.set_mode((1500, 800), pygame.FULLSCREEN)
winrect=window.get_rect()

#colors
GREEN=(19, 225, 30)
BLUE=(41, 2, 245)
YELLOW=(251, 240, 32)
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
RED=(255, 0, 0)

#text
bigfont=pygame.font.SysFont('calibri', 75)
font=pygame.font.SysFont('calibri', 40)
texts={}

so=bigfont.render('Ball Bounce', True, BLUE)
rect=so.get_rect()
rect.top=winrect.top+100
rect.centerx=winrect.centerx
texts['title']=[so, rect]

so=font.render('Start', True, BLUE)
rect=so.get_rect()
so1=pygame.Surface((400, 50))
so2=pygame.Surface((400, 50))
rect1=so1.get_rect()
so1.fill(YELLOW)
so2.fill(RED)
pygame.draw.rect(so1, BLACK, rect1, 5)
pygame.draw.rect(so2, BLACK, rect1, 5)
rect.center=rect1.center
so1.blit(so, rect)
so2.blit(so, rect)
rect1.centerx=winrect.centerx
rect1.top=texts['title'][1].top+300
texts['start']=[so1, rect1, so2]

so=bigfont.render('Levels', True, BLUE)
rect=so.get_rect()
rect.centerx=winrect.centerx
rect.top=winrect.top+100
texts['levels']=[so, rect]

#levels [locked, unlocked, completed/mouseover, rect, state(locked, unlocked, completed)]
levels=[]
lock=pygame.image.load('apple.png').convert()
lock=pygame.transform.scale(lock, (100, 100))
lock.set_colorkey(lock.get_at((1, 1)))
for i in range(1, 21):
    so=pygame.Surface((100, 100))
    so.fill(YELLOW)
    rect=so.get_rect()
    pygame.draw.rect(so, BLACK, rect, 5)
    so1=pygame.Surface((100, 100))
    so1.fill(RED)
    pygame.draw.rect(so1, BLACK, rect, 5)
    text=font.render(str(i), True, BLUE)
    textrect=text.get_rect()
    textrect.center=rect.center
    so.blit(text, textrect)
    so1.blit(text, textrect)
    locked=pygame.Surface((100, 100))
    locked.blit(so, rect)
    locked.blit(lock, lock.get_rect())
    if i<=5:
        rect.top=texts['levels'][1].bottom+25
    elif i<=10:
        rect.top=levels[0][3].bottom+50
    elif i<=15:
        rect.top=levels[7][3].bottom+50
    else:
        rect.top=levels[12][3].bottom+50
    if i==1 or i==6 or i==11 or i==16:
        rect.right=winrect.centerx-200
    elif i==2 or i==7 or i==12 or i==17:
        rect.right=winrect.centerx-75
    elif i==3 or i==8 or i==13 or i==18:
        rect.centerx=winrect.centerx
    elif i==4 or i==9 or i==14 or i==19:
        rect.left=winrect.centerx+75
    else:
        rect.left=winrect.centerx+200
    if i==1:
        levels.append([locked, so, so1, rect, 1])
    else:
        levels.append([locked, so, so1, rect, 1])

#Wall class (0=horizontal, 1=vertical)
class cwall(pygame.Rect):
    'orientation (hor, vert), location, holesize, winrect'
    def __init__(self, orientation, location, holesize, winrect):
        self.orientation=orientation
        if orientation==0:
            self.height=5
            self.width=winrect.width
            self.centery=location
        if orientation==1:
            self.width=5
            self.height=winrect.height
            self.centerx=location
        self.holesize=holesize
        self.bbottomright=round(pygame.mouse.get_pos()[self.orientation]+self.holesize/2)
        self.ttopleft=round(pygame.mouse.get_pos()[self.orientation]-self.holesize/2)
    def update(self):
        self.bbottomright=round(pygame.mouse.get_pos()[self.orientation]+self.holesize/2)
        self.ttopleft=round(pygame.mouse.get_pos()[self.orientation]-self.holesize/2)
        if self.bbottomright<self.holesize:
            self.bbottomright=self.holesize
        if self.ttopleft>self.right-self.holesize and self.orientation==0:
            self.ttopleft=self.right-self.holesize
        if self.ttopleft>self.bottom-self.holesize and self.orientation==1:
            self.ttopleft=self.bottom-self.holesize

#Ball Class
class cball(pygame.Rect):
    'diameter, speed, color, winrect'
    def __init__(self, diameter, speed, color, winrect):
        self.width=diameter
        self.height=diameter
        self.speed=speed
        self.color=color
        self.direction=random.randint(1, 4)
        self.center=(random.randint(round(diameter/2), round(winrect.right-diameter/2)), random.randint(round(diameter/2), round(winrect.bottom-diameter/2)))
    def update(self, winrect, walls):
        if self.direction/2==round(self.direction/2):
            self.right+=self.speed
        else:
            self.right-=self.speed
        if self.direction<=2:
            self.top+=self.speed
        else:
            self.top-=self.speed
        for wall in walls:
            if wall.collidepoint(self.center):
                if wall.orientation==0 and (self.centerx<wall.ttopleft or self.centerx>wall.bbottomright):
                    if self.direction==1:
                        self.direction=3
                        self.bottom=wall.top
                    elif self.direction==2:
                        self.direction=4
                        self.bottom=wall.top
                    elif self.direction==3:
                        self.direction=1
                        self.top=wall.bottom
                    else:
                        self.direction=2
                        self.top=wall.bottom
                elif wall.orientation==1 and (self.centery<wall.ttopleft or self.centery>wall.bbottomright):
                    if self.direction==1:
                        self.direction=2
                        self.left=wall.right
                    elif self.direction==2:
                        self.direction=1
                        self.right=wall.left
                    elif self.direction==3:
                        self.direction=4
                        self.left=wall.right
                    else:
                        self.direction=3
                        self.right=wall.left
            elif wall.orientation==0:
                if self.bottom>wall.top and self.centery<wall.top and (self.centerx<wall.ttopleft or self.centerx>wall.bbottomright):
                    if self.direction==1:
                        self.direction=3
                        self.bottom=wall.top
                    elif self.direction==2:
                        self.direction=4
                        self.bottom=wall.top
                elif self.top<wall.bottom and self.centery>wall.bottom and (self.centerx<wall.ttopleft or self.centerx>wall.bbottomright):
                    if self.direction==3:
                        self.direction=1
                        self.top=wall.bottom
                    if self.direction==4:
                        self.direction=2
                        self.top=wall.bottom
            else:
                if self.left<wall.right and self.centerx>wall.right and (self.centery<wall.ttopleft or self.centery>wall.bbottomright):
                    if self.direction==1:
                        self.direction=2
                        self.left=wall.right
                    elif self.direction==3:
                        self.direction=4
                        self.left=wall.right
                elif self.right>wall.left and self.centerx<wall.left and (self.centery<wall.ttopleft or self.centery>wall.bbottomright):
                    if self.direction==2:
                        self.direction=1
                        self.right=wall.left
                    if self.direction==4:
                        self.direction=3
                        self.right=wall.left
        if self.top<0:
            if self.direction==3:
                self.direction=1
                self.top=0
            elif self.direction==4:
                self.direction=2
                self.topn=0
        if self.bottom>winrect.bottom:
            if self.direction==1:
                self.direction=3
                self.bottom=winrect.bottom
            elif self.direction==2:
                self.direction=4
                self.bottom=winrect.bottom
        if self.left<0:
            if self.direction==1:
                self.direction=2
                self.left=0
            elif self.direction==3:
                self.direction=4
                self.left=0
        if self.right>winrect.right:
            if self.direction==2:
                self.direction=1
                self.right=winrect.right
            if self.direction==4:
                self.direction=3
                self.right=winrect.right
        for box in boxes:
            if box[0].collidepoint(self.center) and self.color==box[1]:
                return True
        return False

#Game loop setup
mode='title'

#Game loop
while True:
    if mode=='title':
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if texts['start'][1].collidepoint(event.pos):
                    mode='levels'
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #screen update
        window.fill(GREEN)
        mouse=pygame.mouse.get_pos()
        if texts['start'][1].collidepoint(mouse):
            window.blit(texts['start'][2], texts['start'][1])
        else:
            window.blit(texts['start'][0], texts['start'][1])
        window.blit(texts['title'][0], texts['title'][1])
        pygame.display.update()

    elif mode=='levels':
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                for level in levels:
                    if level[3].collidepoint(event.pos) and level[4]!=0:
                        mode='loading'
                        loadinglevel=levels.index(level)+1
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        #screen update
        window.fill(GREEN)
        for level in levels:
            if level[3].collidepoint(pygame.mouse.get_pos()) and level[4]==1:
                window.blit(level[2], level[3])
            else:
                window.blit(level[level[4]], level[3])
        window.blit(texts['levels'][0], texts['levels'][1])
        pygame.display.update()

    elif mode=='loading':
        if loadinglevel==1:
            walls=[cwall(1, winrect.width/2, 100, winrect)]
            balls=[]
            for i in range(2):
                balls.append(cball(20, 3, GREEN, winrect))
            for i in range(2):
                balls.append(cball(20, 3, YELLOW, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/2), winrect.height), GREEN), (pygame.Rect(round(winrect.width/2), 0, round(winrect.width/2), winrect.height), YELLOW))
        elif loadinglevel==2:
            walls=[cwall(1, winrect.width/2, 100, winrect)]
            balls=[]
            for i in range(4):
                balls.append(cball(20, 3, GREEN, winrect))
            for i in range(4):
                balls.append(cball(20, 3, YELLOW, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/2), winrect.height), GREEN), (pygame.Rect(round(winrect.width/2), 0, round(winrect.width/2), winrect.height), YELLOW))
        elif loadinglevel==3:
            walls=[cwall(1, winrect.width/3, 100, winrect), cwall(1, 2*winrect.width/3, 100, winrect)]
            balls=[]
            for i in range(2):
                balls.append(cball(20, 3, GREEN, winrect))
            for i in range(2):
                balls.append(cball(20, 3, YELLOW, winrect))
            for i in range(2):
                balls.append(cball(20, 3, BLUE, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/3), winrect.height), GREEN), (pygame.Rect(round(winrect.width/3), 0, round(winrect.width/3), winrect.height), YELLOW),
                   (pygame.Rect(round(2*winrect.width/3), 0, round(winrect.width/3), winrect.height), BLUE))
        elif loadinglevel==4:
            walls=[cwall(1, winrect.width/3, 100, winrect), cwall(1, 2*winrect.width/3, 100, winrect)]
            balls=[]
            for i in range(4):
                balls.append(cball(20, 3, GREEN, winrect))
            for i in range(4):
                balls.append(cball(20, 3, YELLOW, winrect))
            for i in range(4):
                balls.append(cball(20, 3, BLUE, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/3), winrect.height), GREEN), (pygame.Rect(round(winrect.width/3), 0, round(winrect.width/3), winrect.height), YELLOW),
                   (pygame.Rect(round(2*winrect.width/3), 0, round(winrect.width/3), winrect.height), BLUE))

        elif loadinglevel==7:
            walls=[cwall(1, winrect.width/2, 100, winrect), cwall(0, winrect.height/2, 100, winrect)]
            balls=[]
            for i in range(2):
                balls.append(cball(20, 3, GREEN, winrect))
            for i in range(2):
                balls.append(cball(20, 3, YELLOW, winrect))
            for i in range(2):
                balls.append(cball(20, 3, BLUE, winrect))
            for i in range(2):
                balls.append(cball(20, 3, RED, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/2), round(winrect.height/2)), GREEN),
                   (pygame.Rect(0, round(winrect.height/2), round(winrect.width/2), round(winrect.height/2)), RED),
                   (pygame.Rect(round(winrect.width/2), 0, round(winrect.width/2), round(winrect.height/2)), YELLOW),
                   (pygame.Rect(round(winrect.width/2), round(winrect.height/2),  round(winrect.width/2), round(winrect.height/2)), BLUE))
        elif loadinglevel==8:
            walls=[cwall(1, winrect.width/2, 100, winrect), cwall(0, winrect.height/2, 100, winrect)]
            balls=[]
            for i in range(4):
                balls.append(cball(20, 3, GREEN, winrect))
            for i in range(4):
                balls.append(cball(20, 3, YELLOW, winrect))
            for i in range(4):
                balls.append(cball(20, 3, BLUE, winrect))
            for i in range(4):
                balls.append(cball(20, 3, RED, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/2), round(winrect.height/2)), GREEN),
                   (pygame.Rect(0, round(winrect.height/2), round(winrect.width/2), round(winrect.height/2)), RED),
                   (pygame.Rect(round(winrect.width/2), 0, round(winrect.width/2), round(winrect.height/2)), YELLOW),
                   (pygame.Rect(round(winrect.width/2), round(winrect.height/2),  round(winrect.width/2), round(winrect.height/2)), BLUE))
        elif loadinglevel==5:
            walls=[cwall(1, winrect.width/2, 100, winrect), cwall(0, winrect.height/2, 100, winrect)]
            balls=[]
            for i in range(10):
                balls.append(cball(20, 3, RED, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/2), round(winrect.height/2)), RED),
                   (pygame.Rect(0, round(winrect.height/2), winrect.width, round(winrect.height/2)), WHITE),
                   (pygame.Rect(round(winrect.width/2), 0, round(winrect.width/2), winrect.height), WHITE))
        elif loadinglevel==6:
            walls=[cwall(1, winrect.width/2, 100, winrect), cwall(0, winrect.height/2, 100, winrect)]
            balls=[]
            for i in range(20):
                balls.append(cball(20, 3, RED, winrect))
            boxes=((pygame.Rect(0, 0, round(winrect.width/2), round(winrect.height/2)), RED),
                   (pygame.Rect(0, round(winrect.height/2), winrect.width, round(winrect.height/2)), WHITE),
                   (pygame.Rect(round(winrect.width/2), 0, round(winrect.width/2), winrect.height), WHITE))
        mode='playing'
    elif mode=='playing':
        while True:
            #event loop
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            #updates
            updates=[]
            for wall in walls:
                wall.update()
            for ball in balls:
                updates.append(ball.update(winrect, walls))
            #Seeing if won
            won=True
            for update in updates:
                if not update:
                    won=False
                    break
            if won:
                if levels[loadinglevel][4]==0:
                    levels[loadinglevel][4]=1
                levels[loadinglevel-1][4]=2
                mode='levels'
                break
            #blitting
            window.fill(WHITE)
            for box in boxes:
                pygame.draw.rect(window, box[1], box[0])
            for wall in walls:
                if wall.orientation==0:
                    pygame.draw.rect(window, BLACK, (wall.left, wall.top, wall.ttopleft, wall.height))
                    pygame.draw.rect(window, BLACK, (wall.bbottomright, wall.top, wall.right-wall.bbottomright, wall.height))
                else:
                    pygame.draw.rect(window, BLACK, (wall.left, wall.top, wall.width, wall.ttopleft))
                    pygame.draw.rect(window, BLACK, (wall.left, wall.bbottomright, wall.width, wall.bottom-wall.holesize))
            for ball in balls:
                pygame.draw.circle(window, ball.color, ball.center, round(ball.width/2))
                pygame.draw.circle(window, BLACK, ball.center, round(ball.width/2), 2)
            pygame.display.update()
            pygame.time.Clock().tick(100)
