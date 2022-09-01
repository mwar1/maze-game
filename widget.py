import pygame
pygame.init()

class Widget(pygame.sprite.Sprite):
    ## A pygame Sprite object which is used to create a
    ## widget which the user can interact with
    def __init__(self, x, y, width, height):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def isClicked(self, mousex, mousey):
        ## Check if the widget has been clicked

        return self.rect.collidepoint(mousex, mousey)


class Button(Widget):
    ## A child class of Widget, which is used to create a button to allow
    ## the user to move between screens in the game
    def __init__(self, x, y, text, textColour, boxColour, fontSize, goTo, isText=False):
        self.textFont = pygame.font.Font("Fonts/font.ttf", fontSize)
        width, height = self.textFont.size(text)
        width += 10
        height += 10

        super().__init__(x, y, width, height)

        self.text = text
        self.textColour = textColour
        self.boxColour = boxColour
        self.activeColour = (self.boxColour[0]+50, self.boxColour[1]+50, self.boxColour[2]+50)
        self.goTo = goTo
        self.isText = isText

        ## Fill the background and render text  
        self.buttonText = self.textFont.render(self.text, False, self.textColour)
        self.image.fill(self.boxColour)
        self.image.blit(self.buttonText, (5, 5))

    def updateButton(self):
        ## Re-draw the button text and fill onto the image attribute

        ## Render the text for the button
        self.buttonText = self.textFont.render(self.text, False, self.textColour)
        self.image.fill(self.boxColour)
        self.image.blit(self.buttonText, (5, 5))

    def setActive(self, active):
        ## Change the colour of the button if the mouse is over it
        
        if active and not self.isText:
            self.image.fill(self.activeColour)
        else:
            self.image.fill(self.boxColour)
        self.image.blit(self.buttonText, (5, 5))


class Slider(Widget):
    ## A child class of Widget, which is used to create a slider which
    ## can change settings in the game
    def __init__(self, x, y, width, height, minValue, maxValue, currentValue, setting, bgColour, sliderColour, buttonColour, textColour):
        super().__init__(x, y, width, height)

        self.minValue = minValue
        self.maxValue = maxValue
        self.currentValue = currentValue
        self.setting = setting
        self.bgColour = bgColour
        self.sliderColour = sliderColour
        self.buttonColour = buttonColour
        self.textColour = textColour
        self.active = False

        self.textFont = pygame.font.Font("Fonts/font.ttf", int(self.height / 1.4))
        ## Get the width and height of the text needed to display the maximum value
        self.fontWidth, self.fontHeight = self.textFont.size("0" * len(str(self.maxValue)))

        ## Calculate the position of the button as a percentage of the overall width
        self.buttonPercentage = (self.currentValue - self.minValue) / (self.maxValue - self.minValue)

        ## Fill the background and draw the slider elements
        self.image.fill(self.bgColour)
        pygame.draw.rect(self.image, self.sliderColour, (10, self.height/2-4, self.width-20-self.fontWidth, 8))
        pygame.draw.ellipse(self.image, self.buttonColour, (int(self.buttonPercentage*(self.width-20-self.fontWidth-self.height)), 0, self.height, self.height))
        text = self.textFont.render(str(self.currentValue), False, self.textColour)
        self.image.blit(text, (self.width-self.fontWidth, self.height/2-self.fontHeight/2))

    def isClicked(self, mousex, mousey):
        ## Returns True if the slder button has been clicked, False if not

        ## Create a temporary object to represent the button
        buttonRect = pygame.rect.Rect(self.x+int(self.buttonPercentage*(self.width-10-self.fontWidth-self.height)), self.y, self.height, self.height)

        ## Check if the mouse is colliding with the button
        if buttonRect.collidepoint(mousex, mousey):
            self.active = True
        else:
            self.active = False

    def changeValue(self, mousex):
        ## Change the value of the slider, depending on the position of the mouse

        ## Get the position of the mouse relative to the slider
        relMouseX = mousex - self.x

        ## Check how far along the slider the mouse is
        if relMouseX <= 0:
            self.currentValue = self.minValue
        elif relMouseX >= self.width-10-self.fontWidth:
            self.currentValue = self.maxValue
        else:
            self.currentValue = int((relMouseX / (self.width-20-self.fontWidth)) * (self.maxValue - self.minValue)) + self.minValue

        ## Recalculate the button's position
        self.buttonPercentage = (self.currentValue - self.minValue) / (self.maxValue - self.minValue)

        ## Refresh the slider
        self.image.fill(self.bgColour)
        pygame.draw.rect(self.image, self.sliderColour, (10, self.height/2-4, self.width-20-self.fontWidth, 8))
        pygame.draw.ellipse(self.image, self.buttonColour, (int(self.buttonPercentage*(self.width-10-self.fontWidth-self.height)), 0, self.height, self.height))
        text = self.textFont.render(str(self.currentValue), False, self.textColour)
        self.image.blit(text, (self.width-self.fontWidth, self.height/2-self.fontHeight/2))

    def getValue(self):
        ## Return the current value of the slider

        return self.currentValue

