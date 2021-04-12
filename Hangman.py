import pygame, math, sys, random, time
from pygame.locals import *

#should automate finding the longesst width for all buttons based on longest text used

###########################################################

    # PABM ('TEXT', posx, posy, C_or_TL='center',
    #      fontsize=36, fixedtoright=False, fixedtobottom=False,
    #      fontcolor=WHITE, proportionalbuttonshape=False, completecoverage=False, buttonwidthx=0, buttonheighty=0,
    #      proportionalbuttonlocationx=False, proportionalbuttonlocationy=False, useimage=False,
    #      useborder=(1|2|3), blitted=False, buttonstate=(1|2), pressed=False)
    # True False #

###########################################################

pygame.init()

def mf(a):
    return math.floor(a)

class Pygamedisplay():
    def __init__(self, swidth, sheight):
        self.swidth = swidth
        self.sheight = sheight
    def return_swidth(self):
        return self.swidth
    def return_sheight(self):
        return self.sheight

class CentralizedVariable: #re-usable
    def __init__(self, var):
        self.var = var
        self.var_original = var * 1

    def increase_var(self, value=None):
        if type(self.var) == list:
            if value != None:
                self.var.append(value)
            else:
                raise Exception("Variable is not in list. Check your input.")
        elif type(self.var) != list:
            if value == None:
                self.var += 1
            else:
                raise Exception('Cannot use new value for non-list variable.')

    def decrease_var(self, value=None):
        if type(self.var) == list:
            if value != None and value in self.var:
                self.var.remove(value)
            else:
                #self.var = self.var[:-1]
                raise Exception("Variable is not in list. Check your input.")
        elif type(self.var) != list:
            if value == None:
                self.var -= 1
            else:
                raise Exception('Cannot use new value for non-list variable.')

    def append_to_list(self, value=None): # may be redundant
        if type(self.var) == list:
            if value != None:
                self.var.append(value)
            elif value == None:
                raise Exception("Check variable")
        else:
             raise Exception("Not for instance with non-list type")

    def remove_from_list(self, value=None): # may be redundant
        if type(self.var) == list:
            if value in self.var:
                self.var.remove(value)
            elif value == None:
                raise Exception('Check variable')
            elif value not in self.var:
                raise Exception('Check variable')

        else:
            raise Exception("Not for instance with non-list type")

    def return_var(self):
        return self.var

    def return_var_original(self):
        return self.var_original

    def return_var_len(self):
        return len(self.var)


class Phrase: #potentially re-usable
    def __init__(self, ANYTEXT, posx, posy, fontsize):
        self.ANYTEXT = ANYTEXT
        self.posx = posx
        self.posy = posy
        self.fontsize = fontsize

    def blit(self, newtext=''):
        if newtext != '':
            self.ANYTEXT = newtext
        basicfontx = pygame.font.SysFont('calibri', self.fontsize)
        #--------
        try:
            phrasex = basicfontx.render(self.ANYTEXT, 1, (240, 240, 240))
        except pygame.error:
            global inputa, storedtext1
            phrasex = basicfontx.render(None, 1, (240, 240, 240))
            inputa = storedtext1 = ''
        #--------
        phrasexrect = phrasex.get_rect()
        phrasexrect.centerx = self.posx; phrasexrect.centery = self.posy
        windowsurface.blit(phrasex, phrasexrect)
        return phrasexrect

    def blitwithbutton(self, N, S=0):
        basicfontx = pygame.font.SysFont('calibri', self.fontsize)
        #--------
        phrasex = basicfontx.render(self.ANYTEXT, 1, (255, 255, 255))
        #--------
        phrasexrect = phrasex.get_rect()
        #buttonrect = pygame.Rect(0, 0, mf(phrasexrect.width * 1.05), phrasexrect.height)

        if S == 0:
            #uttonrect = pygame.Rect(0, 0, mf((phrasexrect.width * 1.00)+(dimension1.return_swidth()*.03)), mf(dimension1.return_sheight()*.06)) #enough to fix?
            buttonrect = pygame.Rect(0, 0, 150, 30)

        elif S == 1:
            buttonrect = pygame.Rect(0, 0, 50, 30)

        elif S == 2:
            buttonrect = pygame.Rect(0, 0, mf(dimension1.return_swidth()*.1), mf(dimension1.return_sheight()*.06))


        if N == 1:
            phrasexrect.centerx = self.posx; phrasexrect.centery = self.posy
            buttonrect.centerx = self.posx; buttonrect.centery = self.posy

        elif N == 2:
            phrasexrect.left = self.posx + mf(buttonrect.width-phrasexrect.width-((buttonrect.width-phrasexrect.width)/2)); phrasexrect.centery = self.posy
            buttonrect.left = self.posx; buttonrect.centery = self.posy

        pygame.draw.rect(windowsurface, (120, 100, 12), buttonrect)
        windowsurface.blit(phrasex, phrasexrect)
        return buttonrect

