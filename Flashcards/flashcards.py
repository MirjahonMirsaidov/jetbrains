import random
from io import StringIO

mem_buffer = StringIO()

FLASH_CARDS = {}


# find the dictionary key by its value
def find_term_by_key(key, value):
    terms = []
    for term, val in FLASH_CARDS.items():
        if val[key] == value:
            terms.append(f'"{term}"')
    return ', '.join(terms)


# log and print at the same time
def log_and_print(message):
    global mem_buffer
    # mem_buffer.read()
    mem_buffer.write(message + '\n')
    print(message)


# create a new flashcard with a unique term and definition
def add():
    global FLASH_CARDS
    log_and_print("The card:")
    term = input()
    while True:
        if term in FLASH_CARDS.keys():
            log_and_print(f'The card "{term}" already exists. Try again:')
            term = input()
        else:
            break
    log_and_print("The definition of the card:")
    definition = input()
    while True:
        if definition in [i['definition'] for i in FLASH_CARDS.values()]:
            log_and_print(f'The definition "{definition}" already exists. Try again:')
            definition = input()
        else:
            break

    FLASH_CARDS.update({
        term: {
            'definition': definition,
            'mistakes': 0
        }
    })
    log_and_print(f'The pair ("{term}":"{definition}") has been added.')


# remove certain flashcard
def remove():
    global FLASH_CARDS
    log_and_print("Which card?")
    card = input()
    if card in FLASH_CARDS.keys():
        FLASH_CARDS.pop(card)
        log_and_print("The card has been removed.")
    else:
        log_and_print(f"Can't remove \"{card}\": there is no such card.")


# import flashcards from a file
def importt():
    log_and_print("File name:")
    file_name = input()
    try:
        with open(file_name, 'r') as f:
            count = 0
            for line in f:
                term, definition, mistakes = line.split()
                FLASH_CARDS.update({
                    term: {
                        'definition': definition,
                        'mistakes': mistakes
                    }
                })
                count += 1
            log_and_print(str(count) + ' cards have been loaded.')
    except FileNotFoundError:
        log_and_print("File not found.")


# write all flashcards to a file
def export():
    log_and_print("File name:")
    file_name = input()
    with open(file_name, 'w') as f:
        for term in FLASH_CARDS.keys():
            f.write(term + ' ' + FLASH_CARDS[term]['definition'] + ' ' + str(FLASH_CARDS[term]['mistakes']) + '\n')
    log_and_print(f"{len(FLASH_CARDS)} cards have been saved.")


# ask the user about the number of cards they want and then prompt them for definitions
def ask():
    log_and_print("How many times to ask?")
    play_time = int(input())
    n = 0
    while n < play_time:
        key = random.choice(list(FLASH_CARDS.keys()))
        value = FLASH_CARDS[key]['definition']
        log_and_print(f'Print the definition of "{key}":')
        definition = input()
        if definition == value:
            log_and_print("Correct")
        elif definition in [x['definition'] for x in FLASH_CARDS.values()]:
            log_and_print(
                f"""Wrong. The right answer is "{value}", \
                but your definition is correct for {find_term_by_key('definition', definition)}.""")
            FLASH_CARDS[key]['mistakes'] += 1
        else:
            log_and_print(f'Wrong. The answer is "{value}"')
            FLASH_CARDS[key]['mistakes'] += 1
        n += 1


def log():
    log_and_print("File name:")
    file_name = input()
    with open(file_name, 'a') as f:
        content = mem_buffer.getvalue()
        f.write(content)
    mem_buffer.truncate(0)
    print("The log has been saved.")


def hardes_card():
    if not FLASH_CARDS:
        log_and_print("There are no cards with errors.")
    else:
        number_of_mistakes = [x['mistakes'] for x in FLASH_CARDS.values()]
        most_mistakes = max(number_of_mistakes)
        if most_mistakes == 0:
            log_and_print("There are no cards with errors.")
        elif number_of_mistakes.count(most_mistakes) < 2:
            log_and_print(f"""The hardest card is "{find_term_by_key('mistakes', most_mistakes)}". \
            You have {most_mistakes}  errors answering it.""")
        elif number_of_mistakes.count(most_mistakes) > 1:
            log_and_print(f"""The hardest cards are {find_term_by_key('mistakes', most_mistakes)}. \
            You have {most_mistakes} errors answering them.""")


def reset_stats():
    for term, inner_dict in FLASH_CARDS.items():
        inner_dict['mistakes'] = 0
    log_and_print("Card statistics have been reset.")


while True:
    log_and_print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    action = input()
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
    elif action == 'log':
        log()
    elif action == 'hardest card':
        hardes_card()
    elif action == 'reset stats':
        reset_stats()
    elif action == "exit":
        print("Bye bye!")
        mem_buffer.close()
        break
