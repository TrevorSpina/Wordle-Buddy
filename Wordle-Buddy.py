from typing import List, Any

# lookup table of letter frequencies in the english language.
# in alphabetical order i.e. index 0 is the frequency of A and
# index 25 is the frequency of Z.
letter_frequencies = [8.12,
                      1.49,
                      2.71,
                      4.32,
                      12.02,
                      2.3,
                      2.03,
                      5.92,
                      7.31,
                      0.1,
                      0.69,
                      3.98,
                      2.61,
                      6.95,
                      7.68,
                      1.82,
                      0.11,
                      6.02,
                      6.28,
                      9.1,
                      2.88,
                      1.11,
                      2.09,
                      0.17,
                      2.11,
                      0.07]

def getKey(guesses):
    return guesses[1]

def makeGuesses():
    print("Simply make at least one guess in the game and then fill in some")
    print("information and Wordle Buddy will try to come up with a good guess.")
    print("Type \"quit\" at any time to quit.")
    print()
    while True:
        should_quit = False
        print("which letters, if any, do you know the position of? (Green Letters)")
        print("Type the letters you know separated by -\'s for letters you do not know the position of. (Non-Green Letters)")
        print("For example, if you only know that the word ends in an \"r\", type \"----r\".")
        green_invalid = True
        green_letters_string = ""
        while green_invalid:
            green_letters_string = input().lower()
            if green_letters_string == "quit":
                should_quit = True
                break
            elif len(green_letters_string) == 5:
                green_invalid = False
            else:
                print("Word should be 5 characters long")
        if should_quit:
            break
        known_letters = []
        for char in green_letters_string:
            if ord(char) != 32:
                # ignore spaces
                known_letters.append(char)

        print()
        print("Now, type all of the letters that could be in the secret word.")
        print("Type all of the letters that are not grayed out separated by commas.")
        letters_valid = False
        while letters_valid == False:
            letters_valid = True
            valid_letters_string = input().lower()
            if valid_letters_string == "quit":
                should_quit = True
                break
            valid_letters = valid_letters_string.split(",")
            for letter in valid_letters:
                if len(letter) != 1:
                    letters_valid = False
                    print("There must be a comma between each letter")
                    break
                elif ord(letter) < 97 or ord(letter) > 122:
                    letters_valid = False
                    print("Only enter letters")
                    break
        if should_quit:
            break
        print()
        print("Great! Now, what letters do you know are in the word and where in the word are they not located? (Yellow Letters)")
        print("Similar to before with the green letters, type in the yellow letters separated by -\'s.")
        print("Positions of Yellow letters from previous guesses that are now green can be ignored.")
        print("type \"done\" when you are done, and \"clear\" to delete the words you already typed.")
        not_done = True
        yellow_letters_string_list = []
        while not_done:
            yellow_letters_input = input().lower()
            if yellow_letters_input == "quit":
                should_quit = True
                break
            input_valid = True
            if yellow_letters_input == "done":
                not_done = False
                break
            elif yellow_letters_input == "clear":
                yellow_letters_string_list.clear()
                print("Cleared.")
            elif len(yellow_letters_input) != 5:
                input_valid = False
                print("Word should be 5 characters long")
            if input_valid:
                yellow_letters_string_list.append(yellow_letters_input)
        if should_quit:
            break
        print()
        print("Okay, so we know", green_letters_string, ", the possible letters are:", end=" ")
        for letter in valid_letters:
            print(letter, end=", ")
        print()
        print("and we know these letters are present, but not in these locations:", end=". ")

        for yellow_letters_string in yellow_letters_string_list:
            print(yellow_letters_string, end=" ")
        print("Is this correct? (y/n)")
        correct_input = input().lower()
        correct = False
        correct_valid = False
        while correct_valid == False:
            if correct_input == "y":
                correct_valid = True
                print("Great!")
                correct = True
            elif correct_input == "n":
                correct_valid = True
                print("Let's try that again.")
            elif correct_input == "quit":
                break
            else:
                print("please enter y or n")
        if correct:
            print("Finding possible guesses...")
            possible_guesses_file = open("possible_guesses.txt", "a+")
            possible_guesses_file.truncate(0) # clear text file
            guesses_count = 0
            valid_guesses = []
            five_letter_words_file = open("five_letter_words.txt")
            # iterate through word list
            for word in five_letter_words_file:
                #print("now checking " + word[:5] + "...")
                # check if word is valid guess
                # add to file if it is
                trimmed_word = word[:5]
                valid_guess = True
                for pos in range(5):
                    # validate against green letters
                    if known_letters[pos] != "-":
                        if word[pos] != known_letters[pos]:
                            valid_guess = False
                            #print("invalid: " + word[pos] + " at postion: " + str(pos))
                            break
                    # validate against all valid letters
                    if valid_letters.count(word[pos]) == 0:
                        # word contains invalid letter
                        valid_guess = False
                        #print("invalid letter: " + word[pos] + " at position: " + str(pos))
                        break
                if valid_guess:
                    # validate against yellow letters
                    for yellow_letters_string in yellow_letters_string_list:
                        for pos in range(5):
                            char = yellow_letters_string[pos]
                            if char != "-":
                                if word.count(char) == 0:
                                    # word does not contain yellow letter
                                    #print("invalid: " + word + " does not contain yellow letter: " + char)
                                    valid_guess = False
                                if char == word[pos]:
                                    # letter is in word but not in this position (yellow letter)
                                    #print("invalid: " + word[pos] + " is not at postion: " + str(pos))
                                    valid_guess = False

                if valid_guess:
                    # add tuple to list
                    valid_guesses.append((trimmed_word, calculateWeight(trimmed_word, green_string=green_letters_string)))

                    guesses_count += 1
            print()
            print("possible guesses:")
            for guess in sorted(valid_guesses, key=getKey, reverse=True):
                write_string = guess[0] + ", " + str(guess[1]) + "\n"
                possible_guesses_file.write(write_string)
                print(guess[0] + ", " + str(guess[1]))
            print(guesses_count, "possible guesses were found.")
            possible_guesses_file.close()
            print()
            print("Do you want to generate another set of guesses? (y/n)")
            again_input = input().lower()
            again_valid = False
            while again_valid == False:
                if again_input == "y":
                    again_valid = True
                elif again_input == "n":
                    again_valid = True
                    should_quit = True
                elif again_input == "quit":
                    again_valid = True
                    should_quit = True
                    break
                else:
                    print("please enter y or n")
            if should_quit:
                break