class PABM():

    list_of_buttons = []
    WHITE = (255, 255, 255)
    GREEN = (22, 255, 22)
    CYAN = (22, 255, 255)
    RED = (255, 22, 22)
    GREY1 = (40, 40, 40)
    GREY2 = (20, 20, 20)
    BLACK = (0, 0, 0)
    #num = 0
    list_image = {}
    list_image_rect = {}
    imagetext = []

    def __init__(self, TEXT, posx=100, posy=100, C_or_TL='center',
                 fontsize=36, fixedtoright=False, fixedtobottom=False,
                 fontcolor=WHITE, proportionalbuttonshape=False, completecoverage=False, buttonwidthx=0, buttonheighty=0,
                 proportionalbuttonlocationx=False, proportionalbuttonlocationy=False, useimage='F',
                 useborder=1, blitted=False, buttonstate=1, pressed=False, keyboardmode=False, specificimage=''):

        PABM.list_of_buttons.append(self)
        self.TEXT = TEXT; self.C_or_TL = C_or_TL
        self.posx = posx; self.posy = posy
        self.buttonwidthx = buttonwidthx; self.buttonheighty = buttonheighty
        self.posx_original = posx; self.posy_original = posy; self.keyboardmode = keyboardmode
        self.originalscreenwidth = dimension1.return_swidth(); self.originalscreenheight = dimension1.return_sheight()
        self.fixedtoright = fixedtoright; self.fixedtobottom = fixedtobottom

        #translate xxxxx_True to True, xxxxx_False to False

        #takes in fontsize, creates phrase_rect
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fontsize_original = fontsize
        self.fontstyle = pygame.font.SysFont('calibri', self.fontsize)
        try:
            self.phrase = self.fontstyle.render(self.TEXT, 1, self.fontcolor)
        except:
            global inputa, storedtext1
            self.phrase = self.fontstyle.render(None, 1, self.fontcolor)
            inputa = storedtext1 = ''
        self.phrase_rect = self.phrase.get_rect()

        #-----
        self.buttoncolor1 = PABM.GREY1; self.buttoncolor2 = PABM.GREY2
        self.useimage = useimage; self.buttonstate = 1
        self.blitted = blitted
        self.pressed = pressed


        #get variable keep button location proportional in regards to any game screen size/ratio change
        if proportionalbuttonlocationx == True:
            self.proportionalbuttonlocationx = True
            self.proportionalbuttonlocationx_per = self.posx/dimension1.return_swidth() #ex: .10 or 10%
        else:
            self.proportionalbuttonlocationx = False
        if proportionalbuttonlocationy == True:
            self.proportionalbuttonlocationy = True
            self.proportionalbuttonlocationy_per = self.posy/dimension1.return_sheight()
        else:
            self.proportionalbuttonlocationy = False

        ##creates button_rect from scratch, then copy phrase_rect's features (prevents being changed by phrase_rect)
        self.button_rect = pygame.Rect(0,0,10,10)

        self.completecoverage = completecoverage


        if self.completecoverage == True:
            self.button_rect.width = mf(self.phrase_rect.width + buttonwidthx)
            self.button_rect.height = mf(self.phrase_rect.height + buttonheighty)

        #elif self.completecoverage == False: #make it temporary size
        #    self.button_rect.width = mf(self.phrase_rect.width)
        #    self.button_rect.height = mf(self.phrase_rect.height)
        elif self.completecoverage == False:
            self.button_rect.width = mf(self.buttonwidthx)
            self.button_rect.height = mf(self.buttonheighty)

        # self.button_rect.width = mf(self.phrase_rect.width + buttonwidthx)
        # self.button_rect.height = mf(self.phrase_rect.height + buttonheighty)


        self.button_rect_width_original = self.button_rect.width
        self.button_rect_height_original = self.button_rect.height

        #get variable to keep button shape proportional in regards to any game screen size/ratio change
        if proportionalbuttonshape == True:
            self.proportionalbuttonshape = True
            self.lockin_button_width_per = self.button_rect.width/dimension1.return_swidth() #ex: .10 or 10%
            self.lockin_button_height_per = self.button_rect.height/dimension1.return_sheight()
        else:
            self.proportionalbuttonshape = False

        #images for button state
        if self.useimage == 'T':
            self.imagebutton = pygame.image.load(r"C:\Users\patri\PycharmProjects\untitled\6\images_python_training\imagefu_button3.png")
            self.imagebutton = pygame.transform.scale(self.imagebutton, (self.button_rect.width, self.button_rect.height))
            self.imagebutton_original1 = self.imagebutton

            self.imagebutton = pygame.image.load(r"C:\Users\patri\PycharmProjects\untitled\6\images_python_training\imagefu_button7.png")
            self.imagebutton = pygame.transform.scale(self.imagebutton, (self.button_rect.width, self.button_rect.height))
            self.imagebutton_original2 = self.imagebutton

            # PABM.list_image.setdefault(len(PABM.list_image), self.imagebutton)
            # self.imagebutton_rect = self.imagebutton.get_rect()
            # PABM.list_image_rect.setdefault(len(PABM.list_image_rect), self.imagebutton_rect)

        #border
        self.useborder = useborder #1,2,3

    def blit_phraseandbutton(self, NEWTEXT=''):
        if NEWTEXT != '':
            self.TEXT = str(NEWTEXT)
            self.fontstyle = pygame.font.SysFont('calibri', self.fontsize)
            try:
                self.phrase = self.fontstyle.render(self.TEXT, 1, self.fontcolor)
            except:
                global inputa, storedtext1
                self.phrase = self.fontstyle.render(None, 1, self.fontcolor)
                inputa = storedtext1 = ''
            self.phrase_rect = self.phrase.get_rect()

        #for looping on certain buttons (in this case, loop on only buttons that have been blitted)
        self.blitted = True

        if self.keyboardmode == False:
            self.posx = self.posx_original; self.posy = self.posy_original
        else:
            self.proportionalbuttonshape = False; self.proportionalbuttonlocationx = False; self.proportionalbuttonlocationy= False

        #if self.completecoverage == True:
            #self.button_rect.width = mf(self.phrase_rect.width + self.buttonwidthx)
           # self.button_rect.height = mf(self.phrase_rect.height + self.buttonheighty)
        #elif self.completecoverage == False:
        #self.button_rect.width = mf(self.buttonwidthx)
        #self.button_rect.height = mf(self.buttonheighty)

        #updates x,y,w,h of button and phrase if game screen size changes

         #updates width and height of button
        if self.proportionalbuttonshape == True:
            self.button_rect.width = mf(self.lockin_button_width_per * dimension1.return_swidth())
            self.button_rect.height = mf(self.lockin_button_height_per * dimension1.return_sheight()) # * 1.65
        elif self.proportionalbuttonshape == False:
            pass #or write out the codes for width and height customization while game loop is running?


        #updates center/topleft x,y of button
        #try adding "if button on right side, keep button same distance toward right border"
        if self.proportionalbuttonlocationx == True:
            if self.C_or_TL == 'center':
                self.button_rect.centerx = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
            elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                self.button_rect.left = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
            elif self.C_or_TL == 'topright':
                self.button_rect.right = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())

        elif self.proportionalbuttonlocationx == False:
            if self.fixedtoright == True:
                if self.C_or_TL == 'center':
                    #self.button_rect.centerx = (dimension1.return_swidth() - mf(self.posx)) #ex: 100
                    self.button_rect.centerx = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx)) #ex: 700
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.button_rect.left = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))
                elif self.C_or_TL == 'topright':
                    self.button_rect.right = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))

            else:
                if self.C_or_TL == 'center':
                    self.button_rect.centerx = mf(self.posx)
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.button_rect.left = mf(self.posx)
                elif self.C_or_TL == 'topright':
                    self.button_rect.right = mf(self.posx)

        #
        if self.proportionalbuttonlocationy == True:
            if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                self.button_rect.centery = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
            elif self.C_or_TL == 'topleft':
                self.button_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
            elif self.C_or_TL == 'topright':
                self.button_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())

        elif self.proportionalbuttonlocationy == False:

            if self.fixedtobottom == True:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.button_rect.centery = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                elif self.C_or_TL == 'topleft':
                    self.button_rect.top = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                elif self.C_or_TL == 'topright':
                    self.button_rect.top = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))

            else:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.button_rect.centery = mf(self.posy)
                elif self.C_or_TL == 'topleft':
                    self.button_rect.top = mf(self.posy)
                elif self.C_or_TL == 'topright':
                    self.button_rect.top = mf(self.posy)

        #updates center/topleft x,y of phrase
        #okay to use proportionalbuttonlocationxy on phrase_rect
        if self.proportionalbuttonlocationx == True:

            if self.C_or_TL == 'center':
                self.phrase_rect.centerx = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
            elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                self.phrase_rect.left = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth()) + mf((self.button_rect.width-self.phrase_rect.width)/2)
            elif self.C_or_TL == 'topright':
                self.phrase_rect.right = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth()) - mf((self.button_rect.width-self.phrase_rect.width)/2)


        elif self.proportionalbuttonlocationx == False:

            if self.fixedtoright == True:
                if self.C_or_TL == 'center':
                    self.phrase_rect.centerx = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.phrase_rect.left = mf(dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))) + mf((self.button_rect.width-self.phrase_rect.width)/2)
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.right = mf(dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))) - mf((self.button_rect.width-self.phrase_rect.width)/2)

            else:
                if self.C_or_TL == 'center':
                    self.phrase_rect.centerx = mf(self.posx)
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.phrase_rect.left = mf(self.posx) + mf((self.button_rect.width-self.phrase_rect.width)/2)
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.right = mf(self.posx) - mf((self.button_rect.width-self.phrase_rect.width)/2)

        if self.proportionalbuttonlocationy == True:

            if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                self.phrase_rect.centery = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
            elif self.C_or_TL == 'topleft':
                self.phrase_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight()) + mf((self.button_rect.height-self.phrase_rect.height)/2)
            elif self.C_or_TL == 'topright':
                self.phrase_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight()) + mf((self.button_rect.height-self.phrase_rect.height)/2)

        elif self.proportionalbuttonlocationy == False:

            if self.fixedtobottom == True:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.phrase_rect.centery = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                elif self.C_or_TL == 'topleft':
                    self.phrase_rect.top = mf(dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))) + mf((self.button_rect.height-self.phrase_rect.height)/2)
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.top = mf(dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))) + mf((self.button_rect.height-self.phrase_rect.height)/2)

            else:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.phrase_rect.centery = mf(self.posy)
                elif self.C_or_TL == 'topleft':
                    self.phrase_rect.top = mf(self.posy) + mf((self.button_rect.height-self.phrase_rect.height)/2)
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.top = mf(self.posy) + mf((self.button_rect.height-self.phrase_rect.height)/2)

        if self.useimage == 'T':
            #reshape image surface if needed
            #-------------------------------
            if self.buttonstate == 1:
                if self.useborder == 1:
                    self.imagebutton = self.imagebutton_original1
                elif self.useborder == 2:
                    self.imagebutton = self.imagebutton_original1
                    pygame.draw.rect(windowsurface, (120,20,20), self.button_rect, 1)
                elif self.useborder == 3:
                    pygame.draw.rect(windowsurface, (120,20,20), self.button_rect, 1)


            elif self.buttonstate == 2:
                if self.useborder == 1:
                    self.imagebutton = self.imagebutton_original2
                elif self.useborder == 2:
                    self.imagebutton = self.imagebutton_original2
                    pygame.draw.rect(windowsurface, (20,120,20), self.button_rect, 1)
                elif self.useborder == 3:
                    pygame.draw.rect(windowsurface, (20,120,20), self.button_rect, 1)
            #-------------------------------

            if self.useimage == 'T':
                self.imagebutton = pygame.transform.scale(self.imagebutton, (self.button_rect.width, self.button_rect.height))
                #reshape image rect if needed
                self.imagebutton_rect = self.imagebutton.get_rect()
                self.imagebutton_rect.width = self.button_rect.width
                self.imagebutton_rect.height = self.button_rect.height
                self.imagebutton_rect.centerx = self.button_rect.centerx
                self.imagebutton_rect.centery = self.button_rect.centery


            if self.useborder != 3:
                windowsurface.blit(self.imagebutton, self.imagebutton_rect)
                windowsurface.blit(self.phrase, self.phrase_rect)
                return self.button_rect

            else:
                windowsurface.blit(self.phrase, self.phrase_rect)
                return self.button_rect

        elif self.useimage == 'F':
            if self.buttonwidthx == 0 and self.buttonheighty == 0: # temporary solution


                windowsurface.blit(self.phrase, self.phrase_rect)
                return self.button_rect
            else: #used to be without if and else, unindented
                #draw and blit, returns button_rect to work with collidepoint in a game loop
                #-------------------------------
                if self.buttonstate == 1:
                    if self.useborder == 1: #none
                        pygame.draw.rect(windowsurface, self.buttoncolor1, self.button_rect)
                    elif self.useborder == 2:
                        pygame.draw.rect(windowsurface, self.buttoncolor1, self.button_rect)
                        pygame.draw.rect(windowsurface, (120,20,20), self.button_rect, 1)
                    elif self.useborder == 3:
                        pygame.draw.rect(windowsurface, (120,20,20), self.button_rect, 1)

                elif self.buttonstate == 2:
                    if self.useborder == 1: #none
                        pygame.draw.rect(windowsurface, self.buttoncolor2, self.button_rect)
                    elif self.useborder == 2:
                        pygame.draw.rect(windowsurface, self.buttoncolor2, self.button_rect)
                        pygame.draw.rect(windowsurface, (20,120,20), self.button_rect, 1)
                    elif self.useborder == 3:
                        pygame.draw.rect(windowsurface, (20,120,20), self.button_rect, 1)


                #-------------------------------
                windowsurface.blit(self.phrase, self.phrase_rect)
                return self.button_rect

    #must create (okay without "text") once, then blit with desired text
    def blit_phrase_only(self, NEWTEXT=''):
        if NEWTEXT != '':
            self.TEXT = str(NEWTEXT)

        fontstyle = pygame.font.SysFont('calibri', self.fontsize)
        try:
            self.phrase = fontstyle.render(self.TEXT, 1, self.fontcolor)
        except:
            global inputa, storedtext1
            self.phrase = fontstyle.render(None, 1, self.fontcolor)
            inputa = storedtext1 = ''
        self.phrase_rect = self.phrase.get_rect()


        if self.proportionalbuttonlocationx == True:
            if self.C_or_TL == 'center':
                self.phrase_rect.centerx = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
            elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                self.phrase_rect.left = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
            elif self.C_or_TL == 'topright':
                self.phrase_rect.right = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())

        elif self.proportionalbuttonlocationx == False:
            if self.fixedtoright == True:
                if self.C_or_TL == 'center':
                    self.phrase_rect.centerx = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx)) #ex: 700
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.phrase_rect.left = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.right = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))

            else:
                if self.C_or_TL == 'center':
                    self.phrase_rect.centerx = mf(self.posx)
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.phrase_rect.left = mf(self.posx)
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.right = mf(self.posx)


        if self.proportionalbuttonlocationy == True:
            if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                self.phrase_rect.centery = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
            elif self.C_or_TL == 'topleft':
                self.phrase_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
            elif self.C_or_TL == 'topright':
                self.phrase_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())

        elif self.proportionalbuttonlocationy == False:

            if self.fixedtobottom == True:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.phrase_rect.centery = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                elif self.C_or_TL == 'topleft':
                    self.phrase_rect.top = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.top = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))

            else:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.phrase_rect.centery = mf(self.posy)
                elif self.C_or_TL == 'topleft':
                    self.phrase_rect.top = mf(self.posy)
                elif self.C_or_TL == 'topright':
                    self.phrase_rect.top = mf(self.posy)


        windowsurface.blit(self.phrase, self.phrase_rect)
        return self.phrase_rect #could this be better than self.phrasexrect (phrasexrect seems to just stick there) - wrong. actually you just keep self.blitted = False or don't add self.blitted. self.blitted=True seems to prevent the button from getting unblitted/deleted away
        #draw and blit, returns button_rect to work with collidepoint in a game loop

    #try using it under video resize codes
    def create_list_image_and_list_image_rect(self):

        self.list_image = {}
        self.list_image_rect = {}

        #must take in - consider adding more features:
        #
        #      buttonshape,
        #      useimage='T',
        #      useborder=(1|2|3), blitted=False, buttonstate=(1|2), pressed=False, keyboardmode=False)


        for a in PABM.imagetext: #creates a list
            self.an_image = pygame.image.load(a)

            if self.proportionalbuttonshape == True:
                self.an_image = pygame.transform.scale(self.an_image, (mf(self.lockin_button_width_per * dimension1.return_swidth()), mf(self.lockin_button_height_per * dimension1.return_sheight())))

            elif self.proportionalbuttonshape == False:
                self.an_image = pygame.transform.scale(self.an_image, (self.buttonwidthx, self.buttonheighty))


            self.an_image = self.an_image.convert_alpha()
            self.list_image.setdefault(len(self.list_image), self.an_image)


            self.an_image_rect = self.an_image.get_rect()

            if self.proportionalbuttonlocationx == True:
                if self.C_or_TL == 'center':
                    self.an_image_rect.centerx = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
                elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                    self.an_image_rect.left = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())
                elif self.C_or_TL == 'topright':
                    self.an_image_rect.right = mf(self.proportionalbuttonlocationx_per * dimension1.return_swidth())

            elif self.proportionalbuttonlocationx == False:
                if self.fixedtoright == True:
                    if self.C_or_TL == 'center':
                        self.an_image_rect.centerx = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx)) #ex: 700
                    elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                        self.an_image_rect.left = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))
                    elif self.C_or_TL == 'topright':
                        self.an_image_rect.right = dimension1.return_swidth() - (self.originalscreenwidth - mf(self.posx))

                else:
                    if self.C_or_TL == 'center':
                        self.an_image_rect.centerx = mf(self.posx)
                    elif self.C_or_TL == 'topleft' or self.C_or_TL == 'left':
                        self.an_image_rect.left = mf(self.posx)
                    elif self.C_or_TL == 'topright':
                        self.an_image_rect.right = mf(self.posx)

            if self.proportionalbuttonlocationy == True:
                if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                    self.an_image_rect.centery = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
                elif self.C_or_TL == 'topleft':
                    self.an_image_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())
                elif self.C_or_TL == 'topright':
                    self.an_image_rect.top = mf(self.proportionalbuttonlocationy_per * dimension1.return_sheight())

            elif self.proportionalbuttonlocationy == False:

                if self.fixedtobottom == True:
                    if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                        self.an_image_rect.centery = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                    elif self.C_or_TL == 'topleft':
                        self.an_image_rect.top = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))
                    elif self.C_or_TL == 'topright':
                        self.an_image_rect.top = dimension1.return_sheight() - (self.originalscreenheight - mf(self.posy))

                else:
                    if self.C_or_TL == 'center' or self.C_or_TL == 'left':
                        self.an_image_rect.centery = mf(self.posy)
                    elif self.C_or_TL == 'topleft':
                        self.an_image_rect.top = mf(self.posy)
                    elif self.C_or_TL == 'topright':
                        self.an_image_rect.top = mf(self.posy)

            self.list_image_rect.setdefault(len(self.list_image_rect), self.an_image_rect)


    def return_list_image(self):
        return self.list_image


    def return_list_image_rect(self):
        return self.list_image_rect

    @staticmethod
    def loop_hoveringoverbuttons():
        for a in PABM.list_of_buttons:
            if a.blitted == True: #ONLY for buttons that are blitted
                if a.blit_phraseandbutton().collidepoint(pygame.mouse.get_pos()):
                    a.buttonstate = 2
                else:
                    if a.pressed == False:
                        a.buttonstate = 1

    @staticmethod
    def loop_unblitandunpressall():
        for a in PABM.list_of_buttons:
            a.pressed = False
            a.blitted = False

    @staticmethod
    def loop_pressthatbutton():
        for X in PABM.list_of_buttons:
            if X.blitted == True:
                if X.blit_phraseandbutton().collidepoint(a.pos):
                    X.pressed = True
                    X.buttonstate = 2
                    #print('pressed = True, buttonstate = 2')
                    #print(X.TEXT, "X.TEXT")
                    return X.TEXT

    @staticmethod
    def loop_unpressthatbutton():
        for X in PABM.list_of_buttons:
            if X.blitted == True:
                if X.blit_phraseandbutton().collidepoint(a.pos):
                    X.pressed = False
                    X.buttonstate = 1
                    #print('pressed = False, buttonstate = 1')

