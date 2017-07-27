from FoodPiece import FoodPiece
from SnakePart import SnakePart
from Input import Input
import neurons 
import random as r

snakes = []
tile_size = int(50)
attackMode = False

class Snake:
    def __init__(self, brain):
        self.input = Input()
        
        self.snake = []
        self.food = FoodPiece()
        self.direction = 0
        self.clr = color(random(360), 360, 360)
        self.dead = False
            
        self.score = 0
        self.scoreDist = 0.0
        
        self.max_tile_w = width / tile_size
        self.max_tile_h = height / tile_size
                
        self.brain = brain
        
        self.inputs = []
        self.outputs = []
        self.label = int()        
        
        self.lifeSpan = 50
        
        colorMode(HSB, 360)
        
        head = SnakePart(r.randint(0, self.max_tile_w - 1), r.randint(0, self.max_tile_h - 1))
        self.snake.append(head)
        self.direction = r.randint(0, 3)
        
        self.spawnFood()
        
    def IsGameOver(self, max_w, max_h):
        for x in range(max_w):
            for y in range(max_h):
                for snake in snakes:
                    for part in snake.snake:
                        if part.X != x and part.Y != y:
                            return False;
        return True;

    def Update(self):
        if self.lifeSpan <= 0:
            self.dead = True
            return
        for i in range(len(self.snake))[::-1]:
            if i == 0:
                if self.direction == 2: # Down
                    self.snake[0].Y += 1
                elif self.direction == 3: # Left
                    self.snake[0].X -= 1
                elif self.direction == 1: # Right
                    self.snake[0].X += 1
                elif self.direction == 0: # Up
                    self.snake[0].Y -= 1
                
                if self.snake[0].X < 0 or self.snake[0].X >= self.max_tile_w or self.snake[0].Y < 0 or self.snake[0].Y >= self.max_tile_h:
                    self.dead = True
                    
                for othersnake in snakes:
                    if not othersnake.dead:
                        if othersnake.snake != self.snake:
                            if not attackMode:
                                continue
                        for j in range(1, len(othersnake.snake)):
                            if self.snake[0].X == othersnake.snake[j].X and self.snake[0].Y == othersnake.snake[j].Y:
                                self.dead = True
                                othersnake.score += len(self.snake)
                
                if self.snake[0].X == self.food.X and self.snake[0].Y == self.food.Y:
                    #eating
                    part = SnakePart()
                    part.X = self.snake[len(self.snake) - 1].X
                    part.Y = self.snake[len(self.snake) - 1].Y
                    self.snake.append(part)
                    self.spawnFood()
                    self.score += 1
                    self.lifeSpan = 50
                    self.scoreDist = 0.0
            else:
                self.snake[i].X = self.snake[i - 1].X;
                self.snake[i].Y = self.snake[i - 1].Y;
        distance = (dist(self.snake[0].X, self.snake[0].Y, self.food.X, self.food.Y) - 1)
        distance **= -1 if distance > 0 else 0
        if (distance > self.scoreDist):
            self.scoreDist = distance
    
    def display(self):
        fill(self.clr)
        ellipse((self.food.X * tile_size + (tile_size / 2)) + 1, (self.food.Y * tile_size + (tile_size / 2)) + 1, tile_size - 2, tile_size - 2)
        
        for i in range(len(self.snake)):
            snake_color = color(hue(self.clr), map(i, 0, len(self.snake), 360, 0), 360)
            fill(snake_color)
            ellipse((self.snake[i].X * tile_size + (tile_size / 2)) + 1, (self.snake[i].Y * tile_size + (tile_size / 2)) + 1, tile_size - 2, tile_size - 2)
    
    def getDirection(self):
        if self.input.Pressed(39): # Right
            if len(self.snake) < 2 or self.snake[0].X == self.snake[1].X:
                self.direction = 1
                print('right')
        elif self.input.Pressed(37): # Left
            if len(self.snake) < 2 or self.snake[0].X == self.snake[1].X:
                self.direction = 3
                print('left')
        elif self.input.Pressed(38): # Up
            if len(self.snake) < 2 or self.snake[0].Y == self.snake[1].Y:
                self.direction = 0
                print('up')
        elif self.input.Pressed(40): # Down
            if len(self.snake) < 2 or self.snake[0].Y == self.snake[1].Y:
                self.direction = 2
                print('down')
        
    def spawnFood(self):
        self.food = FoodPiece()
        
        cont = True
        while cont:
            cont = False
            self.food.X = r.randint(0, self.max_tile_w - 1)
            self.food.Y = r.randint(0, self.max_tile_h - 1)
            for othersnake in snakes:
                if othersnake.snake != self.snake:
                    if not attackMode:
                        continue
                for i in range(len(othersnake.snake)):
                    if self.food.X == othersnake.snake[i].X and self.food.Y == othersnake.snake[i].Y:
                        cont = True
        self.food.val = 1
        
    def loadInputs(self):
        _inputs = [0.0] * ((width * height) / tile_size ** 2)
        for body in self.snake:
            _inputs[(body.Y * (width / tile_size) + body.X)] = .1 # self body
        _inputs[(self.snake[0].Y * (width / tile_size) + self.snake[0].X)] = .2 # self head
        _inputs[(self.food.Y * (width / tile_size) + self.food.X)] = .4 # self food
        
        return _inputs
    def getFitness(self):
        return self.score + self.scoreDist
    
    def AImove(self, _end):
        new_direction = r.randint(0, 3)
        
        self.input.ChangeState(38, False) # Up
        self.input.ChangeState(40, False) # Down
        self.input.ChangeState(39, False) # Right
        self.input.ChangeState(37, False) # Left
        
        self.inputs = self.loadInputs()
        self.outputs = self.brain.feed_forward(self.inputs)
        
        output = round(sort(self.outputs)[0], 1)
        print("Final Output: ", output)
        new_direction = (self.direction + output) % 4
        
        if new_direction == 2: # Down
            self.input.ChangeState(DOWN, True)
        elif new_direction == 3: # Left
            self.input.ChangeState(LEFT, True)
        elif new_direction == 1: # Right
            self.input.ChangeState(RIGHT, True)
        elif new_direction == 0: # Up
            self.input.ChangeState(UP, True)
        