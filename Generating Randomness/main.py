from random import choice
data = ''
triads = ["000", "001", "010", "011", "100", "101", "110", "111"]
balance = 1000
style = {}


# getting user input to learn their styling for guessing next inputs
def get():
    global data
    print("Please give AI some data to learn...")
    while len(data) < 100:
        print(f"Current data length is {len(data)}, {100-len(data)} symbols left")
        inp = input("Print a random string containing 0 or 1:\n\n")
        for i in inp:
            if i in ['0', '1']:
                data += i
        if len(data) >= 100:
            break


# preprocess user input for statistics
def preprocess():
    global style
    style = {i: [0, 0] for i in triads}
    final_list = [data[symbol:symbol + 4] for symbol in range(len(data) - 3)]

    for i in final_list:
        triad = i[:3]
        if i[3] == '0':
            style[triad][0] += 1
        else:
            style[triad][1] += 1


# check if users input is valid
def is_valid(inp):
    check = True
    for i in inp:
        if i not in ['1', '0']:
            check = False
            break
    return check


# guess users input based on their previous data via statistics
def guess(test_string):
    global balance
    prediction = choice(triads)
    succesfull_guesses = 0
    for i in range(len(test_string) - 3):
        last_three = test_string[i:i + 3]
        zeros = style[last_three][0]
        ones = style[last_three][1]
        predicted_number = '1' if ones > zeros else '0'
        prediction += predicted_number
        if test_string[i + 3] == predicted_number:
            succesfull_guesses += 1
        if predicted_number == '1':
            style[last_three][1] += 1
        else:
            style[last_three][0] += 1
    total_guesses = len(test_string) - 3
    acc = round(succesfull_guesses * 100 / total_guesses, 2)  # percentage of correct guesses
    balance = balance - succesfull_guesses + (total_guesses - succesfull_guesses)
    return prediction, succesfull_guesses, total_guesses, acc


if __name__ == '__main__':
    get()
    preprocess()
    print("\nFinal data string:\n", data, '\n', sep='')
    print("""You have $1000. Every time the system successfully predicts your next press, you lose $1.
Otherwise, you earn $1. Print "enough" to leave the game. Let's go!\n""")
    while True:
        print("Print a random string containing 0 or 1:")
        test_string = input()
        if is_valid(test_string):
            prediction, succesfull_guesses, total_guesses, acc = guess(test_string)
            print("prediction\n", prediction, sep='')
            print(f"\nComputer guessed right {succesfull_guesses} out of {total_guesses} symbols ({acc} %)")
            print(f"Your balance is now ${balance}\n")
        elif test_string == 'enough':
            break
    print("Game over!")