qwerty = [a for a in '1234567890qwertyuiopasdfghjklzxcvbnm']

def keyboardmaker():
    #keyboard maker
    qwerty = [a for a in '1234567890qwertyuiopasdfghjklzxcvbnm']
    placex = 0 # set to 0 and will auto-center on any game screen width size
    placey = mf(dimension1.return_sheight() * .68) # starting y point from top of game screen to bottom of game screen
    buttonwidth = 48#mf(dimension1.return_swidth() / 15)
    buttonheight = 48#mf(dimension1.return_sheight() / 10)
    placex = buttonwidth/2
    gapx = 1.1
    gapy = 1.1

    # find row_1 width for row 1 centering - need code simplification here@@@@
    row_1_buttons_width = 0
    for a in qwerty[:qwerty.index('q')]:
        row_1_buttons_width += buttonwidth + ((buttonwidth * gapx) - buttonwidth)
    row_1_buttons_width -= ((buttonwidth * gapx) - buttonwidth)
    row_1_placex = (dimension1.return_swidth() - mf(row_1_buttons_width)) / 2
    #print(row_1_placex, "row_1_placex")

    # find row_2 width for row 2 centering
    row_2_buttons_width = 0
    for a in qwerty[qwerty.index('q'):qwerty.index('a')]:
        row_2_buttons_width += buttonwidth + ((buttonwidth * gapx) - buttonwidth)
    row_2_buttons_width -= ((buttonwidth * gapx) - buttonwidth)
    row_2_placex = (dimension1.return_swidth() - mf(row_2_buttons_width)) / 2
    #print(row_2_placex, "row_2_placex")

    # find row_3 width for row 3 centering
    row_3_buttons_width = 0
    for a in qwerty[qwerty.index('a'):qwerty.index('z')]:
        row_3_buttons_width += buttonwidth + ((buttonwidth * gapx) - buttonwidth)
    row_3_buttons_width -= ((buttonwidth * gapx) - buttonwidth)
    row_3_placex = (dimension1.return_swidth() - mf(row_3_buttons_width)) / 2
    #print(row_3_placex, "row_3_placex")

    # find row_4 width for row 4 centering
    row_4_buttons_width = 0
    for a in qwerty[qwerty.index('z'):]:
        row_4_buttons_width += buttonwidth + ((buttonwidth * gapx) - buttonwidth)
    row_4_buttons_width -= ((buttonwidth * gapx) - buttonwidth)
    row_4_placex = (dimension1.return_swidth() - mf(row_4_buttons_width)) / 2
    #print(row_4_placex, "row_4_placex")

    #keyboard maker
    placex += row_1_placex

    for a in qwerty:
        list_button.append({a: PABM(a, placex, placey, 'center',
                                    30, True, True,
                                    PABM.WHITE, False, False, buttonwidth, buttonheight,
                                    False, False, 'T',
                                    1, False, 1, False, True)})

        placex += mf(buttonwidth * gapx)
        if placex > dimension1.return_swidth() - (dimension1.return_swidth()*.1) or a == '0' or a == 'p' or a == 'l':
            placey += buttonheight * gapy
            placex = buttonwidth/2
        if a == '0':
            placex += row_2_placex
        elif a == 'p':
            placex += row_3_placex
        elif a == 'l':
            placex += row_4_placex # prob

