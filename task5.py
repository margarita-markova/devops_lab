if __name__ == '__main__':

    keyboard = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a',
                's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
                'v', 'b', 'n', 'm']

    try:
        letter = input()
        letter.strip()  # remove all spaces

        for i in letter:  # find the letter in case of 1233d
            if i.isalpha():
                letter = i
                break

        if letter.isupper():  # convert to lowercase in case of uppercase
            letter = letter.lower()

        place = keyboard.index(letter)
        place = place + 1
        if place >= len(keyboard):
            place = 0

        print(keyboard[place])

    except ValueError:
        print("Incorrect value: no one character is inputted")
