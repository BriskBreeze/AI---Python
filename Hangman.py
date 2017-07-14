from __future__ import print_function
import numpy
import random
"""from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'YOUR API KEY HERE'
client = swagger.ApiClient(apiKey, apiUrl)"""


def draw_gallows(stage):
    gallows = [ # the template of the gallows
        "____________",
        "|-----------",
        "|-/    |    ",
        "|/          ",
        "|           ",
        "|           ",
        "|           "
    ]
    arms = "-"
    if stage >= 1: #change the gallows image based on the current amount of lives lost
        gallows[3] = change_letter(gallows[3], "O", 7)
    if stage >= 2:
        gallows[4] = change_letter(gallows[4], "|", 7)
    if stage >= 3:
        gallows[4] = change_letter(gallows[4], arms[numpy.random.randint(0,len(arms))], 6)
    if stage >= 4:
        gallows[4] = change_letter(gallows[4], arms[numpy.random.randint(0,len(arms))], 8)
    if stage >= 5:
        gallows[5] = change_letter(gallows[5], "/", 6)
    if stage >= 6:
        gallows[5] = change_letter(gallows[5], "\\", 8)

    # displays the gallows
    for line in gallows:
        print(line)

def draw_word(word, guessed): # displays the word and blank underneath the gallows
    finished = True # default flag
    for letter in word:
        if letter in guessed: # goes through each letter and checks to see if its in the guessed list.  if so, display letter, if not, an underscore
            print(letter, end = " ")
        else:
            print("_", end = " ") # if you didn't finish the word, set finished to False
            finished = False
    if finished:
        print()
        print("You Win!") # win message
        exit(0)
    print()

def draw_guessed(guessed): # displays guessed characters
    print("Guessed: ", end = "")
    for letter in guessed:
        print(letter, end = "")
    print()

def change_letter(word, character, index): # replace letter in string given parent string, replacement char and an index
    new_word = list(word)
    new_word[index] = character
    return ''.join(new_word)

def display(stage, word, guessed): # runs all draw methods
    draw_guessed(guessed)
    draw_gallows(stage)
    draw_word(word, guessed)

def player_move(guessed): # input from a human
    guess = ""
    while not guess.isalpha() or guess in guessed or guess == "":
        guess = raw_input("Guess a letter: ")[0].lower()
    return guess

def AI_move(guessed, word, letter_count): # gets result form the AI
    sorted_dict = sorted(letter_count.items(), key=lambda x:x[1])[::-1]
    return sorted_dict[len(guessed)][0]

def AI_train(training_set): # trains the AI
    letter_cnt = {} # empty dict
    for word in training_set:
        for letter in word:
            if letter in letter_cnt: # count each letter in the training set and if its a new alphabet, create a new key
                letter_cnt[letter] += 1
            else:
                letter_cnt[letter] = 1
    return letter_cnt

stage = 0 # full lives
guessed = [] # empty guess list

f = open("E:\Programming\Projects\Python 2.7.13\DukeTiP\words_alpha.txt") # dir for the word dictionary
words = f.read().splitlines() # splits the file into words and loads them into a list

numpy.random.shuffle(words) # shuffles the list
word = words[0] # sets word to first word in words

training_set = words[::10] # gets every tenth word
letter_count = AI_train(training_set)

while stage < 6: # you get 6 lives
    display(stage, word, guessed)
    #guess = player_move(guessed) # user guess
    guess = AI_move(guessed, word, letter_count) # AI guess
    print(guess)
    guessed.append(guess) # adds guess to guess list
    if guess not in word: # if wrong, go up in stage
        stage+=1

display(stage, word, guessed) # refreshes the screen
print("Game Over!") # game over message
print("Your word was: " + word)
