# PYGAME SNAKE

---

## INTRODUCTION & DESCRIPTION

Hello! This is the classic game *Snake*, built in Python with Pygame. It uses several scripts: First, there's main.py -- run this if you want to play the game. It includes most of the game logic, as well as all of the setup, and the game loop itself. Next, there's helper.py, snakeclasses.py, and snakemethods.py; these all supply methods and classes to main.py. helper.py supplies pretty general helper methods/classes, snakeclasses.py supplies Snake-specific classes (currently, just segment class), and snakemethods.py supples Snake-specific methods (like drawApple(), move(), drawScore(), etc.).

## RUNNING THE GAME

This game has not yet been packaged into an executable. Therfore, it will need to be ran on a computer and in an environment where python is installed (version 3.12.3). Some packages may need to be installed; likely, only `multipledispatch` will need to be installed -- this can be done via `pip`. To start the game, simply run `main.py`.