def checkletter(inputa): #not re-usable
    print()

    #input added/inputamulti
    global missedtotal, missed, num, hidden_splitted
    inputamulti = [a for a in inputa]
    if ' ' in hidden_splitted:
        for a in inputamulti:
            if ' ' == a:
                inputamulti.remove(a)
    for a in inputamulti:
        if a in usedletters:
            inputamulti.remove(a)
    inputamulti = list({a for a in inputamulti})
    #print('inputamulti:',inputamulti)
    print('input added: '.ljust(20, " "), sorted(inputamulti))

    #correct letters/usedletters
    num += len(missed)
    missed = []
    for n in inputamulti:
        for n in [n.lower(), n.upper()]:
            if n in answer_splitted0:
                usedletters.append(n)
                for a in answer_splitted:
                    while n in answer_splitted:
                        answer_bank.append(n)
                        answer_splitted.remove(n)
                        while answer_bank != []:
                            for b in answer_bank:
                                for bb in answer_splitted0:
                                    if bb == b:
                                        hidden_splitted[answer_splitted0.index(bb)] = str(bb)
                                        answer_splitted0[answer_splitted0.index(bb)] = '*'
                                        answer_bank.remove(b)
                                        break
    for a in usedletters:
        if ' ' in a or '\n' in a:
            usedletters.remove(a)
    #print('usedletters: ',usedletters)
    print('correct letters: '.ljust(20, " "), sorted(usedletters))

    #incorrect letters/missedtotal
    for n in inputamulti:
        if n not in answer_splitted or n.upper() not in answer_splitted0_upper:
            if n not in answer_splitted and n.upper() not in answer_splitted0_upper and n != ' ' and n != '\n':
                if n not in missedtotal:
                    missedtotal.append(n)
                    missed.append(n)
    missedtotal = list({a for a in missedtotal})
    #print('missedtotal: ',missedtotal)
    print('incorrect letters: '.ljust(20, " "), sorted(missedtotal))



def turn_all_game_loops_to_false():
    global loop_main_menu, loop_setup, loop_play, loop_gameover, loop_setting
    loop_main_menu = False
    loop_setup = False
    loop_play = False
    loop_gameover = False
    loop_setting = False

def save():
    textfile3 = open(r"Hangman Resources\textfile_active.txt", 'w')
    for a in A1.return_var():
        textfile3.write(a)
        textfile3.write('\n')
    textfile3.close()

    textfile4 = open(r"Hangman Resources\textfile_inactive.txt", 'w')
    for a in A2.return_var():
        textfile4.write(a)
        textfile4.write('\n')
    textfile4.close()

######################################################
# get a list (of answer keywords) from textfile2
textfile3 = open(r"Hangman Resources\textfile_active.txt", 'r')
listy0 = []
for a in textfile3.readlines():
    if '\n' in a:
        listy0.append(a[:-1])
    elif '\n' not in a:
        listy0.append(a)
textfile3.close()
# centralized variable init
#print(listy0)
A1 = CentralizedVariable(listy0)

######################################################
textfile4 = open(r"Hangman Resources\textfile_inactive.txt", 'r')
listy2 = []
for a in textfile4.readlines():
    if '\n' in a:
        listy2.append(a[:-1])
    elif '\n' not in a:
        listy2.append(a)
textfile4.close()
# centralized variable init (stores deleted text)
#print(listy2)
A2 = CentralizedVariable(listy2)

######################################################
maxround = CentralizedVariable(4)
maxattempt = CentralizedVariable(7)

######################################################
dimension1 = Pygamedisplay(800, 600)
windowsurface = pygame.display.set_mode((dimension1.return_swidth(), dimension1.return_sheight()),pygame.RESIZABLE)

midwidth = mf(dimension1.return_swidth())
midheight = mf(dimension1.return_sheight())

######################################################
button_title = PABM('Hangman', midwidth/2, midheight*.3, 'center',
80, False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'T',
1, False, 1, False)

button_bypatrickdlr = PABM('by Patrick DLR', midwidth/2, midheight*.4, 'center',
24, False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'T',
1, False, 1, False)

button_play = PABM('Play', midwidth/2, midheight*.6, 'center',
30, False, False,
PABM.WHITE, False, False, 250, 50,
True, True, 'T',
1, False, 1, False)

button_resume = PABM('Resume', midwidth/2, midheight*.6, 'center',
30, False, False,
PABM.WHITE, False, False, 250, 50,
True, True, 'T',
1, False, 1, False)

button_setting = PABM('Setting', midwidth/2, midheight*.7, 'center',
30, False, False,
PABM.WHITE, False, False, 250, 50,
True, True, 'T',
1, False, 1, False)

button_quit = PABM('Quit', 10, 383, 'topleft',
30, False, True,
PABM.WHITE, False, False, 100, 50,
False, False, 'F',
1, False, 1, False)

button_quit2 = PABM('Main Menu', 10, 10, 'topleft',
30, False, False,
PABM.WHITE, False, False, 160, 50,
False, False, 'F',
1, False, 1, False)


button_quit3 = PABM('Main Menu', midwidth/2, midheight*.7, 'center',
30, False, False,
PABM.WHITE, False, False, 250, 50,
True, True, 'T',
1, False, 1, False)

button_pause = PABM('Pause', midwidth-10, 383, 'topright',
30, True, True,
PABM.WHITE, False, False, 100, 50,
False, False, 'F',
1, False, 1, False)

button_back = PABM('Back', 10, 10, 'topleft',
30, False, False,
PABM.WHITE, False, False, 100, 50,
False, False, 'F',
1, False, 1, False)

####
button_save = PABM('Save', 10, 70, 'topleft',
30, False, False,
PABM.WHITE, False, False, 100, 50,
False, False, 'F',
1, False, 1, False)

