import snakeclasses, helper
import random
import pygame
import math

def respawnApple(snake, appleRect, applePadding, gridSize, pixelsPerSquare):
    while True:
        appleRect.x = helper.gridToPixels(random.randint(0, gridSize - 1), pixelsPerSquare) + applePadding
        appleRect.y = helper.gridToPixels(random.randint(0, gridSize - 1), pixelsPerSquare) + applePadding

        if pygame.Rect.collidelist(appleRect, snake) == -1: # generate another apple position if this one is inside the snake
            break

def collectApple(snake, appleRect, applePadding, gridSize, pixelsPerSquare):
    global score
    score += 1
    snake.append(snakeclasses.segment(snake, pixelsPerSquare))
    respawnApple(snake, appleRect, applePadding, gridSize, pixelsPerSquare)

def drawApple(canvas, APPLECOLOR, appleRect):
    pygame.draw.rect(canvas, APPLECOLOR, appleRect)

def drawScore(x, retroFontSmall, TEXTCOLOR, canvas):
    scoreText = retroFontSmall.render(f"Score: {x}", True, TEXTCOLOR)
    canvas.blit(scoreText, scoreText.get_rect(topright = canvas.get_rect().topright))


def respawnSnake(snake, gridSize, pixelsPerSquare, startingLength, appleRect, applePadding):
    snake.clear()
    global score
    score = 0
    
    headposx, headposy = math.ceil(gridSize / 2), math.ceil(gridSize / 2)
    snake.append(snakeclasses.segment(snake, pixelsPerSquare, headposx, headposy, helper.vector(1, 0))) # head of snake
    for i in range(startingLength - 1): # body
        snake.append(snakeclasses.segment(snake, pixelsPerSquare))
    
    respawnApple(snake, appleRect, applePadding, gridSize, pixelsPerSquare)