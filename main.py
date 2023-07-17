import pygame
from random import randint
import sys

pygame.init()
screen = pygame.display.set_mode((620, 660))
pygame.display.set_caption('<<Snek>>')
font = pygame.font.SysFont('Menlo',20,True)

# pygame.mixer.init()
# mixer = pygame.mixer
# chomp = mixer.Sound('chomp.wav')
# mixer.music.load('theme.wav')
# mixer.music.play(-1)
class Snake():
    def __init__(self,x,y,rot,head=False):
        self.x = x
        self.y = y
        self.head = head
        self.rot = rot

    def move(self):
        if self.head:
            if self.rot == 'up':
                self.y-=20
            elif self.rot == 'down':
                self.y+=20
            elif self.rot == 'right':
                self.x+=20
            elif self.rot == 'left':
                self.x-=20
    def turn(self,dir):
        if self.head:
            if dir == 'up':
                if self.rot == 'right' or self.rot == 'left':
                    self.rot = 'up'
            elif dir == 'right':
                if self.rot == 'up' or self.rot == 'down':
                    self.rot = 'right'
            elif dir == 'left':
                if self.rot == 'up' or self.rot == 'down':
                    self.rot = 'left'
            elif dir == 'down':
                if self.rot == 'right' or self.rot == 'left':
                    self.rot = 'down'
    def draw(self,flick):
        pygame.draw.rect(screen,'white',(self.x,self.y,20,20))
        pygame.draw.rect(screen,'black',(self.x,self.y,20,20),2)

        if self.head:
            if self.rot == 'up':
                if flick == 5: pygame.draw.rect(screen,'red',(self.x+8,self.y-8,4,8))
                pygame.draw.rect(screen,'black',(self.x+5,self.y+5,3,3))
                pygame.draw.rect(screen,'black',(self.x+12,self.y+5,3,3))
            elif self.rot == 'down':
                if flick == 5: pygame.draw.rect(screen,'red',(self.x+8,self.y+20,4,8))
                pygame.draw.rect(screen,'black',(self.x+5,self.y+12,3,3))
                pygame.draw.rect(screen,'black',(self.x+12,self.y+12,3,3))
            elif self.rot == 'left':
                if flick == 5: pygame.draw.rect(screen,'red',(self.x-8,self.y+8,8,4))
                pygame.draw.rect(screen,'black',(self.x+5,self.y+5,3,3))
                pygame.draw.rect(screen,'black',(self.x+5,self.y+12,3,3))
            elif self.rot == 'right':
                if flick == 5: pygame.draw.rect(screen,'red',(self.x+20,self.y+8,8,4))
                pygame.draw.rect(screen,'black',(self.x+12,self.y+5,3,3))
                pygame.draw.rect(screen,'black',(self.x+12,self.y+12,3,3))
        else:
            if self.rot == 'up' or self.rot == 'down':
                pygame.draw.rect(screen,'black',(self.x+5,self.y+5,3,10))
                pygame.draw.rect(screen,'black',(self.x+12,self.y+5,3,10))
            elif self.rot == 'left' or self.rot == 'right':
                pygame.draw.rect(screen,'black',(self.x+5,self.y+12,10,3))
                pygame.draw.rect(screen,'black',(self.x+5,self.y+5,10,3))


class Food():
    def __init__(self):
        self.x = randint(1,29)*20
        self.y = randint(1,29)*20


    def draw(self):
        pygame.draw.rect(screen,'red',(self.x+4,self.y+4,13,13))


    def randomize(self,segments):
        satisfied = False
        segx = []
        segy = []
        for seg in segments:
            segx.append(seg.x)
            segy.append(seg.y)
        while satisfied == False:
            self.x = randint(1,29)*20
            self.y = randint(1,29)*20
            if self.x not in segx and self.y  not in segy:
                satisfied = True
        #chomp.play()


