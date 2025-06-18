import math
import random
from multipledispatch import dispatch
import pygame
import os
from collections.abc import Iterable
import snakemethods, helper
import snakeclasses


pygame.init()

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

# CREATING CANVAS
width = height = 500
canvas = pygame.display.set_mode((width, height))

# use a NxN grid system to make calculations simpler and easy to scale; independent of pixels
gridSize = 10  # TODO make grid be able to be a non-square; ex. 3x5
pixelsPerSquare = math.ceil(width / gridSize)


# TICK STUFF
TICKLENGTH = .25 # how long between frames, in seconds
TICKKEY = pygame.K_SPACE # if TICKLENGTH == -1, do tick when this key is pressed
doTick = False
t_Old = 0 # get_ticks is how long since the pygame was initialized, basically .old
deltaTime = 0

# TITLE OF WINDOW
pygame.display.set_caption("Snake")
dead = False


doDebugDraw = False # Draw debugging shapes?

doTerminalClearing = False # Clear terminal every frame?
clearTerminal = lambda: os.system('cls' if os.name == 'nt' else 'clear')


# COLORS
BACKGROUND = (15, 11, 41)

GRADIENTSNAKE = True
SNAKECOLOR = pygame.Color(81, 240, 89)
SNAKECOLOR2 = pygame.Color(7, 100, 250)

TEXTCOLOR = pygame.Color(160, 217, 235)

# BODY SEGMENTS
segmentSize = pixelsPerSquare
snake = []
startingLength = 3
turningPoint = []

# TEXT
retroFontBig = pygame.font.Font("Retro Gaming.ttf", int(width / 8))
retroFontSmall = pygame.font.Font("Retro Gaming.ttf", int(width / 24))

# death text
deathText = retroFontBig.render("Game Over", True, TEXTCOLOR)

# retry text
retryText = retroFontSmall.render("Press any key to retry", True, TEXTCOLOR)


DIRECTIONDICT = {
    pygame.K_a: helper.vector(-1, 0),
    pygame.K_d: helper.vector(1, 0),
    pygame.K_w: helper.vector(0, -1),
    pygame.K_s: helper.vector(0, 1),
    pygame.K_LEFT: helper.vector(-1, 0),
    pygame.K_RIGHT: helper.vector(1, 0),
    pygame.K_UP: helper.vector(0, -1),
    pygame.K_DOWN: helper.vector(0, 1)
}
rawInput = None

def moveBodySegments():
    turningSegments = {} # change the direction of these segments we should after the for loop. 
                         # We can't turn during it because that would cause the segments behind it to think th segment was going a different direction
    for ind, seg in enumerate(snake):
        seg.move(seg.direction.x, seg.direction.y, pixelsPerSquare)

        # makes a copied snake list without the current segment - we don't want segment to just collide with itself
        collisionList = snake[:]
        collisionList.pop(ind)

        # WARNING - because we remove an element from the list, the index collision gives us will sometimes be INCORRECT
        collision = pygame.Rect.collidelist(seg.rect, collisionList)
        if collision != -1 and collision != ind and collision != len(collisionList) - 1:
            onDeath(f"hitting your tail")
            return

        if ind == 0:
            if not (0 <= snake[0].gridX < gridSize and 0 <= snake[0].gridY < gridSize): # if the head is out of bounds, we're dead
                onDeath(f"hitting the wall")
                return
            if pygame.Rect.collidepoint(seg.rect, (appleRect.x, appleRect.y)):
                snakemethods.collectApple(snake, appleRect, applePadding, gridSize, pixelsPerSquare)
        else:
            gridInFront = (seg.gridX + seg.direction.x, seg.gridY + seg.direction.y)
            nextSeg = snake[ind - 1]
            
            # draw the rect each seg is testing to see if the snake has turned
            inFrontRect = pygame.Rect(
                helper.gridToPixelsVec(
                    (seg.gridX + seg.direction.x + 1/4, seg.gridY + seg.direction.y + 1/4),
                    pixelsPerSquare
                ),
                (pixelsPerSquare / 2, pixelsPerSquare / 2)
            )

            if gridInFront != (nextSeg.gridX, nextSeg.gridY):
                turningSegments[ind] = nextSeg.direction

            inFrontDebugRects.append(inFrontRect)

    for ind in turningSegments:
        snake[ind].direction = turningSegments[ind]

            