def calculateWeight(word, green_string = "-----"):
    # sum letter weights
    weight_sum = 0
    previous_letters = []
    for pos in range(5):
        letter = word[pos]
        index = ord(letter) - 97
        if index > 0 and index < 26:
            # character is a lowercase ascii letter
            if previous_letters.count(letter) == 0:
                # letter does not occur previously in the word
                if green_string[pos] != letter:
                    # letter is not already known
                    weight_sum += letter_frequencies[index]
            else:
                # letter occurs previously in the word
                weight_sum *= 0.25
        previous_letters.append(letter)
    return weight_sum

def bestFirstGuess():
    five_letter_words_file = open("five_letter_words.txt")
    maxWeight = 0
    maxWord = ""
    print("finding best first guess...")
    for word in five_letter_words_file:
        trimmed_word = word[:5]
        curr_weight = calculateWeight(trimmed_word)
        if curr_weight > maxWeight:
            maxWeight = curr_weight
            maxWord = word
    print("The best first guess is:", maxWord + ": " + str(maxWeight))
    five_letter_words_file.close()

def main():
    print()
    print(" ___ ___ _______ _______ ______   ___     _______     _______  ___ ___ ______   ______  ___ ___ ")
    print("|   Y   |   _   |   _   |   _  \ |   |   |   _   |   |   _   \|   Y   |   _  \ |   _  \|   Y   |")
    print("|.  |   |.  |   |.  l   |.  |   \|.  |   |.  1___|   |.  1   /|.  |   |.  |   \|.  |   |   1   |")
    print("|. / \  |.  |   |.  _   |.  |    |.  |___|.  __)_    |.  _   \|.  |   |.  |    |.  |    \_   _/ ")
    print("|:      |:  1   |:  |   |:  1    |:  1   |:  1   |   |:  1    |:  1   |:  1    |:  1    /|:  |  ")
    print("|::.|:. |::.. . |::.|:. |::.. . /|::.. . |::.. . |   |::.. .  |::.. . |::.. . /|::.. . / |::.|  ")
    print("`--- ---`-------`--- ---`------' `-------`-------'   `-------'`-------`------' `------'  `---'  ")
    print("")
    print("Wordle Buddy will help you solve today's Wordle!")

    while(True):
        print()
        print("-------------------------------------------------------------------------------------------------")
        print("|  Options:                                                                                     |")
        print("|    Type \"first guess\" to get a good first guess.                                              |")
        print("|    Type \"smart guess\" to generate a list of possible guesses given what you already know.     |")
        print("|    Type \"quit\" to quit.                                                                       |")
        print("-------------------------------------------------------------------------------------------------")
        print()
        usr_input = input().lower()

        if usr_input == "first guess":
            bestFirstGuess()
        elif usr_input == "smart guess":
            makeGuesses()
        elif usr_input == "quit":
            break

main()