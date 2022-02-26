dictionary_words_file = open("dictionary.txt")
five_letter_words_file = open("five_letter_words.txt", "a+")
five_letter_words_file.truncate(0) # erase file contents

print("finding 5 letter words...")
word_count = 0
for word in dictionary_words_file:
    if len(word) == 6:
        trimmed_word = word[:5]
        print(trimmed_word)
        five_letter_words_file.write(word)
        word_count += 1

print("search complete.", word_count, "words were found.")

dictionary_words_file.close()
five_letter_words_file.close()