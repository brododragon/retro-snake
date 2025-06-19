from multipledispatch import dispatch
from collections.abc import Iterable

def areOppDirection(j, k):
    return abs(j - k) == 2

def gridToPixels(j, pixelsPerSquare):
    return j * pixelsPerSquare

def pixelsToGrid(j, pixelsPerSquare):
    return j / pixelsPerSquare

@dispatch(int, int, int)
def gridToPixelsVec(x, y, pixelsPerSquare):
    return [gridToPixels(x, pixelsPerSquare), gridToPixels(y, pixelsPerSquare)]

@dispatch(Iterable, int)
def gridToPixelsVec(arr, pixelsPerSquare):
    return [gridToPixels(arr[0], pixelsPerSquare), gridToPixels(arr[1], pixelsPerSquare)]

@dispatch(int, int, int)
def pixelsToGridVec(x, y, pixelsPerSquare):
    return [pixelsToGrid(x, pixelsPerSquare), pixelsToGrid(y, pixelsPerSquare)]

@dispatch(Iterable, int)
def pixelsToGridVec(tup, pixelsPerSquare):
    return [pixelsToGrid(tup[0], pixelsPerSquare), pixelsToGrid(tup[1], pixelsPerSquare)]

class vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f"vec({self.x}, {self.y})"

    def __tuple__(self): # Doesn't work, says "vector object is not iterable"
        return (self.x, self.y)
    
    def __eq__(self, other):
        return isinstance(other, vector) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
