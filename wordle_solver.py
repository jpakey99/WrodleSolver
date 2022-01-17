def word_list():
    words = []
    word_file = open('words.txt')

    for word in word_file:
        words.append(word.strip())

    return words