class Textbox(Widget):
    ## A child class of Widget, used to create a textbox to allow the user to enter text input
    def __init__(self, x, y, width, height, bgColour, boxColour, textColour, fontSize):
        super().__init__(x, y, width, height)

        self.bgColour = bgColour
        self.boxColour = boxColour
        self.activeColour = (self.boxColour[0]-25, self.boxColour[1]-25, self.boxColour[2]-25)
        self.textColour = textColour
        self.fontSize = fontSize
        self.active = False

        ## Render the text as empty initially
        self.text = ""
        self.textFont = pygame.font.Font("Fonts/font.ttf", self.fontSize)
        ## Calculate the y co-ordinate to render the text at
        self.textStart = (self.height-10)/2-self.textFont.size("j")[1]/2
        self.renderedText = self.textFont.render(self.text, False, self.textColour)

        ## Create the button
        self.button = Button(0, 0, "Enter", self.textColour, self.bgColour, self.fontSize, 20)
        self.button.rect.x = self.width - self.button.width - 2
        self.button.rect.y = self.textStart

        ## Draw all parts of the Textbox
        self.redrawBox(boxColour)
        self.button.rect.height -= 2

    def redrawBox(self, boxColour):
        self.image.fill(self.bgColour)
        pygame.draw.rect(self.image, boxColour, (5, 5, self.width-self.button.width-15, self.height-10))
        self.image.blit(self.renderedText, (10, self.textStart))
        self.image.blit(self.button.image, self.button.rect)
        #pygame.draw.rect(self.image, self.boxColour, self.button.rect, 2, 15)
        pygame.draw.rect(self.image, self.boxColour, self.button.rect, 2)

    def addText(self, key):
        ## Add a letter to the text in the textbox

        ## Remove a letter if backspace is pressed
        if key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif len(self.text) < 10:
            ## Add the key to the text in the box
            self.text += chr(key)

        ## Re-render text and re-draw Textbox
        self.renderedText = self.textFont.render(self.text, False, self.textColour)

        self.redrawBox(self.activeColour)

    def isBoxClicked(self, mousex, mousey):
        ## Returns True if the box has been clicked, False if not

        box = pygame.rect.Rect(self.x, self.y, self.width-self.button.width-15, self.height-10)
        if box.collidepoint(mousex, mousey):
            self.redrawBox(self.activeColour)
            return True

        self.redrawBox(self.boxColour)
        return False

    def isButtonClicked(self, mousex, mousey):
        ## Returns True if the 'Enter' button has been clicked, False if not
        relMouseX = mousex - self.x
        relMouseY = mousey - self.y

        return self.button.rect.collidepoint(relMouseX, relMouseY)

    def getText(self, mousex, mousey):
        ## Return the text contained in the textbox

        return self.text
