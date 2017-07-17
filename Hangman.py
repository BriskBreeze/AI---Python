from __future__ import print_function
import numpy
import random
"""from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'YOUR API KEY HERE'
client = swagger.ApiClient(apiKey, apiUrl)"""

f = open("words_alpha.txt")
#f = open("20k.txt")
words = f.read().lower().splitlines() # splits the file into words and loads them into a list

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
            pass
            # print(letter, end = " ")
        else:
            #print("_", end = " ") # if you didn't finish the word, set finished to False
            finished = False
    if finished:
        print("You Win!") # win message
        return 1
    return 0

def draw_guessed(guessed): # displays guessed characters
    print("Guessed: ", end = "")
    for letter in guessed:
        if len(letter) == 1:
            print(letter, end = "")
    print()

def change_letter(word, character, index): # replace letter in string given parent string, replacement char and an index
    new_word = list(word)
    new_word[index] = character
    return ''.join(new_word)

def display(stage, word, guessed): # runs all draw methods
    # draw_guessed(guessed)
    # draw_gallows(stage)
    return draw_word(word, guessed)

def player_move(guessed): # input from a human
    guess = ""
    while not guess.isalpha() or guess in guessed or guess == "":
        guess = raw_input("Guess a letter: ")[0].lower()
    return guess

def AI_move(lcl_guessed, word, ngram_count, training_set): # gets result form the AI
    sorted_dict = sorted(ngram_count.items(), key=lambda x:x[1])[::-1]
    if len(lcl_guessed) == 0 or len(word) == 1:
        #print(sorted(AI_train(training_set, 1))[0])
        return sorted(AI_train(training_set, 1))[0]
    left_letter = ""
    right_letter = ""
    for i in xrange(len(word)):
        if word[i] not in lcl_guessed:
            if i == 0:
                if word[i+1] in lcl_guessed:
                    right_letter = word[i+1]
                else:
                    continue
            elif i == len(word)-1:
                if word[i-1] in lcl_guessed:
                    left_letter = word[i-1]
                else:
                    continue
            else:
                if word[i-1] in lcl_guessed:
                    left_letter = word[i-1]
                else:
                    continue
                if word[i + 1] in lcl_guessed:
                    right_letter = word[i + 1]
                else:
                    continue

    ngram1 = {}
    ngram2 = {}
    if not left_letter == "":
        for ngram in sorted_dict:
            if ngram[0][0] == left_letter and ngram not in lcl_guessed:
                ngram1 = ngram
                break
    if not right_letter == "":
        for ngram in sorted_dict:
            if ngram[0][1] == right_letter and ngram not in lcl_guessed:
                ngram2 = ngram
                break

    if not ngram1 == {} and not ngram2 == {}:
        if ngram1[1] > ngram2[1]:
            guessed.append(ngram1)
            return ngram1[0][1]
        else:
            guessed.append(ngram2)
            return  ngram2[0][0]
    elif not ngram1 == {}:
        guessed.append(ngram1)
        return ngram1[0][1]
    elif not ngram2 == {}:
        guessed.append(ngram2)
        return  ngram2[0][0]
    else:
        return sorted_dict[len(lcl_guessed)][0][0]

def AI_train(training_set, gramsize): # trains the AI
    ngram_cnt = {} # empty dict
    for word in training_set:
        for i in xrange(len(word) - gramsize):
            ngram = ""
            for j in xrange(gramsize):
                ngram += word[i+j]
        if ngram in ngram_cnt:
            ngram_cnt[ngram] += 1
        else:
            ngram_cnt[ngram] = 1

        """for letter in word:
            if letter in ngram_cnt: # count each letter in the training set and if its a new alphabet, create a new key
                ngram_cnt[letter] += 1
            else:
                ngram_cnt[letter] = 1"""

    return ngram_cnt

def filter(guess): # filters out words of the training data to make a better guess
    temp = ngram_count.copy()
    for key in temp:
        if guess in key:
            ngram_count.pop(key)

win = 0.0
loss = 0.0

for i in xrange(9999):
    won = False

    numpy.random.shuffle(words)  # shuffles the list
    # word = words[0] # sets word to first word in words
    stage = 0  # full lives
    guessed = []  # empty guess list
    word = words[0]

    training_set = words[::10]  # gets every tenth word
    ngram_count = AI_train(training_set, 2)
    while stage < 6:  # you get 6 lives
        if display(stage, word, guessed) == 1:
            win += 1
            won = True
            break
        # guess = player_move(guessed) # user guess
        guess = AI_move(guessed, word, ngram_count, training_set)  # AI guess
        if guess not in word and guess not in guessed:  # if wrong, go up in stage
            stage += 1
            filter(guess)
        guessed.append(guess.lower())  # adds guess to guess list

    if not won:
        display(stage, word, guessed)  # refreshes the screen
        print("Game Over!")  # game over message
        loss += 1
    print("Your word was: " + word)
    print(float(win) / ((float(loss) + float(win))))
