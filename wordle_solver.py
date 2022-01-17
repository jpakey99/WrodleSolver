import re


def word_list():
    words = []
    word_file = open('words.txt')

    for word in word_file:
        words.append(word.strip())

    return words


def remove_char_words(char, words):
    for word in words:
        if re.search(char, word):
            words.remove(word)

    return words


def remove_char_after_index_words(index, char, words):
    new_words = []
    for word in words:
        if len([*re.finditer(char, word)]):
            new_words.append(word)
        elif re.search(char, word[index+1:]) is None:
            new_words.append(word)

    return new_words


def remove_char_index_words(index, char, words):
    new_words = []
    for word in words:
        res = re.search(char, word)
        if res is not None:
            if index != res.start():
                new_words.append(word)

    return new_words


def remove_all_but_char_at_index(index, char, words):
    new_words = []
    for word in words:
        # print(word)
        for i, c in enumerate(word):
            if i == index and c == char:
                new_words.append(word)

    return new_words


def refine_words(guessed_word_string, result_string, words):
    previous_c = []
    for i, c in enumerate(guessed_word_string):
        if result_string[i] == '0' and c not in previous_c:
            words = remove_char_words(c, words)
        elif result_string[i] == '0' and c in previous_c:
            words = remove_char_after_index_words(i, c, words)
        elif result_string[i] == '1':
            words = remove_char_index_words(i, c, words)
        elif result_string[i] == '2':
            words = remove_all_but_char_at_index(i, c, words)
        previous_c.append(c)
    return words


def get_probabilities(words):
    prob = {}
    for word in words:
        for i, c in enumerate(word):
            if c not in prob:
                prob[c] = {'0':0,
                           '1':0,
                           '2':0,
                           '3':0,
                           '4':0}
            prob[c][str(i)] += 1
    return prob


def guess_word(words):
    length = len(words)
    count = get_probabilities(words)
    current_champ_word, current_champ_amount = '', 0
    for word in words:
        word_likely_amount = 0
        for i, c in enumerate(word):
            word_likely_amount += (count[c][str(i)]/length)
            word_likely_amount += ((count[c]['0'] + count[c]['1'] + count[c]['2'] + count[c]['3'] + count[c]['4'])/length)
        if word_likely_amount > current_champ_amount:
            current_champ_amount = word_likely_amount
            current_champ_word = word
    return current_champ_word


def main():
    i = 0
    words = word_list()
    while i < 6:
        word = guess_word(words)
        result_string = input('Enter result string for word: ' + word)
        words = refine_words(word, result_string, words)
        if result_string == '22222':
            print('CONGRATS, you solved the puzzle')
            break


main()
# wordss = word_list()
# wordss = refine_words('sleep', '22201', wordss)
# wordss = remove_char_after_index_words(0, 'e', wordss)
# print(wordss)