import snakemethods, helper
import pygame

class segment:
    def __init__(self, game_state, gridX: int = None, gridY: int = None, direction: helper.vector = None) -> None:
        self.ind = len(game_state.snake)
        if self.ind != 0: 
            previousSeg = game_state.snake[self.ind - 1]
        
        # If no gridx/y passed, place segment behind the previous segment
        self.gridX = gridX if gridX != None else previousSeg.gridX - previousSeg.direction.x
        self.gridY = gridY if gridY != None else previousSeg.gridY - previousSeg.direction.y
        # Same thing, set this direction to previous seg's direction
        self.direction = direction if direction != None else previousSeg.direction

        self.rect = pygame.Rect(helper.gridToPixelsVec(self.gridX, self.gridY, game_state.pixelsPerSquare), 
                               (game_state.pixelsPerSquare, game_state.pixelsPerSquare))

    def __repr__(self):
        return(f"<grid pos: ({self.gridX}, {self.gridY}), direction: {self.direction}, rect: {self.rect}>")

    def move(self, gridXMove: int, gridYMove: int, pixelsPerSquare: int):
        self.gridX += gridXMove
        self.gridY += gridYMove

        self.rect.x = helper.gridToPixels(self.gridX, pixelsPerSquare)
        self.rect.y = helper.gridToPixels(self.gridY, pixelsPerSquare)
