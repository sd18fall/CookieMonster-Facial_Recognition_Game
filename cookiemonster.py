import numpy as np
import cv2
import random

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/home/ajensen/Downloads/haarcascade_frontalface_alt.xml') #find classifier
kernel = np.ones((21, 21), 'uint8')
mouth_y = [0,0] #initialize array for mouth y
mouth_x = [0,0] #initialize array for mouth x
mouth_open = False

class Model(object):
    """
    Attributes: cookie_list
    methods: eat
    """
    def __init__(self):
        self.cookies = []
        self.cookies.append(Cookies())

class Cookies(object):
    """
    Attributes: location, radius
    methods: rando_place (init)
    """
    def __init__(self):
        self.x= random.randint(0,400)
        self.y= random.randint(0,400)
        self.radius = random.randint(40,50)

class Person(object):
    """
    Controller for game
    Attributes: x, y, mouth_open
    """
    def __init__(self, x, y, open):
        self.x = x
        self.y = y
        self.open = mouth_open


class View:
    """blah"""
    def __init__(self, model):
        """
        Initialize the view with a reference to the model and the specified game screen dimensions (represented as a tuple containing the width and height
        """
        self.model = model


    def draw(self,frame):
        """
        Draw the current game state to the screen
        """

        #self.screen.fill(pygame.Color(0,0,0))
        for cookie in self.model.cookies:
            cv2.circle(frame,(cookie.x,cookie.y),(cookie.radius), (100,100,100))


if __name__ == '__main__':


    model = Model()

    view = View(model)


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        view.draw(frame)
        cv2.imshow('frame', frame)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 30))
        for (x, y, w, h) in faces:
            #frame[y:y+h, x:x+w, :] = cv2.dilate(frame[y:y+h, x:x+w, :], kernel)
            mouth_y = [int(y+4*h/5), int(y+3*h/4)]
            mouth_x = [int(x+w/4), int(x+3*w/4)]
            if (h>200):
                mouth_open = True
            else:
                mouth_open = False

            print(mouth_open)
            cv2.rectangle(frame, (mouth_x[0], mouth_y[0]), (mouth_x[1], mouth_y[1]), (0, 0, 255))

            # Display the resulting frame
            cv2.imshow('frame', frame)
            #for cookies in model
                #if cookie is in range of box
                    #destroy cookie
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break







    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
