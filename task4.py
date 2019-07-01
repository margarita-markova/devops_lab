def chck_word_length(word):
    global count
    count = count + len(word)
    if count >= 10 ** 6:
        return False
    else:
        return True


if __name__ == '__main__':
    count = 0
    n = 0
    while (1 <= n <= 10 ** 5) is False:  # conditionals checking
        n = int(input())

    result = {}  # dictionary with results

    for i in range(n):
        word = input()
        word = word.lower()
        if chck_word_length(word) is False:  # check common length of words
            break
        if result.get(word):
            result[word] = result.get(word) + 1  # counting the words
        else:
            result[word] = 1  # adding new key-value pair in dictionary

    print(len(result))
    for value in result.values():
        print(value, end=' ')
