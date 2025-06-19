import snakeclasses, helper
import random
import pygame
import math

def respawnApple(game_state):
    while True:
        game_state.appleRect.x = helper.gridToPixels(random.randint(0, game_state.gridSize - 1), game_state.pixelsPerSquare) + game_state.applePadding
        game_state.appleRect.y = helper.gridToPixels(random.randint(0, game_state.gridSize - 1), game_state.pixelsPerSquare) + game_state.applePadding

        if pygame.Rect.collidelist(game_state.appleRect, game_state.snake) == -1:
            break

def collectApple(game_state):
    game_state.score += 1
    game_state.snake.append(snakeclasses.segment(game_state))
    respawnApple(game_state)

def drawApple(game_state):
    pygame.draw.rect(game_state.canvas, game_state.APPLECOLOR, game_state.appleRect)

def drawScore(game_state):
    scoreText = game_state.retroFontSmall.render(f"Score: {game_state.score}", True, game_state.TEXTCOLOR)
    game_state.canvas.blit(scoreText, scoreText.get_rect(topright=game_state.canvas.get_rect().topright))

def respawnSnake(game_state):
    game_state.snake.clear()
    game_state.score = 0
    
    headposx, headposy = math.ceil(game_state.gridSize / 2), math.ceil(game_state.gridSize / 2)
    game_state.snake.append(snakeclasses.segment(game_state, headposx, headposy, helper.vector(1, 0)))
    for i in range(game_state.startingLength - 1):
        game_state.snake.append(snakeclasses.segment(game_state))
    
    respawnApple(game_state)

def nextBestMove(board: list[list]):
    return helper.vector(0, 1)
