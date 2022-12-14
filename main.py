from re import T
import pygame
import random
import time

# Initialize
pygame.init()
pygame.mixer.init()

# Create screen
screen = pygame.display.set_mode((800,600))

# Set icon and title
pygame.display.set_caption("Color Pyramid")
icon = pygame.image.load('Assets/ColorPyramid.png')
pygame.display.set_icon(icon)

BG     = pygame.Color("#2A9D8F")
pink   = pygame.Color("#FF006E")
yellow = pygame.Color("#FFBE0B")
blue   = pygame.Color("#1663BE")


# 2D List representation of the board:
grid = [[BG,BG,BG,BG,BG,BG,BG,BG,BG],
        [BG,BG,BG,BG,BG,BG,BG,BG,BG],
        [BG,BG,BG,BG,BG,BG,BG,BG,BG],
        [BG,BG,BG,BG,BG,BG,BG,BG,BG],
        [BG,BG,BG,BG,BG,BG,BG,BG,BG]]

# List of cells that didn't satisfy the conditions:
badCells = []

# Create random game board
def initBoard ():
    for i in range (5):
        for j in range (4-i, 4+i+1):
            grid[i][j] = random.choice([pink, yellow, blue])
    drawBoard()

# Draw the current board 
def drawBoard():
    x = 265
    y = 100
    for i in range (5):
        for j in range (9):
            pygame.draw.rect(screen, grid[i][j], [x, y, 25, 25])
            x += 30
        x = 265
        y += 30

# Check for bad cells
def findBadCells(): 
    # Check yellow condition separately for the relevant rows:
    i = 4
    while i >= 2:
        if not yellowCondition(i):
            for t in range (4-i, 4+i+1):
                badCells.append([i,t])
        # If yellow condition is satisfied, check other coditions:
        else:
            for j in range (4-i, 4+i+1):
                if checkCell(i,j):
                    badCells.append([i,j])
        i -= 1
    # Now check rows 0,1:
    while i >= 0:
        for k in range (4-i, 4+i+1):
                if checkCell(i,k):
                    badCells.append([i,k])
        i -= 1


# The next four finctions are used to actually check the conditions.

# Check if row i has more than 4 yellow cells:
def yellowCondition(i):
    yellowCount = 0
    for j in range (4-i, 4+i+1):
        if grid[i][j] is yellow:
            yellowCount += 1
    if yellowCount > 4:
        return False
    else: 
        return True

# Check relevant conditions in *specific cells*: 
def checkCell(i,j):
    color = grid[i][j]
    if color is blue and blueCondition(i,j):
        return True
    elif color is pink and pinkCondition(i,j):
        return True
    return False

# Check if a blue cell is on the edge of the pyramid
def blueCondition(i,j):
    if i == 4 or j == -i + 4 or j == i + 4:
        return True
    else:
        return False

# Check if a pink cell has blue neighbors
def pinkCondition(i,j):
    up = i-1 if i > 0 else i
    down = i+1 if i < 4 else i
    left = j-1 if j > 0 else j
    right = j+1 if j < 8 else j

    adjacent = [grid[up][j], grid[down][j], grid[i][left], grid[i][right]]
    if blue in adjacent:
        return True
    else:
        return False


# Update cells that don't satisfy conditions
def updateBoard():
    for item in badCells:
        i = item[0]
        j = item[1]
        grid[i][j] = random.choice([pink, yellow, blue])
    badCells.clear()
    drawBoard()

def celebration():
    celebrationSound = pygame.mixer.Sound('Assets/TADA.ogg')
    celebrationSound.play()


# Set background color and initialize random board
screen.fill(BG)
initBoard()

# Game loop:
running = True
playing = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False          
    
    # Wait a moment
    time.sleep(0.01)

    # If the board doesn't satisfy all conditions, fix it
    findBadCells()
    if len(badCells) != 0:
        updateBoard()
    elif playing:
        celebration()
        playing = False
        
    pygame.display.update()