button_saved = PABM('Saved!', 135, 70, 'topleft',
30, False, False,
PABM.GREEN, False, False, 100, 50,
False, False, 'F',
3, False, 1, False)

phrase_roundspergame = PABM('Rounds per game', midwidth*.15, midheight*.4, 'left',
36, False, False,
PABM.WHITE, False, True, 0, 0,
True, True, 'F',
1, False, 1, False)

phrase_roundspergame_X = PABM(str(maxround.return_var()), midwidth*.6, midheight*.4, 'center',
36, False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'F',
1, False, 1, False)

phrase_attemptsperround = PABM('Attempts per round', midwidth*.15, midheight*.5, 'left',
36, False, False,
PABM.WHITE, False, True, 0, 0,
True, True, 'F',
1, False, 1, False)

phrase_attemptsperround_X = PABM(str(maxattempt.return_var()), midwidth*.6, midheight*.5, 'center',
36, False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'F',
1, False, 1, False)

##issue
phrase_listofwords = PABM('List of words', midwidth*.15, midheight*.6, 'left',
36, False, False,
PABM.WHITE, False, True, 0, 0,
True, True, 'F',
1, False, 1, False)



phrase_listofwords_X = PABM(str(len(A1.return_var())), midwidth*.6, midheight*.6, 'center',
36, False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'F',
1, False, 1, False)

button_up1 = PABM('↑', midwidth*.7, midheight*.4, 'center',
36, False, False,
PABM.WHITE, False, False, 48, 48,
True, True, 'T',
1, False, 1, False)

button_down1 = PABM('↓', midwidth*.8, midheight*.4, 'center',
36, False, False,
PABM.WHITE, False, False, 48, 48,
True, True, 'T',
1, False, 1, False)

button_up2 = PABM('↑', midwidth*.7, midheight*.5, 'center',
36, False, False,
PABM.WHITE, False, False, 48, 48,
True, True, 'T',
1, False, 1, False)

button_down2 = PABM('↓', midwidth*.8, midheight*.5, 'center',
36, False, False,
PABM.WHITE, False, False, 48, 48,
True, True, 'T',
1, False, 1, False)
####

button_expand = PABM('Expand', midwidth*.75, midheight*.6, 'center',
36, False, False,
PABM.WHITE, False, False, 130, 48,
True, True, 'T',
1, False, 1, False)

button_textfield1 = PABM('', midwidth*.5, midheight*.7, 'center',
36, False, False,
PABM.WHITE, True, False, 400, 48,
True, True, 'F',
3, False, 1, False)

button_up4 = PABM('↑', 413, 480, 'center',
24, False, False,
PABM.WHITE, True, False, 30, 30,
True, True, 'F',
1, False, 1, False)

button_down5 = PABM('↓', 413, 570, 'center',
24, False, False,
PABM.WHITE, True, False, 30, 30,
True, True, 'F',
1, False, 1, False)

button_up6 = PABM('↑', 605, 480, 'center',
24, False, False,
PABM.WHITE, True, False, 30, 30,
True, True, 'F',
1, False, 1, False)

button_down7 = PABM('↓', 605, 570, 'center',
24, False, False,
PABM.WHITE, True, False, 30, 30,
True, True, 'F',
1, False, 1, False)

button_playagain = PABM('Play again', midwidth/2, midheight*.6, 'center',
30, False, False,
PABM.WHITE, False, False, 250, 50,
True, True, 'T',
1, False, 1, False)

phrase_gameover = PABM('GAME OVER', midwidth/2, midheight*.2, 'center',
48, False, False,
PABM.RED, False, False, 0, 0,
True, True, 'T',
1, False, 1, False)

phrase_yourscore = ''

phrase_playagain = PABM('Play again?', midwidth/2, midheight*.4, 'center',
30, False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'T',
1, False, 1, False)

#to be updated in-game loop, no blitted=True
phrase_correctletters = PABM(' ', 216, 366, 'center',
24, False, True,
PABM.WHITE, False, False, 0, 0,
False, False, 'F',
1, False, 1, False)

#to be updated in-game loop, no blitted=True
phrase_incorrectletters = PABM(' ', 584, 366, 'center',
24, False, True,
PABM.WHITE, False, False, 0, 0,
False, False, 'F',
1, False, 1, False)
#starter tick


    #reference
    # PABM ('TEXT', posx, posy, C_or_TL='center',
    #      fontsize=36, fixedtoright=False, fixedtobottom=False,
    #      fontcolor=WHITE, proportionalbuttonshape=False, completecoverage=False, buttonwidthx=0, buttonheighty=0,
    #      proportionalbuttonlocationx=False, proportionalbuttonlocationy=False, useimage='F',
    #      useborder=(1|2|3), blitted=False, buttonstate=(1|2), pressed=False, keyboardmode=False)
    # True False #


# add pictures to list (using PABM)
for a in range(8):
    a = a + 0
    #text = str(r"C:\Users\patri\OneDrive\Pictures\Hangman Resources\h" + str(a) + ".jpg")
    text = str(r"Hangman Resources\h" + str(a) + ".jpg")
    PABM.imagetext.append(text) #new way

# define size, x, y, and stuffs
PicturePABM1 = PABM(' ', 150, 168, 'center',
40 , False, True,
PABM.WHITE, False, False, 300, 370,
True, True, 'F',
1, False, 1, False)

PicturePABM2 = PABM(' ', 650, 168, 'center',
40 , False, True,
PABM.WHITE, False, False, 300, 370,
True, True, 'F',
1, False, 1, False)

# return lists for blitting (pictures from list can now be selected)
#4 centralized variable

list_button = []
keyboardmaker()

loop_main_menu = True
loop_setup = False
loop_play = False
loop_gameover = False
loop_setting = False

exit_this_loop = False
useresumebutton = False
backspacenow = False
holdkey = False

storedtext1 = ''
inputa = ''
score = num = 0; round = 1

saveseconds = 0
timelimitinseconds = 60

