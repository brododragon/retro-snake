# main.py
import math
import random
from multipledispatch import dispatch
import pygame
import os
from collections.abc import Iterable
import snakemethods, helper
import snakeclasses


pygame.init()

class GameState:
    def __init__(self, width=800, height=600, fullscreen=False):
        # Screen settings
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        
        # Initialize display
        if fullscreen:
            self.canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width = self.canvas.get_width()
            self.height = self.canvas.get_height()
        else:
            self.canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        
        # Grid system
        self.gridSize = 20  # Increased for better scaling
        self.pixelsPerSquare = min(self.width, self.height) // self.gridSize
        
        # Colors
        self.BLACK = pygame.Color(0, 0, 0)
        self.WHITE = pygame.Color(255, 255, 255)
        self.BACKGROUND = (15, 11, 41)
        self.SNAKECOLOR = pygame.Color(81, 240, 89)
        self.SNAKECOLOR2 = pygame.Color(7, 100, 250)
        self.TEXTCOLOR = pygame.Color(160, 217, 235)
        self.APPLECOLOR = pygame.Color(207, 48, 108)
        
        # Game settings
        self.GRADIENTSNAKE = True
        self.TICKLENGTH = .25
        self.TICKKEY = pygame.K_SPACE
        self.startingLength = 3
        
        # Game state
        self.dead = False
        self.score = 0
        self.doTick = False
        self.t_Old = 0
        self.deltaTime = 0
        self.rawInput = None
        
        # Debug settings
        self.doDebugDraw = False
        self.doTerminalClearing = False
        
        # Initialize fonts (scale with screen size)
        font_size_big = max(24, min(self.width, self.height) // 20)
        font_size_small = max(12, min(self.width, self.height) // 40)
        self.retroFontBig = pygame.font.Font("Retro Gaming.ttf", font_size_big)
        self.retroFontSmall = pygame.font.Font("Retro Gaming.ttf", font_size_small)
        
        # Game objects
        self.snake = []
        self.turningPoint = []
        self.inFrontDebugRects = []
        
        # Apple setup
        self.appleSize = .5
        self.applePadding = (1 - self.appleSize) / 2 * self.pixelsPerSquare
        self.appleRect = pygame.Rect(0, 0, 
                                   self.pixelsPerSquare - (self.applePadding * 2), 
                                   self.pixelsPerSquare - (self.applePadding * 2))
        
        # Input mapping
        self.DIRECTIONDICT = {
            pygame.K_a: helper.vector(-1, 0),
            pygame.K_d: helper.vector(1, 0),
            pygame.K_w: helper.vector(0, -1),
            pygame.K_s: helper.vector(0, 1),
            pygame.K_LEFT: helper.vector(-1, 0),
            pygame.K_RIGHT: helper.vector(1, 0),
            pygame.K_UP: helper.vector(0, -1),
            pygame.K_DOWN: helper.vector(0, 1)
        }
        
        # Initialize game
        snakemethods.respawnSnake(self)
    
    def resize_screen(self, new_width, new_height):
        """Handle screen resize events"""
        self.width = new_width
        self.height = new_height
        self.canvas = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        
        # Recalculate grid and scaling
        self.pixelsPerSquare = min(self.width, self.height) // self.gridSize
        
        # Update apple size
        self.applePadding = (1 - self.appleSize) / 2 * self.pixelsPerSquare
        self.appleRect.width = self.pixelsPerSquare - (self.applePadding * 2)
        self.appleRect.height = self.pixelsPerSquare - (self.applePadding * 2)
        
        # Update fonts
        font_size_big = max(24, min(self.width, self.height) // 20)
        font_size_small = max(12, min(self.width, self.height) // 40)
        self.retroFontBig = pygame.font.Font("Retro Gaming.ttf", font_size_big)
        self.retroFontSmall = pygame.font.Font("Retro Gaming.ttf", font_size_small)
        
        # Update snake segment positions
        for seg in self.snake:
            seg.rect.width = self.pixelsPerSquare
            seg.rect.height = self.pixelsPerSquare
            seg.rect.x = helper.gridToPixels(seg.gridX, self.pixelsPerSquare)
            seg.rect.y = helper.gridToPixels(seg.gridY, self.pixelsPerSquare)
        
        # Respawn apple to ensure it's still valid
        snakemethods.respawnApple(self)
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width = self.canvas.get_width()
            self.height = self.canvas.get_height()
        else:
            self.canvas = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
            self.width = 800
            self.height = 600
        
        # Recalculate everything for new screen size
        self.resize_screen(self.width, self.height)


def moveBodySegments(game_state):
    turningSegments = {}
    for ind, seg in enumerate(game_state.snake):
        seg.move(seg.direction.x, seg.direction.y, game_state.pixelsPerSquare)

        collisionList = game_state.snake[:]
        collisionList.pop(ind)

        collision = pygame.Rect.collidelist(seg.rect, collisionList)
        if collision != -1 and collision != ind and collision != len(collisionList) - 1:
            onDeath(game_state, f"hitting your tail")
            return

        if ind == 0:
            if not (0 <= game_state.snake[0].gridX < game_state.gridSize and 0 <= game_state.snake[0].gridY < game_state.gridSize):
                onDeath(game_state, f"hitting the wall")
                return
            if pygame.Rect.collidepoint(seg.rect, (game_state.appleRect.x, game_state.appleRect.y)):
                snakemethods.collectApple(game_state)
        else:
            gridInFront = (seg.gridX + seg.direction.x, seg.gridY + seg.direction.y)
            nextSeg = game_state.snake[ind - 1]
            
            inFrontRect = pygame.Rect(
                helper.gridToPixelsVec(
                    (seg.gridX + seg.direction.x + 1/4, seg.gridY + seg.direction.y + 1/4),
                    game_state.pixelsPerSquare
                ),
                (game_state.pixelsPerSquare / 2, game_state.pixelsPerSquare / 2)
            )

            if gridInFront != (nextSeg.gridX, nextSeg.gridY):
                turningSegments[ind] = nextSeg.direction

            game_state.inFrontDebugRects.append(inFrontRect)

    for ind in turningSegments:
        game_state.snake[ind].direction = turningSegments[ind]


def drawBodySegments(game_state):
    for ind, seg in enumerate(game_state.snake):
        if not game_state.GRADIENTSNAKE: 
            drawColor = game_state.SNAKECOLOR
        else: 
            drawColor = pygame.Color.lerp(game_state.SNAKECOLOR, game_state.SNAKECOLOR2, ind / len(game_state.snake))
        pygame.draw.rect(game_state.canvas, drawColor, seg.rect)


def onDeath(game_state, cause=None):
    game_state.dead = True
    print("You Died!" if cause == None else f"You died of {cause}!")
    game_state.snake[0].move(-game_state.snake[0].direction.x, -game_state.snake[0].direction.y, game_state.pixelsPerSquare)


def calcNewInputDirection(keyID, oldDirection, game_state):
    inputDirection = game_state.DIRECTIONDICT.get(keyID, oldDirection)
    if not (helper.areOppDirection(inputDirection.x, oldDirection.x) or helper.areOppDirection(inputDirection.y, oldDirection.y)):
        newDirection = inputDirection
    else:
        newDirection = oldDirection
    return newDirection


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # Initialize game
    pygame.display.set_caption("Snake")
    game_state = GameState(600, 600)  # Default size, can be changed
    clock = pygame.time.Clock()
    exit = False

    # Draw first frame
    game_state.canvas.fill(game_state.BACKGROUND)
    drawBodySegments(game_state)
    snakemethods.drawApple(game_state)
    snakemethods.drawScore(game_state)

    fps = 60

    while not exit:
        game_state.inFrontDebugRects = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            
            elif event.type == pygame.VIDEORESIZE:
                game_state.resize_screen(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # Toggle fullscreen with F11
                    game_state.toggle_fullscreen()
                elif game_state.dead:
                    game_state.dead = False
                    snakemethods.respawnSnake(game_state)
                else:
                    if event.key in game_state.DIRECTIONDICT.keys(): 
                        game_state.rawInput = event.key
                    if game_state.TICKLENGTH and event.key == game_state.TICKKEY:
                        game_state.doTick = True

        # Calculate deltaTime for next frame
        t = pygame.time.get_ticks()
        game_state.deltaTime += (t - game_state.t_Old) / 1000.0
        game_state.t_Old = t
        
        if not game_state.dead and ((game_state.TICKLENGTH == -1 and game_state.doTick) or (game_state.TICKLENGTH >= 0 and game_state.deltaTime >= game_state.TICKLENGTH)):
            if game_state.TICKLENGTH >= 0: 
                game_state.deltaTime = 0
            if game_state.doTick: 
                game_state.doTick = False

            if game_state.doTerminalClearing: 
                clearTerminal()

            game_state.canvas.fill(game_state.BACKGROUND)
            game_state.snake[0].direction = calcNewInputDirection(game_state.rawInput, game_state.snake[0].direction, game_state)
            moveBodySegments(game_state)
            drawBodySegments(game_state)
            snakemethods.drawApple(game_state)
            snakemethods.drawScore(game_state)
            
            if game_state.doDebugDraw:
                for ind, rect in enumerate(game_state.inFrontDebugRects):
                    if not game_state.GRADIENTSNAKE: 
                        drawColor = pygame.Color.lerp(game_state.BLACK, game_state.WHITE, ind / len(game_state.inFrontDebugRects))
                    else: 
                        drawColor = pygame.Color.lerp(game_state.SNAKECOLOR, game_state.SNAKECOLOR2, (ind + 1) / len(game_state.snake))
                    pygame.draw.rect(game_state.canvas, drawColor, rect)
                    
        elif game_state.dead:
            deathText = game_state.retroFontBig.render("Game Over", True, game_state.TEXTCOLOR)
            retryText = game_state.retroFontSmall.render("Press any key to retry", True, game_state.TEXTCOLOR)
            game_state.canvas.blit(deathText, deathText.get_rect(center=game_state.canvas.get_rect().center))
            game_state.canvas.blit(retryText, retryText.get_rect(center=game_state.canvas.get_rect().center).move(0, 50))

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
