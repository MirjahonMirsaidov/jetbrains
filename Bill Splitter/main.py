from random import choice
people = {}
lucky_one = None
number_of_people = int(input("Enter the number of friends joining (including you):\n"))
if number_of_people > 0:
    print("\nEnter the name of every friend (including you), each on a new line:")
    for i in range(number_of_people):
        person = input()
        people[person] = 0
        
    print("\nEnter the total bill value:")
    total_bill = int(input())
    
    print("\nDo you want to use the \"Who is lucky?\" feature? Write Yes/No:")
    is_lucky = input()
    if is_lucky == "Yes":
        lucky_one = choice(list(people.keys()))
        print(f"{lucky_one} is the lucky one!")
        number_of_people -= 1
    elif is_lucky == "No":
        print("No one is going to be lucky")
    single_bill = round(total_bill / number_of_people, 2)
    people = {key: (single_bill if not key == lucky_one else 0) for key in people.keys()}
    print('\n', people, sep='')
    
else:
    print("\nNo one is joining for the party")
