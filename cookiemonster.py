import numpy as np
import cv2
import random
import pygame
from pygame.locals import *
import time

"""
TODO: Eat Cookies, create background,

"""

#mouth_y = [0,0] #initialize array for mouth y
#mouth_x = [0,0] #initialize array for mouth x
#mouth_open = False

class Model(object):
    """
    Attributes: cookie_list, player
    methods: update
    """
    def __init__(self, size):
        self.size = size
        self.cookies = Cookies()
        self.player = Player()
    def update(self):
        """ Update the game state (currently only tracking the cookies) """
        self.cookies.update()
        self.player.mouth.update()
        #if cookie is in mouth, eat it
        if self.cookies.x > self.player.mouth.x1 and self.cookies.x < self.player.mouth.x2 and self.cookies.y > self.player.mouth.y1 and self.cookies.y < self.player.mouth.y2:
            self.cookies.eat(self.player)

class Cookies(object):
    """
    Attributes: location, radius
    methods: rando_place (init)
    """
    def __init__(self):
        self.x= random.randint(100,500)
        self.y= 0
        self.radius = random.randint(40,50)
        self.velocity = 5.0
        self.speed = 3
        self.is_bomb=False
    def update(self):
        if self.y<800:
            self.y =int(self.y+ self.speed)
        else:
            self.y = 0
            rand=random.randint(0,5)
            if rand==1:
                self.is_bomb=True
            else:
                self.is_bomb=False
            self.x= random.randint(100,500)
            if self.speed<15:
                self.speed = self.speed * 1.2
    def eat(self, player):
        if self.is_bomb==True:
            self.speed = self.speed * 1.2
            player.lives-=1
        self.y=0

        self.x= random.randint(100,500)
        if player.lives >0:
            player.score+=1
        if self.speed<15:
            self.speed = self.speed * 1.2
        rand=random.randint(0,5)
        if rand==1:
            self.is_bomb=True

class Mouth(object):
    """Creates a mouth in the model"""
    def __init__(self, mouth_x1=0, mouth_y1=0, mouth_x2=0, mouth_y2=0):
        self.x1=mouth_x1
        self.y1=mouth_y1
        self.x2 = mouth_x2
        self.y2 = mouth_y2

    def update(self):
        ret, frame = cap.read()
        self.face_cascade = cv2.CascadeClassifier('/home/ajensen/Downloads/haarcascade_frontalface_alt.xml')
        self.faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 30))
        for (x, y, w, h) in self.faces:
            self.y1 = int(y+3*h/5)
            self.y2 = int(y+3*h/4)
            self.x1 = int(x+w/4)
            self.x2 = int(x+3*w/4)

class Player(object):
    """
    Player with score and whatnot
    """
    def __init__(self):
        self.score=0
        self.mouth=Mouth()
        self.lives=3

class View:
    """Display cookies on screen """
    def __init__(self, model, size):
        """
        Initialize the view with a reference to the model and the specified game screen dimensions (represented as a tuple containing the width and height
        """
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """
        Draw the current game state to the screen
        """
        monster = pygame.image.load('CookieMonster.png')
        cookie = pygame.image.load('cookie.png')
        bomb = pygame.image.load('Bomb.png')
        for i in range(size[0]):
            pygame.draw.line(self.screen,(i/8+40,i/20+20,i/7+70),(i,0),(i,size[1]))
        if self.model.player.score >= 0 and self.model.player.lives>0:

            self.screen.blit(monster, (self.model.player.mouth.x1-125,self.model.player.mouth.y1-150))

            #self.screen.fill(pygame.Color(255,150,100))
            if self.model.cookies.is_bomb == True:
                self.screen.blit(bomb, (self.model.cookies.x-50,self.model.cookies.y-50))
            else:
                self.screen.blit(cookie, (self.model.cookies.x-25,self.model.cookies.y-30))
            pygame.font.init() # you have to call this at the start,
                       # if you want to use this module.
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            textsurface = myfont.render('Score:' + str(self.model.player.score), False, (255, 255, 255))
            self.screen.blit(textsurface,(400,700))
            textsurface = myfont.render('Lives:' + str(self.model.player.lives), False, (255, 255, 255))
            self.screen.blit(textsurface,(400,750))
        else:
            for i in range(size[0]):
                pygame.draw.line(self.screen,(i/4+40,0,0),(i,0),(i,size[1]))

            pygame.font.init() # you have to call this at the start,
                       # if you want to use this module.
            myfont = pygame.font.SysFont('Comic Sans MS', 60)

            textsurface = myfont.render('GAME OVER. Score:' + str(self.model.player.score), False, (255, 255, 255))
            self.screen.blit(textsurface,(200,400))

        pygame.display.update()


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    kernel = np.ones((21, 21), 'uint8')
    pygame.init()
    size = (800, 800)
    model = Model(size)
    view = View(model,size)
    while True:
        view.draw()
        model.update()
        time.sleep(.001)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if model.player.lives==0:
            print ("YOU HAVE FAILED US!!")

    pygame.quit()