class SpecialFood():
    def __init__(self,x,y,segments):
        self.x = randint(1,29)*20
        self.y = randint(1,29)*20
        self.foodx = x
        self.foody = y
        self.timer = 1

        satisfied = False
        segx = [self.foodx]
        segy = [self.foody]
        for seg in segments:
            segx.append(seg.x)
            segy.append(seg.y)
        while satisfied == False:
            self.x = randint(1,29)*20
            self.y = randint(1,29)*20
            if self.x not in segx and self.y  not in segy:
                satisfied = True
    def draw(self):

        if self.timer < 300:
            #print(self.timer)
            self.timer+=1
        else:
            return False

        pygame.draw.rect(screen,'lightblue',(self.x,self.y,20,20))
        pygame.draw.rect(screen,'black',(self.x,self.y,20,20),1)

        return True



def addseg(segments):
    nx = ny = 0
    if segments[-1].rot == 'up':
        nx = segments[-1].x
        ny = segments[-1].y +20
    elif segments[-1].rot == 'down':
        nx = segments[-1].x
        ny = segments[-1].y -20
    elif segments[-1].rot == 'left':
        nx = segments[-1].x +20
        ny = segments[-1].y
    elif segments[-1].rot == 'right':
        nx = segments[-1].x -20
        ny = segments[-1].y

    segments.append(Snake(nx,ny,segments[-1].rot))


def main():
    print('Started..')
    #timers
    stimer = 0
    count = 1
    flick = 1
    #boolean
    turned = True
    sfoodexists = False
    score = 0
    special = 1
    #class instances
    head = Snake(320,320,'up',head=True)
    segments = [Snake(320,340,'up'),Snake(320,360,'up')]
    food = Food()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and turned == False:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    head.turn('up')
                    turned = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    head.turn('left')
                    turned = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    head.turn('right')
                    turned = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    head.turn('down')
                    turned = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.time.Clock().tick(60)
        screen.fill('black')
        for i in range(1,31):
            pygame.draw.line(screen,'#101010',(20*i,20),(20*i,600))
            pygame.draw.line(screen,'#101010',(20,20*i),(600,20*i))
        head.draw(flick)
        for segment in segments: segment.draw(flick)
        food.draw()
        pygame.draw.rect(screen,'white',(10,10,600,600),5)

        if count >= 6:
            x = head.x
            y = head.y
            rot = head.rot

            head.move()
            if head.x == food.x and head.y == food.y:
                if special > 5:
                    special = 1
                    sfood = SpecialFood(food.x,food.y,segments)
                    sfoodexists = True
                food.randomize(segments)
                addseg(segments)
                score+=1
                special+=1

            if head.x < 20:
                head.x = 580
            if head.x > 580:
                head.x = 20
            if head.y < 20:
                head.y = 580
            if head.y > 580:
                head.y = 20

            count = 0
            flick +=1
            if flick >= 6: flick = 1

            for i in range(len(segments)):
                x1 = segments[i].x
                y1 = segments[i].y
                rot1 = segments[i].rot

                segments[i].x = x
                segments[i].y = y
                segments[i].rot = rot

                x = x1
                y = y1
                rot = rot1
            turned = False
        else:
            count+=1

        if sfoodexists:
            sfoodexists = sfood.draw()
            if head.x == sfood.x and head.y == sfood.y:
                sfood.timer = 300
                score += 5

        score_label = font.render(f'Score = {score:<}',1,'white')
        score_rect = score_label.get_rect(topleft = (10,620))
        screen.blit(score_label,score_rect)


        high_label = font.render(f'Highscore = {high:<}',1,'white')
        high_rect = high_label.get_rect(topright = (610,620))
        screen.blit(high_label,high_rect)

        for seg in segments:
            if seg.x == head.x and seg.y == head.y:
                return score
        pygame.display.flip()


with open('Highscore.txt','r',) as f:
    high = int(f.read())
while True:
    score = main()
    if score > high:
        high = score
        with open('Highscore.txt','w',) as f:
            f.write(str(high))