def drawBodySegments():
    for ind, seg in enumerate(snake):
        if not GRADIENTSNAKE: drawColor = SNAKECOLOR
        else: drawColor = pygame.Color.lerp(SNAKECOLOR, SNAKECOLOR2, ind / len(snake))
        pygame.draw.rect(canvas, drawColor, seg.rect)

def onDeath(cause=None):
    global dead
    dead = True
    

    print("You Died!" if cause == None else f"You died of {cause}!")

    snake[0].move(-snake[0].direction.x, -snake[0].direction.y, pixelsPerSquare) # kinda sketchy, but its easier to move the head and see if we're colliding (w/ other segs) and then move it back if we are


def calcNewInputDirection(keyID, oldDirection):
    inputDirection = DIRECTIONDICT.get(keyID, oldDirection) # the direction last inputted
    if not (helper.areOppDirection(inputDirection.x, oldDirection.x) or helper.areOppDirection(inputDirection.y, oldDirection.y)): # make sure the direction inputted is not opposite to the current x or y direction
        newDirection = inputDirection
    else:
        newDirection = oldDirection

    return(newDirection)

# apples and score
score = 0
APPLECOLOR = pygame.Color(207, 48, 108)
appleSize = .5 # percent of size of the grid size
applePadding = (1 - appleSize) / 2 * pixelsPerSquare
appleRect = pygame.Rect(0, 0, pixelsPerSquare - (applePadding * 2), pixelsPerSquare - (applePadding * 2))


snakemethods.respawnSnake(snake, gridSize, pixelsPerSquare, startingLength, appleRect, applePadding)


clock = pygame.time.Clock()
exit = False

# draw first frame - don't want to do any movement or calculations yet
canvas.fill(BACKGROUND)
drawBodySegments()
snakemethods.drawApple(canvas, APPLECOLOR, appleRect)
snakemethods.drawScore(score, retroFontSmall, TEXTCOLOR, canvas)

fps = 60

while not exit:
    inFrontDebugRects = [] # put debugging rects in here so we can draw after frame update, emptied after frame update to avoid old debug artifacts
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True

        elif event.type == pygame.KEYDOWN:
            if dead: # if they hit any key while they are dead, respawn them
                dead = False
                snakemethods.respawnSnake(snake, gridSize, pixelsPerSquare, startingLength, appleRect, applePadding)

            else:
                if event.key in DIRECTIONDICT.keys(): rawInput = event.key # log the latest valid 
                # input so that only the latest valid input is considered,
                # because we don't want to try and use every input after the previous frame.
                
                if TICKLENGTH and event.key == TICKKEY:
                    doTick = True

    # Calculate deltaTime for next frame
    t = pygame.time.get_ticks()
    deltaTime += (t - t_Old) / 1000.0 # deltaTime in seconds.
    t_Old = t
    
    if not dead and ((TICKLENGTH == -1 and doTick) or (TICKLENGTH >= 0 and deltaTime >= TICKLENGTH)):
        if TICKLENGTH >= 0: deltaTime = 0
        if doTick: doTick = False

        if doTerminalClearing: clearTerminal()

        canvas.fill(BACKGROUND)
        snake[0].direction = calcNewInputDirection(rawInput, snake[0].direction)
        moveBodySegments()
        drawBodySegments()
        snakemethods.drawApple(canvas, APPLECOLOR, appleRect)
        snakemethods.drawScore(score, retroFontSmall, TEXTCOLOR, canvas)
        if doDebugDraw:
            for ind, rect in enumerate(inFrontDebugRects):
                # BW gradient if the snake is monochrome, otherwise use the segment that is drawing the debug rect
                if not GRADIENTSNAKE: drawColor = pygame.Color.lerp(BLACK, WHITE, ind / len(inFrontDebugRects))
                else: drawColor = pygame.Color.lerp(SNAKECOLOR, SNAKECOLOR2, (ind + 1) / len(snake))

                pygame.draw.rect(canvas, drawColor, rect)
    elif dead: # WARNING this repeatedly draws text to the screen without redrawing the canvas - may have ghosting issues in the future
        canvas.blit(deathText, deathText.get_rect(center = canvas.get_rect().center))
        canvas.blit(retryText, retryText.get_rect(center = canvas.get_rect().center).move(0, 50))

    pygame.display.update()
    clock.tick(fps)
