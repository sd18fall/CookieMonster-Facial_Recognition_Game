import numpy as np
import cv2
import random
import pygame

"""
TODO: Eat Cookies, create background,

"""

cap = cv2.VideoCapture(0)
kernel = np.ones((21, 21), 'uint8')
mouth_y = [0,0] #initialize array for mouth y
mouth_x = [0,0] #initialize array for mouth x
mouth_open = False

class Model(object):
    """
    Attributes: cookie_list, player
    methods: update
    """
    def __init__(self):
        self.cookies = Cookies()
        self.player = Player()
    def update(self):
        """ Update the game state (currently only tracking the cookies) """
        self.cookies.update()
        self.player.mouth.recognize()
        #if mouth = cookie then cookie.eat

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
    def update(self):

        if self.y<800:
            self.y =int(self.y+ self.speed)
        else:
            self.y = 0
            self.x= random.randint(100,500)
            if self.speed<15:
                self.speed = self.speed * 1.2
    def eat(self, player):
        self.y=1000
        player.score+=1
        self.speed = self.speed * 1.2
        pass

class Bomb(Cookies):
    """
    Bomb
    """
    def eat(self, player):
        self.y=1000
        player.score-=10
        pass

class Mouth(object):
    """Creates a mouth in the model"""
    def __init__(self, mouth_x1=0, mouth_y1=0, mouth_x2=0, mouth_y2=0):
        self.x1=mouth_x1
        self.y1=mouth_y1
        self.x2 = mouth_x2
        self.y2 = mouth_y2
    def recognize(self):
        ret, frame = cap.read()
        self.face_cascade = cv2.CascadeClassifier('/home/ajensen/Downloads/haarcascade_frontalface_alt.xml')
        self.faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 30))
        for (x, y, w, h) in self.faces:
            self.y1 = int(y+4*h/5)
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
        for i in range(size[0]):
            pygame.draw.line(self.screen,(i/8+40,i/20+20,i/7+70),(i,0),(i,800))

        #self.screen.fill(pygame.Color(0,0,0))
        #pygame.circle(frame,(100,100,100),(self.model.cookies.x,self.model.cookies.y),(self.model.cookies.radius))
            #pygame.image('Cookie.png')

if __name__ == '__main__':
    pygame.init()
    size = (800, 800)
    model = Model()

    view = View(model,size)


    while True:
        # Capture frame-by-frame
        view.draw()
        model.update()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
