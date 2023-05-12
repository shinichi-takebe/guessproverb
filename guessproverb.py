#This program is written by Shinichi Takebe, and I will write a program for a guess proverb game.

#I will provide my design, implement, and test explanation here, instead of Proj1_reflection.pdf.

"""
1.The main function will contain the game loop, which will keep running as long as the user wants to
play the game. It also  updates the user's stats, such as rounds played, rounds won, and average letter reveals.
2.Implement the getRandomProverb function: This function reads a list of proverbs from a text file
and returns a random proverb. It uses the 'random' module to generate a random index to select a proverb from the list.
3.Implement the checkwiththeproverb function: This function checks if the user's input is correct,
either a letter or a word, and updates the hidden proverb accordingly. It also updates the letter reveals
and misses based on the user's input.
4.Implement the getLetter function: This function returns the most common unrevealed letter
 in the proverb, which will be revealed to the user when they make a wrong guess.
5.Implement the showRound function: This function displays the current status of the game,
including the hidden proverb, letter reveals, and misses.
6.Implement the Game function: This function contains the main game loop, where it
initializes the game variables, calls the necessary functions to get a random proverb,
and sets up the hidden proverb. The user inputs their guesses, and the function continues to
update the hidden proverb and game status until the game is won or lost.
"""


#I will import a random function.
from random import *

def main():
    # main() function: This function is the main function that runs the game.
    # It initializes variables for the hidden proverb, number of letter reveals,
    # player's guess, and number of misses. It selects a random proverb using the
    # getRandomProverb() function and builds an initial hidden proverb with underscores
    # in place of letters. The game  continues until the player has used all of
    # their letter reveals or has correctly guessed the hidden proverb. In each loop
    # iteration, the showRound() function is called to display the current game state
    # to the player, and the player is prompted to enter a guess. The checkwiththeproverb()
    # function is called to update the hidden proverb based on the player's guess, and
    # the hidden_proverb variable is updated. If the player has correctly guessed the
    # proverb, a message is printed, and the game ends. Otherwise, if the player
    # has used all of their letter reveals, a message indicating the game has ended is
    # printed. Finally, the player's game statistics (number of rounds
    # played, rounds won, and average number of letter reveals) are printed.
    proverb = getRandomProverb()
    if proverb[-1] == '.':
        proverb = proverb[:-1]
    hidden_proverb, letter_reveals, guess, misses = '', 0, '', 0
    max_reveals = len(proverb.split())
    print(proverb)
    #Build initial hidden proverb with same number of underscores as actual proverb
    for i in range(len(proverb)):
        if proverb[i].isalpha():
            hidden_proverb += '~'
        else:
            hidden_proverb += proverb[i]
    status = False
    while letter_reveals < max_reveals:
        showRound(hidden_proverb, letter_reveals, misses)
        guess = input("Put your guess here: ")
        changedPart, letter_reveals, misses = checkwiththeproverb(hidden_proverb, letter_reveals, guess, misses, proverb)
        hidden_proverb = changedPart
        if '~' not in hidden_proverb:
            print(f"\nCongratulations, you won this round!\n")
            status = True
            break
        if letter_reveals >= max_reveals:
            print(f"\nSorry, you lost. Too many letter reveals.\n")
            status = False
    print(f"The answer was :{proverb}")
    return status, letter_reveals, max_reveals

    option = "Y"
    game, roundWon, total_letter_reveals, total_max_reveals = 0, 0, 0, 0
    while option == "Y":
        status, letter_reveals, max_reveals = Game()
        game += 1
        total_max_reveals += max_reveals
        total_letter_reveals += letter_reveals
        average = total_letter_reveals/total_max_reveals
        if status:
            roundWon += 1
        print(f"Your stats so far:\nRounds played: {game}\nRounds won: {roundWon}\nAverage letter reveals: {average}\n")
        option = input("Do you want to play again (Y/N): ")
    # getRandomProverb() function: This function reads a text file called "proverbs.txt"
    # that contains a list of proverbs, chooses a random index between 0 and the number of proverbs - 1,
    # selects the proverb at that index, and returns it with whitespace removed.