# game starts
while True:


    # main menu
    if loop_main_menu == True:

        turn_all_game_loops_to_false()
        exit_this_loop = False
        PABM.loop_unblitandunpressall()
       #if useresumebutton == False:



        while True:
            #print(saveseconds)

            # fill the screen
            windowsurface.fill((0,0,0))

            # blit the buttons
            button_title.blit_phraseandbutton()
            button_bypatrickdlr.blit_phraseandbutton()

            if useresumebutton == True:
                button_resume.blit_phraseandbutton()
            else:
                button_play.blit_phraseandbutton()
                button_setting.blit_phraseandbutton()

            # make buttons dynamic
            PABM.loop_hoveringoverbuttons()

            # refresh the display
            pygame.display.update()
            pygame.time.Clock().tick(60)

            # exit this loop
            if exit_this_loop == True:
                break

            # control
            for a in pygame.event.get():

                if a.type == 12:
                    pygame.quit(); sys.exit()

                if a.type == KEYDOWN:
                    if a.key == K_ESCAPE:
                        pygame.quit(), sys.exit()

                    if a.key == K_RETURN:
                        loop_play = True
                        exit_this_loop = True

                if a.type == MOUSEBUTTONDOWN:
                    if a.button == 1:
                        PABM.loop_pressthatbutton()

                        if useresumebutton == True:
                            if button_resume.blit_phraseandbutton().collidepoint(a.pos):

                                loop_play = True
                                exit_this_loop = True

                        if useresumebutton == False:
                            if button_play.blit_phraseandbutton().collidepoint(a.pos):
                                loop_play = True
                                loop_setup = True
                                exit_this_loop = True

                            if button_setting.blit_phraseandbutton().collidepoint(a.pos):
                                loop_setting = True
                                exit_this_loop = True

                #update keyboard even when keyboard is not on game screen atm. to prevent incorrect keyboard positioning
                old_screen_width = dimension1.return_swidth()
                old_screen_height = dimension1.return_sheight()
                if a.type == pygame.VIDEORESIZE:
                    dimension1 = Pygamedisplay(a.w, a.h)
                    windowsurface = pygame.display.set_mode((
                                    dimension1.return_swidth(), dimension1.return_sheight()),
                                    pygame.RESIZABLE)

                    #try integrating into class PABM?
                    for B in list_button:
                        for k,v in B.items():
                            for n in v.list_of_buttons:
                                if n.fixedtoright == False: #need to define more
                                    n.posx += ((int(a.w) - old_screen_width) / 72) #how did i get this 72?
                                else:
                                    n.posx -= ((int(a.w) - old_screen_width) / 72)
                                if n.fixedtobottom == False:
                                    n.posy += ((int(a.h) - old_screen_height) / 72)



    # one-time setup
    if loop_setup == True:
        turn_all_game_loops_to_false()
        exit_this_loop = False
        PABM.loop_unblitandunpressall()

        useresumebutton = False
        loop_play = True
        storedtext1 = ''
        inputa = ''
        score = 0; round = 1; num = 0
        # maxlenanswerlist = len(A1.return_var_original())
        # if maxround.return_var() > maxlenanswerlist:
        #     maxround = maxlenanswerlist - 1



    # gameplay
    if loop_play == True and len(A1.return_var()) == 0:
        turn_all_game_loops_to_false()
        loop_gameover = True

    elif loop_play == True:
        #use [] or something after each round

        if useresumebutton == False:

            num = 0
            answer = A1.return_var()[random.randint(0, len(A1.return_var()) - 1)]

            answer_splitted0 = [a for a in answer]
            answer_splitted0_upper = [a.upper() for a in answer]
            answer_splitted = [a for a in answer]
            answer_bank = []
            hidden_symbol = '_'
            hidden = len(answer) * hidden_symbol
            hidden_splitted = [a for a in hidden]

            inputamulti = []
            usedletters = []
            missed = []
            missedtotal = []

            while ' ' in answer_splitted:
                if ' ' in answer:
                    if ' ' not in hidden_splitted:
                        for a in answer_splitted:
                            if ' ' == a:
                                hidden_splitted[answer_splitted.index(a)] = ' '
                                answer_splitted[answer_splitted.index(a)] = '#'
            start_ticks=pygame.time.get_ticks()
        else:
            start_ticks=pygame.time.get_ticks()-saveseconds


        useresumebutton = False
        turn_all_game_loops_to_false()
        exit_this_loop = False
        PABM.loop_unblitandunpressall()
        blitonce = False

        while True:
            seconds=(pygame.time.get_ticks()-start_ticks)/1000
            #print(pygame.time.get_ticks(), start_ticks, pygame.time.get_ticks()-start_ticks,'playing') #log print

            #print(seconds) #log print

            # fill the screen
            windowsurface.fill((0,0,0))

            PicturePABM1.create_list_image_and_list_image_rect()
            PicturePABM2.create_list_image_and_list_image_rect()

            #print(usedletters)
            if exit_this_loop == False:
                if num <= maxattempt.return_var():
                    windowsurface.blit(PicturePABM1.return_list_image().get(num), PicturePABM1.return_list_image_rect().get(num))
                    windowsurface.blit(PicturePABM2.return_list_image().get(num), PicturePABM2.return_list_image_rect().get(num))
                elif num > maxattempt.return_var():
                    windowsurface.blit(PicturePABM1.return_list_image().get(maxattempt.return_var()), PicturePABM1.return_list_image_rect().get(maxattempt.return_var()))
                    windowsurface.blit(PicturePABM2.return_list_image().get(maxattempt.return_var()), PicturePABM2.return_list_image_rect().get(maxattempt.return_var()))
                    #windowsurface.blit()

                if int(seconds) >= 60:
                    windowsurface.blit(PicturePABM1.return_list_image().get(maxattempt.return_var()), PicturePABM1.return_list_image_rect().get(maxattempt.return_var()))
                    windowsurface.blit(PicturePABM2.return_list_image().get(maxattempt.return_var()), PicturePABM2.return_list_image_rect().get(maxattempt.return_var()))

            # blit whole keyboard
            for a in list_button:
                for k,v in a.items():
                    v.blit_phraseandbutton()

            # blit the phrases
            Phrase(storedtext1, dimension1.return_swidth()*.5, dimension1.return_sheight()*.25, 48).blit()

            # idk why i ccant blit along with the "next round - fail" REVIEW THIS
            if num >= maxattempt.return_var() or int(seconds) >= timelimitinseconds:
                PABM(f'"{answer}"', dimension1.return_swidth()*.5, dimension1.return_sheight()*.45, 'center',
40 , False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'F',
1, False, 1, False).blit_phraseandbutton()
                PABM('Fail', dimension1.return_swidth()*.5, dimension1.return_sheight()*.53, 'center',
48, False, False,
PABM.RED, False, False, 0, 0,
True, True, 'F',
1, False, 1, False).blit_phraseandbutton()

            if ''.join(hidden_splitted) == answer:
                PABM(f'+1 point', dimension1.return_swidth()*.5, dimension1.return_sheight()*.45, 'center',
40 , False, False,
PABM.WHITE, False, False, 0, 0,
True, True, 'F',
1, False, 1, False).blit_phraseandbutton()
                PABM('Pass', dimension1.return_swidth()*.5, dimension1.return_sheight()*.53, 'center',
48, False, False,
PABM.GREEN, False, False, 0, 0,
True, True, 'F',
1, False, 1, False).blit_phraseandbutton()

            Phrase(''.join(hidden_splitted), dimension1.return_swidth()*.5, dimension1.return_sheight()*.35, 48).blit()

            Phrase(f'Attempts remaining: {maxattempt.return_var()-num}', dimension1.return_swidth()*.5, dimension1.return_sheight()*.11, 24).blit()

            Phrase(f'Score: {score}/{maxround.return_var()}', dimension1.return_swidth()*.5, dimension1.return_sheight()*.16, 24).blit()

            phrase_correctletters.blit_phrase_only('Correct Letters: ' + str(', '.join(sorted(usedletters))))

            phrase_incorrectletters.blit_phrase_only('Incorrect Letters: ' + str(', '.join(sorted(missedtotal))))

            if seconds > 0:

                Phrase(str(int(timelimitinseconds-seconds+1)), dimension1.return_swidth()*.5, dimension1.return_sheight()*.25, 48).blit()

            if blitonce == False:
                blitonce = True
                PABM(f'Round {round}/{maxround.return_var()}', dimension1.return_swidth()*.5, 30, 'center',
    30, False, False,
    PABM.WHITE, False, False, 0, 0,
    True, True, 'T',
    1, False, 1, False).blit_phraseandbutton()

            # blit the buttons
            button_quit.blit_phraseandbutton()
            button_pause.blit_phraseandbutton()

            #make buttons dynamic (keyboard typing)
            for B in list_button:
                for k,v in B.items():
                    for n in v.list_of_buttons:
                        if n.TEXT in usedletters or n.TEXT in missedtotal or n.TEXT in storedtext1:
                            n.buttonstate = 2

            # make buttons dynamic
            PABM.loop_hoveringoverbuttons()

            # refresh the display
            pygame.display.update()
            pygame.time.Clock().tick(60)

            # exit this loop
            if exit_this_loop == True:
                break

            # backspace
            if backspacenow == True:
                if len(storedtext1) > 0:
                    storedtext1 = storedtext1[:-1]

            #if useresumebutton == False:
              #  if seconds>10: # if more than 10 seconds close the game
                #   loop_gameover = True
                  #  break

            # end rounds
            if round-1 >= maxround.return_var():
                loop_gameover = True
                break #exit_this_loop = True

            # next round - win
            if ''.join(hidden_splitted) == answer:
                Phrase(answer, dimension1.return_swidth()*.5, dimension1.return_sheight()*.60, 48).blit()

                #pygame.time.wait(2000)
                time.sleep(0.5)
                score += 1

                #Exception: Variable is not in list. Check your input.
                if len(A1.return_var()) > 1:
                    A1.decrease_var(answer)
                    round += 1
                    loop_play = True
                    exit_this_loop = True

                elif len(A1.return_var()) == 1:
                    loop_gameover = True
                    exit_this_loop = True


            # #failed round #DONT delete - good for code review (this is where I pinpointed the issue, turns out that you need to be careful when adding "break" or not.
            # if num >= maxattempt.return_var():
            #     num = maxattempt.return_var() - 0 #or 1
            #     print(num,'loser')
            #     A1.decrease_var(answer)
            #
            #     if A1.return_var() == []:#
            #         #pygame.time.wait(2000)
            #         time.sleep(2)
            #         loop_gameover = True
            #         A1 = CentralizedVariable(A1.return_var_original())
            #     else:
            #         #pygame.time.wait(2000)
            #         time.sleep(2)
            #         loop_play = True
            #         exit_this_loop = True
            #     print('Score +0')
            #     score += 0
            #     round += 1
            #
            #     #break #dont use this!!



            #failed round
            if num >= maxattempt.return_var() or seconds>timelimitinseconds:
                #num = maxattempt.return_var()

                #pygame.time.wait(2000)
                time.sleep(1)
                score += 0

                if len(A1.return_var()) > 1:#
                    A1.decrease_var(answer)
                    round += 1
                    loop_play = True
                    exit_this_loop = True
                elif len(A1.return_var()) == 1:
                    loop_gameover = True
                    exit_this_loop = True


            # control
            for a in pygame.event.get():
                if a.type == 12:
                    pygame.quit(); sys.exit()

                if a.type == KEYDOWN:

                    #if a.key == K_RETURN:
                    #    inputa = storedtext1
                     #   checkletter(inputa)
                    #    storedtext1 = ''

                    #if a.key == K_BACKSPACE:
                    #    backspacenow = True

                    if a.key == K_ESCAPE:
                        A1 = CentralizedVariable(A1.return_var_original())
                        exit_this_loop = True

                    if num <= maxattempt.return_var():
                        if a.key != K_ESCAPE:
                            if a.key != 8:
                                if storedtext1 == ' ':
                                    storedtext1 = ''
                                if a.unicode.lower() in qwerty:
                                    checkletter(a.unicode.lower())
                                    storedtext1 = ''
                                for X in PABM.list_of_buttons:
                                    if X.blitted == True:
                                        if X.TEXT == a.unicode.lower():
                                            X.pressed = True
                                            X.buttonstate = 2


                #if a.type == KEYUP:
                   # if a.key == K_BACKSPACE:
                   #     backspacenow = False


                if a.type == MOUSEBUTTONDOWN:
                    if a.button == 1:
                        if PABM.loop_pressthatbutton() != None and PABM.loop_pressthatbutton() != 'Pause':
                            checkletter(PABM.loop_pressthatbutton())
                            blitonce2 = False

                        if button_quit.blit_phraseandbutton().collidepoint(a.pos):
                            loop_gameover = True
                            useresumebutton = False
                            A1 = CentralizedVariable(A1.return_var_original())
                            exit_this_loop = True

                        if button_pause.blit_phraseandbutton().collidepoint(a.pos):
                            loop_main_menu = True
                            useresumebutton = True
                            saveseconds = pygame.time.get_ticks()-start_ticks
                            exit_this_loop = True

                # for moving entire keyboard while still preserving the pressed/button state
                old_screen_width = dimension1.return_swidth()
                old_screen_height = dimension1.return_sheight()

                if a.type == pygame.VIDEORESIZE:
                    dimension1 = Pygamedisplay(a.w, a.h)
                    windowsurface = pygame.display.set_mode((
                                    dimension1.return_swidth(), dimension1.return_sheight()),
                                    pygame.RESIZABLE)

                    #try integrating into class PABM?
                    for B in list_button:
                        for k,v in B.items():
                            for n in v.list_of_buttons:
                                if n.fixedtoright == False: #need to define more
                                    n.posx += ((int(a.w) - old_screen_width) / 72) #how did i get this 72?
                                else:
                                    n.posx -= ((int(a.w) - old_screen_width) / 72)
                                if n.fixedtobottom == False:
                                    n.posy += ((int(a.h) - old_screen_height) / 72)



                #################



    # game over
    if loop_gameover == True:
        exit_this_loop = False
        turn_all_game_loops_to_false()
        PABM.loop_unblitandunpressall()
        blitonce = False
        while True:
            # fill the screen
            windowsurface.fill((0,0,0))

            # blit the buttons
            phrase_gameover.blit_phraseandbutton()
            #phrase_yourscore.blit_phraseandbutton()

            if blitonce == False:
                phrase_yourscore = PABM(f'Your score is {score} out of {maxround.return_var()}.', mf(dimension1.return_swidth()*.5), mf(dimension1.return_sheight()*.3), 'center',
    30, False, False,
    PABM.WHITE, False, False, 0, 0,
    True, True, 'T',
    1, False, 1, False).blit_phraseandbutton()
                blitonce = True

            phrase_playagain.blit_phraseandbutton()
            button_playagain.blit_phraseandbutton()
            #button_quit2.blit_phraseandbutton()
            button_quit3.blit_phraseandbutton()

            # make buttons dynamic
            PABM.loop_hoveringoverbuttons()

            # refresh the display
            pygame.display.update()
            pygame.time.Clock().tick(60)

            # exit this loop
            if exit_this_loop == True:
                break

            # control
            for a in pygame.event.get():

                if a.type == 12:
                    pygame.quit(); sys.exit()

                if a.type == KEYDOWN:
                    if a.key == K_ESCAPE:
                        pygame.quit(), sys.exit()

                if a.type == MOUSEBUTTONDOWN:
                    if a.button == 1:
                        PABM.loop_pressthatbutton()
                        if button_quit3.blit_phraseandbutton().collidepoint(a.pos):
                            A1 = CentralizedVariable(A1.return_var_original())
                            loop_main_menu = True
                            exit_this_loop = True


                        if button_playagain.blit_phraseandbutton().collidepoint(a.pos):
                            A1 = CentralizedVariable(A1.return_var_original())
                            loop_setup = True
                            exit_this_loop = True

                old_screen_width = dimension1.return_swidth()
                old_screen_height = dimension1.return_sheight()
                if a.type == pygame.VIDEORESIZE:
                    dimension1 = Pygamedisplay(a.w, a.h)
                    windowsurface = pygame.display.set_mode((
                                    dimension1.return_swidth(), dimension1.return_sheight()),
                                    pygame.RESIZABLE)

                    #try integrating into class PABM?
                    for B in list_button:
                        for k,v in B.items():
                            for n in v.list_of_buttons:
                                if n.fixedtoright == False: #need to define more
                                    n.posx += ((int(a.w) - old_screen_width) / 72) #how did i get this 72?
                                else:
                                    n.posx -= ((int(a.w) - old_screen_width) / 72)
                                if n.fixedtobottom == False:
                                    n.posy += ((int(a.h) - old_screen_height) / 72)



    # setting
    if loop_setting == True:
        exit_this_loop = False
        turn_all_game_loops_to_false()
        PABM.loop_unblitandunpressall()
        storedtext1 = ''
        inputa = ''

        toggle1 = 0
        toggle2 = 0
        getoff = False
        dropdownlist1 = {}
        dropdownlist2 = {}
        dropdownlist3 = {}
        scroll_yA1 = 0
        scroll_yA2 = 0
        scroll_y_signal_upA1 = False
        scroll_y_signal_downA1 = False
        scroll_y_signal_upA2 = False
        scroll_y_signal_downA2 = False
        backspacenow = False
        count_answerlist = 0
        displaytemporarytext_save = False
        start_ticks = 0

        while True:
            # fill the screen
            windowsurface.fill((23, 40, 30))

            # blit the buttons
            button_back.blit_phraseandbutton()
            button_save.blit_phraseandbutton()
            phrase_roundspergame.blit_phraseandbutton()
            phrase_roundspergame_X.blit_phraseandbutton(maxround.return_var())
            phrase_attemptsperround.blit_phraseandbutton()
            phrase_attemptsperround_X.blit_phraseandbutton(maxattempt.return_var())
            phrase_listofwords.blit_phraseandbutton()
            phrase_listofwords_X.blit_phraseandbutton(str(len(A1.return_var())))

            if toggle1 == 1:
                PABM.loop_unblitandunpressall()

                button_textfield1.blit_phraseandbutton()
                Phrase(storedtext1, mf(dimension1.return_swidth() * 0.50), mf(dimension1.return_sheight() * 0.70), 36).blit()

                #textile_active print
                button_up4.blit_phraseandbutton()
                button_down5.blit_phraseandbutton()
                row = .8
                for a in A1.return_var():
                    x = mf(dimension1.return_swidth()*.64)
                    y = mf((dimension1.return_sheight()*row)+scroll_yA1)
                    if y < dimension1.return_sheight():
                        if y > (dimension1.return_sheight()*.75):
                            button4 = Phrase(str(a), x, y, 24).blitwithbutton(1)
                            #button4 = Phrase(str(a), x, y, 24).blitwithbutton(1)
                            dropdownlist1.setdefault(str(a),button4)
                        row += .05


                #textile_inactive print

                button_up6.blit_phraseandbutton()
                button_down7.blit_phraseandbutton()

                row = .8
                for a in A2.return_var():
                    x = mf(dimension1.return_swidth()*.33)
                    y = mf((dimension1.return_sheight()*row)+scroll_yA2)
                    if y < dimension1.return_sheight():
                        if y > (dimension1.return_sheight()*.75):
                            button6 = Phrase(str(a), x, y, 24).blitwithbutton(1)
                            dropdownlist2.setdefault(str(a),button6)
                            button7 = Phrase('DEL', button6.right + 30, y, 24).blitwithbutton(1,1)
                            dropdownlist3.setdefault(str(a), button7)
                        row += .05

                #pygame.draw.rect(windowsurface, (23, 40, 30), pygame.Rect(0,435,800,30))
                #pygame.draw.rect(windowsurface, (23, 40, 30), pygame.Rect(0,585,800,30))

                pygame.draw.rect(windowsurface, (23, 40, 30), pygame.Rect(0,mf(dimension1.return_sheight() *.725),mf(dimension1.return_swidth()),30))
                pygame.draw.rect(windowsurface, (23, 40, 30), pygame.Rect(0,mf(dimension1.return_sheight() *.975),mf(dimension1.return_swidth()),30))
            else:
                PABM.loop_unblitandunpressall()

            if toggle2 == 1:
                Phrase(storedtext1, mf(dimension1.return_swidth() / 2), 90).blit(2)

            button_up1.blit_phraseandbutton(); button_down1.blit_phraseandbutton()
            button_expand.blit_phraseandbutton()
            button_up2.blit_phraseandbutton(); button_down2.blit_phraseandbutton()

            if displaytemporarytext_save == True:
                print(((pygame.time.get_ticks() - start_ticks)/1000))
                if ((pygame.time.get_ticks() - start_ticks)/1000) < 2:
                    button_saved.blit_phraseandbutton()
                if ((pygame.time.get_ticks() - start_ticks)/1000) >= 2:
                    displaytemporarytext_save = False

            # make buttons dynamic
            PABM.loop_hoveringoverbuttons()

            # refresh the display
            pygame.display.update()
            pygame.time.Clock().tick(60)

            # exit this loop
            if exit_this_loop == True:
                break

            # backspace
            if backspacenow == True:
                if len(storedtext1) > 0:
                    storedtext1 = storedtext1[:-1]




            # #scroll_y_signal
            # print(dropdownlist1)
            # print(dropdownlist2)
            # print(dropdownlist3)
            #
            # dropdownlist1_listversion = [dropdownlist1[i][1] for i in sorted(dropdownlist1)]
            # print(dropdownlist1_listversion)
            # if len(dropdownlist1_listversion) != 0:
            #     print(list(dropdownlist1_listversion)[0])
            #     print(list(dropdownlist1_listversion)[-1])
            # #465, 555
            #
            #
            # if dropdownlist1_listversion[0] > 465:
            if scroll_y_signal_downA1 == True:
                dropdownlist1 = {}
                dropdownlist2 = {}
                dropdownlist3 = {}
                scroll_yA1 -= 13
            if scroll_y_signal_upA1 == True:
                dropdownlist1 = {}
                dropdownlist2 = {}
                dropdownlist3 = {}
                scroll_yA1 += 13
            if scroll_y_signal_downA2 == True:
                dropdownlist1 = {}
                dropdownlist2 = {}
                dropdownlist3 = {}
                scroll_yA2 -= 13
            if scroll_y_signal_upA2 == True:
                dropdownlist1 = {}
                dropdownlist2 = {}
                dropdownlist3 = {}
                scroll_yA2 += 13

            # control
            for a in pygame.event.get():
                if a.type == 12:
                    pygame.quit(); sys.exit()

                #update keyboard even when keyboard is not on game screen atm. to prevent incorrect keyboard positioning
                old_screen_width = dimension1.return_swidth()
                old_screen_height = dimension1.return_sheight()
                if a.type == pygame.VIDEORESIZE:

                    dropdownlist1 = {}
                    dropdownlist2 = {}
                    dropdownlist3 = {}

                    dimension1 = Pygamedisplay(a.w, a.h)
                    windowsurface = pygame.display.set_mode((
                                    dimension1.return_swidth(),dimension1.return_sheight()),pygame.RESIZABLE)

                    #try integrating into class PABM?
                    for B in list_button:
                        for k,v in B.items():
                            for n in v.list_of_buttons:
                                if n.fixedtoright == False: #need to define more
                                    n.posx += ((int(a.w) - old_screen_width) / 72) #how did i get this 72?
                                else:
                                    n.posx -= ((int(a.w) - old_screen_width) / 72)
                                if n.fixedtobottom == False:
                                    n.posy += ((int(a.h) - old_screen_height) / 72)



                if a.type == KEYUP:
                    if a.key == K_UP:
                        if toggle1 == 1:
                            scroll_y_signal_up = False
                    if a.key == K_DOWN:
                        if toggle1 == 1:
                            scroll_y_signal_down = False

                    if a.key == K_BACKSPACE:
                        backspacenow = False



                if a.type == KEYDOWN:
                    if a.key == K_UP:
                        if toggle1 == 1:
                            scroll_y_signal_up = True

                    if a.key == K_DOWN:
                        if toggle1 == 1:
                            scroll_y_signal_down = True

                    if a.key == K_RETURN:
                        A1.increase_var(storedtext1)
                        A1 = CentralizedVariable(sorted(A1.return_var()))
                        storedtext1 = ''
                        dropdownlist1 = {}
                        dropdownlist2 = {}
                        dropdownlist3 = {}

                    if a.key == K_ESCAPE:
                        pygame.quit(), sys.exit()

                    #update storedtext1
                    if a.key != 8:
                        if a.key != K_ESCAPE:
                            if a.key != K_RETURN:
                                if storedtext1 == ' ':
                                    storedtext1 = ''
                                storedtext1 += a.unicode

                    if a.key == K_BACKSPACE:
                        backspacenow = True


                if a.type == MOUSEBUTTONUP:
                    if a.button == 1:
                        if button_up4.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_upA2 = False
                        if button_down5.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_downA2 = False

                        if button_up6.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_upA1 = False
                        if button_down7.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_downA1 = False

                if a.type == MOUSEBUTTONDOWN:
                    if a.button == 1:
                        if button_back.blit_phraseandbutton().collidepoint(a.pos):
                            loop_main_menu = True
                            exit_this_loop = True

                        if button_save.blit_phraseandbutton().collidepoint(a.pos):
                            print('saved')
                            save()
                            displaytemporarytext_save = True
                            start_ticks=pygame.time.get_ticks()

                        if button_up1.blit_phraseandbutton().collidepoint(a.pos):
                            #if maxround.return_var() < maxround.return_var_original():
                            if maxround.return_var() < len(A1.return_var()):
                                maxround.increase_var()
                        if button_down1.blit_phraseandbutton().collidepoint(a.pos):
                            if maxround.return_var() > 1:
                                maxround.decrease_var()
                        if button_up2.blit_phraseandbutton().collidepoint(a.pos):
                            if maxattempt.return_var() < maxattempt.return_var_original():
                                maxattempt.increase_var()
                        if button_down2.blit_phraseandbutton().collidepoint(a.pos):
                            if maxattempt.return_var() > 1:
                                maxattempt.decrease_var()
                        if button_expand.blit_phraseandbutton().collidepoint(a.pos):
                            if toggle1 == 0:
                                toggle1 = 1
                            else:
                                toggle1 = 0

                        if button_up4.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_upA2 = True
                        if button_down5.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_downA2 = True

                        if button_up6.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_upA1 = True
                        if button_down7.blit_phraseandbutton().collidepoint(a.pos):
                            scroll_y_signal_downA1 = True

                        try: #is this good to use? check out try-except-else-finally
                            if toggle1 == 1:
                                for k,v in dropdownlist1.items():
                                    if v.collidepoint(a.pos):
                                        for a in A1.return_var():
                                            if a == k:
                                                A1.decrease_var(a)
                                                A2.increase_var(a)
                                                A1 = CentralizedVariable(sorted(A1.return_var()))
                                                A2 = CentralizedVariable(sorted(A2.return_var()))
                                                #dropdownlist1/2/3 can't be in one line. idk why
                                                dropdownlist1 = {}
                                                dropdownlist2 = {}
                                                dropdownlist3 = {}
                                                if A1.return_var_len() < maxround.return_var():
                                                    if maxround.return_var() > 1:
                                                        maxround.decrease_var()
                                for k,v in dropdownlist2.items():
                                    if v.collidepoint(a.pos):
                                        for a in A2.return_var():
                                            if a == k:
                                                A2.decrease_var(a)
                                                A1.increase_var(a)

                                                maxround = CentralizedVariable(len(A1.return_var()))
                                                A1 = CentralizedVariable(sorted(A1.return_var()))
                                                A2 = CentralizedVariable(sorted(A2.return_var()))
                                                dropdownlist1 = {}
                                                dropdownlist2 = {}
                                                dropdownlist3 = {}
                                for k,v in dropdownlist3.items():
                                    if v.collidepoint(a.pos):
                                        for a in A2.return_var():
                                            if a == k:
                                                print('deleted',a)
                                                A2.decrease_var(a)
                                                A2 = CentralizedVariable(sorted(A2.return_var()))
                                                dropdownlist1 = {}
                                                dropdownlist2 = {}
                                                dropdownlist3 = {}
                            break
                        except AttributeError:
                            pass
