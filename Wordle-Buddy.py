from typing import List, Any

five_letter_words_file = open("five_letter_words.txt")

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
    print("Wordle Buddy will help you solve today's Wordle!")
    print()
    print("Simply make at least one guess in the game and then fill in some")
    print("information and Wordle Buddy will try to come up with a good guess.")
    print()
    while True:
        print("which letters, if any, do you know the position of? (Green Letters)")
        print("Type the letters you know separated by -\'s for letters you do not know the position of. (Non-Green Letters)")
        print("For example, if you only know that the word ends in an \"r\", type \"----r\".")
        green_invalid = True
        green_letters_string = ""
        while green_invalid:
            green_letters_string = input()
            if len(green_letters_string) == 5:
                green_invalid = False
            else:
                print("Word should be 5 characters long")
        known_letters = []
        for char in green_letters_string:
            if ord() != 32:
                # ignore spaces
                known_letters.append(char.lower())

        print()
        print("Now, type all of the letters that could be in the secret word.")
        print("Type all of the letters that are not grayed out separated by commas.")
        letters_valid = False
        while letters_valid == False:
            letters_valid = True
            valid_letters_string = input()
            valid_letters = valid_letters_string.split(",")
            for letter in valid_letters:
                if len(letter) != 1:
                    letters_valid = False
                    print("There must be a comma after each letter")
                    break
                if ord(letter) < 97 or ord(letter) > 122:
                    letters_valid = False
                    print("Only enter letters")
                    break
        print()
        print("Great! Now, what letters do you know are in the word and where in the word are they not located? (Yellow Letters)")
        print("Similar to before with the green letters, type in the yellow letters separated by -\'s.")
        print("Positions of Yellow letters from previous guesses that are now green can be ignored.")
        print("type \"Done\" when you are done, and \"Clear\" to delete the words you already typed.")
        not_done = True
        yellow_letters_string_list = []
        while not_done:
            yellow_letters_input = input()
            input_valid = True
            if yellow_letters_input.lower() == "done":
                not_done = False
                break
            elif yellow_letters_input.lower() == "clear":
                yellow_letters_string_list.clear()
            elif len(yellow_letters_input) != 5:
                input_valid = False
                print("Word should be 5 characters long")
            if input_valid:
                yellow_letters_string_list.append(yellow_letters_input)
        print()
        print("Okay, so we know", green_letters_string, ", the possible letters are:", end=" ")
        for letter in valid_letters:
            print(letter, end=", ")
        print()
        print("and we know these letters are present, but not in these locations:", end=". ")
        for yellow_letters_string in yellow_letters_string_list:
            print(yellow_letters_string, end=" ")
        correct_input = input("Is this correct? (y/n) ")
        correct = False
        if correct_input.lower() == "y":
            print("Great!")
            correct = True
        elif correct_input.lower() == "n":
            print("Let's try that again.")
        else:
            print("please enter y or n")
        if correct:
            print("Finding possible guesses...")
            # iterate through word list
            possible_guesses_file = open("possible_guesses.txt", "a+")
            possible_guesses_file.truncate(0) # clear text file if it already exists
            guesses_count = 0
            valid_guesses = []
            for word in five_letter_words_file:
                # check if word is valid guess
                # add to file if it is
                valid_guess = True
                for pos in range(5):
                    # validate against green letters
                    if known_letters[pos] != "-":
                        if word[pos] != known_letters[pos]:
                            valid_guess = False
                            break
                    # validate against all valid letters
                    if valid_letters.count(word[pos]) == 0:
                        # word contains invalid letter
                        valid_guess = False
                        break
                if valid_guess:
                    # validate against yellow letters
                    for yellow_letters_string in yellow_letters_string_list:
                        for pos in range(5):
                            char = yellow_letters_string[pos]
                            if char != "-":
                                if word.count(char) == 0:
                                    # word does not contain yellow letter
                                    valid_guess = False
                                if char == word[pos]:
                                    # letter is in word but not in this position (yellow letter)
                                    valid_guess = False

                if valid_guess:
                    # add tuple to list
                    valid_guesses.append((word[:5], calculateWeight(word[:5], green_string=green_letters_string)))

                    guesses_count += 1
            for guess in sorted(valid_guesses, key=getKey, reverse=True):
                write_string = guess[0] + ", " + str(guess[1]) + "\n"
                possible_guesses_file.write(write_string)
            print(guesses_count, "possible guesses were found.")
            possible_guesses_file.close()
            print("")

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
        curr_weight = calculateWeight(word[:5])
        if curr_weight > maxWeight:
            maxWeight = curr_weight
            maxWord = word
    print("The best first guess is:", maxWord[:5] + ": " + str(maxWeight))
    five_letter_words_file.close()

bestFirstGuess()
makeGuesses()