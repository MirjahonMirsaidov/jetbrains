import random

FLASH_CARDS = {}


# create a new flashcard with a unique term and definition
def add():
    global FLASH_CARDS
    term = input("The card:\n")
    while True:
        if term in FLASH_CARDS.keys():
            term = input(f'The card "{term}" already exists. Try again:\n')
        else:
            break
    definition = input("The definition of the card:\n")
    while True:
        if definition in FLASH_CARDS.values():
            definition = input(f'The definition "{definition}" already exists. Try again:\n')
        else:
            break

    FLASH_CARDS[term] = definition
    print(f'The pair ("{term}":"{definition}") has been added.')


# remove certain flashcard
def remove():
    global FLASH_CARDS
    card = input("Which card?\n")
    if card in FLASH_CARDS.keys():
        FLASH_CARDS.pop(card)
        print("The card has been removed.")
    else:
        print(f"Can't remove \"{card}\": there is no such card.")


# import flashcards from a file
def importt():
    file_name = input("File name:\n")
    try:
        with open(file_name, 'r') as f:
            count = 0
            for line in f:
                term, definition = line.split()
                FLASH_CARDS[term] = definition
                count += 1
            print(count, 'cards have been loaded.')
    except FileNotFoundError:
        print("File not found.")


# write all flashcards to a file
def export():
    file_name = input("File name:\n")
    with open(file_name, 'w') as f:
        for key, value in FLASH_CARDS.items():
            f.write(key + ' ' + value + '\n')
    print(f"{len(FLASH_CARDS)} cards have been saved.")


# find the dictionary key by its value
def find_key_by_value(value):
    for key, val in FLASH_CARDS.items():
        if val == value:
            return key


# ask the user about the number of cards they want and then prompt them for definitions
def ask():
    play_time = int(input("How many times to ask?\n"))
    n = 0
    while n < play_time:
        key = random.choice(list(FLASH_CARDS.keys()))
        value = FLASH_CARDS[key]
        definition = input(f'Print the definition of "{key}":\n')
        if definition == value:
            print("Correct")
        elif definition in FLASH_CARDS.values():
            print(
                f'Wrong. The right answer is "{value}", but your definition is correct for "{find_key_by_value(definition)}".')
        else:
            print(f'Wrong. The answer is "{value}"')
        n += 1


while True:
    action = input("Input the action (add, remove, import, export, ask, exit):\n")
    if action == "add":
        add()
    elif action == "remove":
        remove()
    elif action == "import":
        importt()
    elif action == "export":
        export()
    elif action == "ask":
        ask()
    elif action == "exit":
        print("Bye bye!")
        break
