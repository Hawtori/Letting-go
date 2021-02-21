
import pyxel, enum, math


# add into somewhere later 
# if the player chooses to throw something away 
#pyxel.play(2, 1) #play sound track 7 on channel 1 - unlock room main melody
#pyxel.play(2, 1) #play sound track 0 on channel 1 - unlock room secondary melody  

# constants 
class Constants:
    MAX_X = 235
    MAX_Y = 147
    MIN_X = 14
    MIN_Y = 40

    CHARACTER_U = 1
    CHARACTER_V = 4
    CHARACTER_WIDTH = 14
    CHARACTER_HEIGHT = 24

    object_number = {"bear": 4, "book":0, "letter":2, "cage":3, "bottle":5, "violin":1}
     #book, violin, letter, birb, bear, bottle

# class for the character guy, handles what direction the guy is facing, and if he collides within an area for an object
class Player_Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    
    def draw(self, direction):
        """draw the guy lmao"""
        pass


# class for movement && direction for the guy 
class Direction(enum.Enum):
    """Sets value for each direction"""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# main class 
class Main:
    def __init__(self):
        pyxel.init(250, 160, caption="Letting go")

        # We can only import 3 images at a time. 
        # 0 will be the very back background 
        # 
        #pyxel.image(0).load(0, 0, "assets/pixelroomempty.png")
        pyxel.image(1).load(0, 0, "assets/character.png")
        pyxel.image(2).load(0, 0, "assets/pixelitems.png")

         #coordinates of interactables range
        self.coordinates = ((35, 119), (223, 92), (118, 112), (147, 37), (38, 38), (187, 141)) #book, violin, letter, birb, bear, bottle
        #width and height of each interactable
        self.uv = ((2, 1), (34, 2), (79, 12), (105, 4), (142, 7), (167, 10)) 
        self.wh = ((24, 32), (40, 46), (14, 14), (25, 31), (14, 21), (20, 23))
        #locations of each interactable on screen
        self.location = ((32, 117), (235, 92), (158, 121), (200, 44), (110, 25), (175, 70))


        #bool array for each item where true means we should put it on scren
        self.items = [True, True, True, True, True, True]

        #player positions
        self.pos_x = 150
        self.pos_y = 75
        self.dir = 1
        pyxel.mouse(True) #shows cursor on window


        self.play_music = True # lets background music play 
        if self.play_music: 
            pyxel.playm(0, loop = True)

        self.startScreen()
        


    def update(self):
        #get inputs for character
        if(pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A)):
            self.pos_x = max(self.pos_x - 2, Constants.MIN_X)
            self.dir = -1
        elif(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)):
            self.pos_x = min(self.pos_x + 2, Constants.MAX_X)
            self.dir = 1
        elif(pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W)):
            self.pos_y = max(self.pos_y - 2, Constants.MIN_Y)
        elif(pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)):
            self.pos_y = min(self.pos_y + 2, Constants.MAX_Y)

        self.collision()


    def collision(self):
        """check to see if the guy comes within 32pix of an object AND presses enter"""
        for i in self.coordinates:
            a = math.sqrt((self.pos_x - i[0]) ** 2 + (self.pos_y - i[1]) ** 2)
            if (a < 32 and (pyxel.btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.KEY_KP_ENTER))):
                print("is inside collision circle and has pressed enter") 
                #book, violin, letter, birb, bear, bottle

                if(i == 0): self.showObjectScreen("book")
                if(i == 1): self.showObjectScreen("violin")
                if(i == 2): self.showObjectScreen("letter")
                if(i == 3): self.showObjectScreen("cage")
                if(i == 4): self.showObjectScreen("bear")
                if(i == 5): self.showObjectScreen("bottle")

                #pyxel.play(2, 1) #play sound track 1 on channel 2 - object pickup noise 


    # might use this if we make constant bg music, but we dont have that as of rn 
    def toggleMusic(self):
        """toggles music on and off"""
        if self.play_music:
            self.play_music = False
            pyxel.stop() # tells pyxel to stop playing all sounds   
        else: 
            self.play_music = True


    def draw(self):
        """draws things on screen. look at Direction class for directions of main character"""
        pyxel.cls(0)  #clears screen
        pyxel.blt(0, 0, 0, 0, 0, 250, 160) #background image

        #draw circle if they are in range to interact with it
        for i in self.coordinates:
            a = math.sqrt((self.pos_x - i[0]) ** 2 + (self.pos_y - i[1]) ** 2)
            if (a < 32): pyxel.circb(i[0], i[1], 32, 1)

        #put items on the screen
        for i in range(5):
            if (self.items[i] == True):
                loc = self.location[i]
                uv = self.uv[i]
                wh = self.wh[i]
                pyxel.blt(loc[0] - ((uv[0] + wh[0])/2), loc[1] - ((uv[1] + wh[1])/2), 2, uv[0], uv[1], wh[0], wh[1], 0)

        #put character on the screen
        offsetX = (Constants.CHARACTER_U + Constants.CHARACTER_WIDTH) / 2
        offsetY = (Constants.CHARACTER_V + Constants.CHARACTER_HEIGHT) / 2
        if(self.dir == -1): pyxel.blt(self.pos_x - offsetX, self.pos_y - offsetY, 1, Constants.CHARACTER_U, Constants.CHARACTER_V, Constants.CHARACTER_WIDTH, Constants.CHARACTER_HEIGHT, 0)
        if(self.dir == 1): pyxel.blt(self.pos_x - offsetX, self.pos_y - offsetY, 1, Constants.CHARACTER_U, Constants.CHARACTER_V, -Constants.CHARACTER_WIDTH, Constants.CHARACTER_HEIGHT, 0)
            
    def removeBlue(self, grey_object):
        """remove specific blue tile from on top of room. argument is an int"""
        # remove a specific blue tile
        #pyxel.play(2, 1) #play sound track 7 on channel 1 - unlock room main melody
        #pyxel.play(2, 1) #play sound track 0 on channel 1 - unlock room secondary melody 


    def showObjectScreen(self, object_name):
        """show the screen with the object only. argument is a string"""
        # change image 0 then display it 
        pyxel.image(0).load(0, 0, "assets/is" + object_name + ".png") 
        while True:
            pyxel.blt(0, 0, 0, 0, 0, 250, 160)
            pyxel.flip()
            if(pyxel.btnp(pyxel.KEY_1)):
                self.items[Constants.object_number[object_name]] = False
                return
            if(pyxel.btnp(pyxel.KEY_2)):
                return


    def objectInterations(self, object_num):
        """function where player chooses what to do with the object. argument is an integer"""
        if pyxel.btnp(pyxel.KEY_1): # go back to room as it originally is 
            pass
        if pyxel.btnp(pyxel.KEY_2):
            self.removeBlue(object_num)
            

    def startScreen(self):
        """show the title screen"""
        # change image 0 then display it 
        flag = True
        while flag:
            pyxel.image(0).load(0, 0, "assets/startscreen.png")
            pyxel.blt(0, 0, 0, 0, 0, 250, 160)
            pyxel.flip()
            if(pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
                self.startButton()
                self.helpButton()
                self.exitButton()


    def mainScreen(self):
        """ show the main screen """
        # change image 0 then display it 
        pyxel.image(0).load(0, 0, "assets/pixelroomempty.png")
        pyxel.run(self.update, self.draw)


    def startButton(self):
        """starts the game when player presses start"""
        if ((91 <= pyxel.mouse_x <= 157) and  (61 <= pyxel.mouse_y <= 85) and (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON))):
            self.mainScreen() 


    def helpButton(self):
        """opens up the instruction page. tab to go back"""
        if ((92 <= pyxel.mouse_x <= 158) and (88 <= pyxel.mouse_y <= 111) and (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON))):
            while True:
            # change image 0 then display it 
                pyxel.image(0).load(0, 0, "assets/helpscreen.png")
                pyxel.blt(0, 0, 0, 0, 0, 250, 160)
                pyxel.flip()
                if pyxel.btnp(pyxel.KEY_TAB): 
                    self.startScreen()


    def exitButton(self):
        """quits game if player presses exit"""
        if ((92 <= pyxel.mouse_x <= 157) and (114 <= pyxel.mouse_y <= 142) and (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON))):
            pyxel.quit()


if __name__ == "__main__":
    Main()



#pyxel.blt(x, y, img(0-2), u, v, width, height) #put an image on screen
#pyxel.circ(x, y, 2, 7) #draws a circle at location (x, y) of radius 2, color 7