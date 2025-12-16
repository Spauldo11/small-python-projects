import numpy as np
import time
import math

# map so every number can represent a letter
map_letters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!']
print('Enter the number of rows in your key matrix: ')
key_rows = int(input())
key_columns = key_rows
# establishes the key matrix
def establish_matrix(): 
    
    key = []
    # the key matrix is always square, so number of rows is all you need
    print('You will now begin entering the numbers inside of your key matrix')
    print('Please enter every number in your matrix starting from left to right, top to bottom: ')
    time.sleep(1)
    for i in range(key_rows):
        row = []
        for j in range(key_columns):
            row.append(int(input()))
        key.append(row)

    print('This is your matrix. Is this correct? Y/N or press \'q\' to quit')
    for i in range(key_rows):
        for j in range(key_columns):
            print(key[i][j], end=" ")
        print()
    ans = input()
    if ans.lower() == 'y':
        encoded_message(key)
    elif ans.lower() == 'n':
        establish_matrix()
    else:
        print('Sorry I couldn\'t help you this time. Maybe try again later!')

# establishes what the encoded message is
def encoded_message(key):
    length = int(input('How many numbers are in your encoded message: '))
    encoded_rows = int(math.ceil(length / key_rows))
    encoded_message = []
    map_message = []
    # np.array() allows for me to find the inverse of it and multiply with it using built in functions
    key_arr = np.array(key)
    print('Please enter all of the numbers in your encoded message. After each number, press the return key')
    if (encoded_rows * key_rows > length):
        print("Please the number zero to fill in empty spaces. There should only be one or two")
    # sorts the encoded message into individual arrays to be multiplied with later
    for i in range(encoded_rows):
        row = []
        for j in range(key_rows):
            row.append(int(input()))
        encoded_message.append(row)
    # establishes the decoded numbers that map to the letters in the message
    for i in range(encoded_rows):
        current_mat = np.array(encoded_message[i])
        map_message.append(np.dot(np.linalg.inv(key_arr), current_mat))
    translate(map_message)

# translates the mapped numbers into words that you can read
def translate(map_message):
    final_message = []
    for i in range(len(map_message)):
        for j in range(len(map_message[i])):
            index = round(map_message[i][j])
            final_message.append(map_letters[index])
    print("Your message is: ")
    for i in range(len(final_message)):
        print(final_message[i], end='')

establish_matrix()