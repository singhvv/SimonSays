import random, time, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 700
WINDOWHEIGHT = 600
FLASHSPEED = 200
FLASHDELAY = 200
TILESIZE = 220
TILEGAPSIZE = 30
TIMEOUT = 4


WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (100,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 100,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 100)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (100, 100,   0)
GREY         = (100,  100,  100)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * TILESIZE) - TILEGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * TILESIZE) - TILEGAPSIZE) / 2)

# Creating rectangular objects for four tiles
YELLOWRECTANGLE = pygame.Rect(XMARGIN, YMARGIN, TILESIZE, TILESIZE)
BLUERECTANGLE   = pygame.Rect(XMARGIN + TILESIZE + TILEGAPSIZE, YMARGIN, TILESIZE, TILESIZE)
REDRECTANGLE    = pygame.Rect(XMARGIN, YMARGIN + TILESIZE + TILEGAPSIZE, TILESIZE, TILESIZE)
GREENRECTANGLE  = pygame.Rect(XMARGIN + TILESIZE + TILEGAPSIZE, YMARGIN + TILESIZE + TILEGAPSIZE, TILESIZE, TILESIZE)




def main():
    global FPSCLOCK, DISPLAYSURF, FONT, BEEP1, BEEP2, BEEP3, BEEP4, GAMEOVER

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('SimonSays')

    FONT = pygame.font.Font('freesansbold.ttf', 14)
    infoSurf = FONT.render('Repeat the pattern shown by the tiles', 1, GREY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # Loading the beeps
    BEEP1 = pygame.mixer.Sound('sounds/beep1.wav')
    BEEP2 = pygame.mixer.Sound('sounds/beep2.wav')
    BEEP3 = pygame.mixer.Sound('sounds/beep3.wav')
    BEEP4 = pygame.mixer.Sound('sounds/beep4.wav')
    GAMEOVER = pygame.mixer.Sound('sounds/gameover.wav')

    # Start game with variables
    pattern = [] # Array will store colour patterns for tiles
    currentStep = 0 # Next colour that must be pressed by Player
    lastClickTime = 0 # Last button press timestamp
    score = 0
    waitingForInput = False # When this is False, the pattern is going on.
    # When this is True, tha game is waiting for the player to click a button:

    while True: # Gameplay
        clickedButton = None # Button clicked by player (Valid values are YELLOW, RED, GREEN, or BLUE)
        DISPLAYSURF.fill(bgColor)
        makeTiles()

        scoreSurf = FONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        QuitTrue()
        for event in pygame.event.get(): # event handling
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getClick(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN



        if not waitingForInput:
            # Making pattern
            pygame.display.update()
            pygame.time.wait(500)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # Waiting for Player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # Case: Correct button pressed
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # Last button in pattern pressed
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # Reset to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # Pushed incorrect button or timeout
                gameOverAnimation()
                # Reset variables for new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)




def makeTiles():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECTANGLE)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECTANGLE)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECTANGLE)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECTANGLE)

def QuitTrue():
    for event in pygame.event.get(QUIT): # Check all quitting events
        terminate() # If any quitting events are found, terminate() is called
    for event in pygame.event.get(KEYUP): # get all KEYUP events
        if event.key == K_ESCAPE:
            terminate() # Call terminate() if the KEYUP event was for Esc key
        pygame.event.post(event) # Put other KEYUP event objects back

def getClick(x, y):
    if YELLOWRECTANGLE.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECTANGLE.collidepoint( (x, y) ):
        return BLUE
    elif REDRECTANGLE.collidepoint( (x, y) ):
        return RED
    elif GREENRECTANGLE.collidepoint( (x, y) ):
        return GREEN
    return None

def flashButtonAnimation(color, animationSpeed = 50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECTANGLE
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECTANGLE
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECTANGLE
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECTANGLE

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((TILESIZE, TILESIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            QuitTrue()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))

def changeBackgroundAnimation(animationSpeed = 50):
    # print ("notdefined")
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # Animation loop
        QuitTrue()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        makeTiles() # Redraw the buttons on top of the tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation():
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    GAMEOVER.play()

def terminate():
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()