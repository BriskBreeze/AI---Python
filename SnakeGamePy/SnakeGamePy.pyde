import random as r
from FoodPiece import FoodPiece
from SnakePart import SnakePart
from Input import Input
import neurons
from Snake import Snake, tile_size, snakes, attackMode

paused = False;

screen_gcd = int()

rate = 10
generation = 0
direction = 0 # Down = 2, Left = 3, Right = 1, Up = 0
highscores = []

maxDist = 0.0

population = neurons.Population()
population.new_species()



def keyReleased():
    snakes[0].input.ChangeState(keyCode, False)
    pass

def keyPressed():
    global rate, paused
    snakes[0].input.ChangeState(keyCode, True)
    if (keyCode == 32):
        paused = not paused
    elif (keyCode == 107 or keyCode == 61):
        rate += 10
    elif ((keyCode == 109 or keyCode == 45) and rate > 10):
        rate -= 10;
    pass
def setup():
    size(800, 800)
    colorMode(HSB, 360)
    # fullScreen()
    frameRate(rate)
    noStroke()
    highscores.append(0.0)
    UpdateScreen()
    StartGame()

def draw():
    global generation
    if not paused:
        alldead = True
        for snake in snakes:
            if not snake.dead:
                alldead = False
                snake.AImove(SnakePart(snake.food.X, snake.food.Y))
                snake.lifeSpan -= 1
                snake.getDirection()
                snake.Update()
            if snake.getFitness() > highscores[generation]:
                highscores[generation] = snake.getFitness()
        if alldead:
            highscores.append(0.0)
            generation += 1
            population.generation()
            for species in population.species:
                species.distance_check()
            print(population.species)
            StartGame()
    frameRate(rate)
    UpdateScreen()

def GCD(a, b):
    return a if b == 0 else GCD(b, a % b)

def StartGame():
    global snakes
    screen_gcd = GCD(width, height)
    tile_size = screen_gcd / 2 if screen_gcd > 64 else screen_gcd
    while tile_size > 64:
        tile_size /= 2
    while tile_size < 32:
        tile_size *= 2
    tile_size = 50

    max_tile_w = width / tile_size
    max_tile_h = height / tile_size

    snakes = [] 
      
    for species in population.species:
        for network in species.current_generation:
              snakes.append(Snake(network))
    '''for i in range(snakeCnt):
        snakes.append(Snake())
    ''' 
    UpdateScreen()

def UpdateScreen():
    background(0);
    for snake in snakes:
        if not snake.dead:
            snake.display()
    fill(0, 0, 360);
    text("Generation: " + str(generation), 4, 16);
    text("Programmed by Jeffrey Holzman", 4, 32);
    text("Approxamate updates a second: " + str(rate), 4, 48);
    text("HighScore: " + str(highscores[generation]), (width / 2) - ((11 + (len(str(highscores[generation])))) / 2), 16)