def getRandomProverb():
    with open("proverbsfull.txt", "r") as file:
        proverbs = file.readlines()
        random_index = randint(0, len(proverbs) - 1)
        return proverbs[random_index].strip()

#checkwiththeproverb(hidden_proverb, letter_reveals, guess, misses) function:
# This function takes in the current hidden proverb, the number of letter reveals so far,
# the player's guess, and the number of misses so far. It splits the guess into individual
# words and checks if each word appears in the hidden proverb. If a word in the guess is
# found in the hidden proverb, all occurrences of the word in the hidden proverb are replaced
# with the guessed word. If a guessed word is not found in the hidden proverb, the number of
# letter reveals increases and the hidden proverb is updated using the changeTheHiddenProverb()
# function. Finally, the updated hidden proverb, number of letter reveals, and number of misses
# are returned at the end.
def checkwiththeproverb(hidden_proverb, letter_reveals, guess, misses, proverb):
    changedPart = hidden_proverb.split()
    guess = guess.split()
    if guess == []:
        letter_reveals += 1
        changedPart = ' '.join(changedPart)
        changedPart = list(changedPart)
        letter = getLetter(proverb, hidden_proverb)
        for i in range(len(proverb)):
            if letter == proverb[i]:
                changedPart[i] = proverb[i]
        changedPart = ''.join(changedPart)
        misses += 1
    else:
        for g in guess:
            if g.lower() in proverb.lower():
                words = proverb.split()
                for i in range(len(words)):
                    if words[i].lower() == g.lower() or words[i].lower() == g.lower() +  ',' or words[i].lower() == g.lower() +  ';' :
                        changedPart[i] = words[i]
                #replace all occurrences of the word
            else:
                letter_reveals += 1
                changedPart = ' '.join(changedPart)
                changedPart = list(changedPart)
                hidden_proverb = ''.join(changedPart)
                letter = getLetter(proverb, hidden_proverb)
                for i in range(len(proverb)):
                    if letter == proverb[i]:
                        changedPart[i] = proverb[i]
                changedPart = ''.join(changedPart)
                changedPart = changedPart.split()
                misses += 1
        changedPart = ' '.join(changedPart)
    return changedPart, letter_reveals, misses

#getLetter(hidden_proverb) function: This function takes in the current hidden proverb and
# finds all uppercase letters in the proverb. It randomly selects one of these letters and
# replaces it with the lowercase version of the letter. The updated hidden proverb is returned.

def getLetter(proverb, hidden_proverb):
    unrevealed_letters = {}
    for i in proverb:
        if i.isalpha() and i not in hidden_proverb:
            if i.lower() not in unrevealed_letters:
                unrevealed_letters[i.lower()] = 1
            else:
                unrevealed_letters[i.lower()] += 1
    letter = list(unrevealed_letters)
    letter.sort(key = lambda char: unrevealed_letters[char])
    return letter[0]

#unrevealed_letters is a dictionary with key = character of the proverb and value = number of appearances
#unrevealed is a list of characters from the proverb, when you list(dictionary), you get the list of its keys
#lambda is a nameless function, it's similar to this:
#def lambda(char):
#    return unrevealed_letters[char]
#that means for char in unrevealed,
#the system will understand char as the value you return in the function, which is unrevealed_leters[char] in this case
#and the system will sort based on the values you provided


#showRound(hidden_proverb, letter_reveals, misses) function:
# This function takes in the current hidden proverb, the number
# of letter reveals so far, and the number of misses so far, and
# prints these values.
def showRound(hidden_proverb, letter_reveals, misses):
    print(f"\nHidden proverb: {hidden_proverb}")
    print(f"Letter reveals: {letter_reveals} / {len(hidden_proverb.split())}")
    print(f"Misses: {misses}\n")


if __name__ == "__main__":
    main()



