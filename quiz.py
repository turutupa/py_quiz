import requests
import json
import pprint as p
import random
import sys
import time
from termcolor import colored 
import html

def ask_category(retry=False):
    categories = {
        "Any Category":"any",
        "General Knowledge": "9",
        "Entertainment: Books": "10",
        "Entertainment: Film": "11",
        "Entertainment:Music": "12",
        "Entertainment: Musicals & Theatres": "13",
        "Entertainment: Television": "14",
        "Entertainment: Video Games": "15",
        "Entertainment: Board Games": "16",
        "Entertainment: Comics": "29",  
        "Entertainment: Japanese Anime & Manga": "31",
        "Entertainment: Cartoon & Animations": "32",
        "Science & Nature": "17",
        "Science: Computers": "18",
        "Science: Mathematics": "19",
        "Science: Gadgets": "30",
        "Mythology": "20",
        "Sports": "21",
        "Geography": "22",
        "History": "23",
        "Politics": "24",
        "Art": "25",
        "Celebrities": "26",
        "Animals": "27",
        "Vehicles": "28",
    }

    print(colored("\nPlease select a Category", "red"))
    print("\n** Select category by typing in the number")

    categories_list = []

    for index, category in enumerate(categories):
        categories_list.append(category)
        if not retry:
            print(index, category)

    selected_category = input("\n")

    try:
        int(selected_category)
    except:
        return ask_category(True)
    
    if int(selected_category.strip()) <= len(categories_list):
        print("Fantastic!! You've selected", categories_list[int(selected_category.strip())])
        return categories[categories_list[int(selected_category.strip())]]
    else:
        ask_category(True)
    
def ask_difficulty():
    print( colored("\nPlease select difficulty level!", "red"))
    difficulties = ["easy", "medium", "hard"]

    for i,d in enumerate(difficulties):
        print(i, d)
    
    selected_difficulty = input("\n")

    try:
        int(selected_difficulty)
    except:
        return ask_difficulty()

    if int(selected_difficulty) >= 0 and int(selected_difficulty) <= 2:
        print("\nGreat!!! You have chosen", difficulties[int(selected_difficulty)])
        return difficulties[int(selected_difficulty)]
    else:
        print("\nPlease select a difficulty")
        return ask_difficulty()

def get_question(difficulty, category):
    try:
        if category != "any":
            category_filter = 'category='
        else:
            category_filter = ''
        quiz_url = f"https://opentdb.com/api.php?amount=1&{category_filter}{category}&difficulty={difficulty}&type=multiple"
        r = requests.get(quiz_url)
        return json.loads(r.text)
    except Exception:
        print("\nOops!!Something went wrong!!")
        print(Exception)
        return sys.exit(0)

def play_game():
    while True:
        user_input = ""
        games_played = 0
        correct_answers = 0
        waiting_time_between_questions = 1.5
        exit_message = ['quit', 'exit']
        print(colored("\nWELCOME TO QUIZ TIME!!!", "red"))
        print("\nWe hope you enjoy it and have a great time!!! Let's start! ")
        time.sleep(1.5)


        category = ask_category()
        difficulty = ask_difficulty()
       

        while user_input.lower() not in exit_message:
            
            question = get_question(difficulty, category)

            # init array of answers with the incorrect ones
            answers = question['results'][0]['incorrect_answers']

            # save the index of the correct answer to later verification
            correct_answer_index = random.randint(0,2)

            # insert the correct answer randomly in answers
            answers.insert(correct_answer_index, question['results'][0]['correct_answer'])
            
            print("\n")
            print(colored(html.unescape(question['results'][0]['question']), 'red'))
            print("** Type 1,2,3 or 4 to select an answer\n")

            for index, answer in enumerate(answers):
                print(index + 1, html.unescape(answer))

            print(colored("\n** You may exit by typing 'quit' or 'exit'", "white"))
            print(colored("** You my type 'score' to check your current score", "white"))
            
            user_input_placeholder = "\nYour Answer: "
            user_input = input(user_input_placeholder).strip()

            while user_input.strip() == '':
                user_input = input(user_input_placeholder)
            
            while user_input == 'score':
                print("\nYour score is", str(correct_answers) + '/' + str(games_played))
                user_input = input(user_input_placeholder)

            try:
                int_user_answer = int(user_input.strip())
            except:
                int_user_answer = 'Fuck'

            if user_input == "quit" or user_input == 'exit':
                print(user_input.strip())
                print("Hope to see you soon!!")
            elif int_user_answer == correct_answer_index + 1:
                print(colored("Oleee! You got it right!, \nLets keep playing!", 'green'))
                correct_answers = correct_answers + 1
                games_played = games_played + 1
                time.sleep(waiting_time_between_questions)
            else:
                print(colored("Oops! So bad, better luck next time!", 'red'))
                print(colored("Right answer was " + question['results'][0]['correct_answer'] + '!', 'red'))
                games_played = games_played + 1
                time.sleep(waiting_time_between_questions)

        play_again = ''

        while play_again != 'y' or play_again != 'n':
            play_again = input("\nDo you want to play another game? (y/n)\n")

            response_yes = ['y', 'Y', 'yes']
            response_no = ['n', 'N', 'no']
            
            if play_again.strip().lower() in response_yes:
                play_game()
            elif play_again.strip().lower() in response_no:
                sys.exit(0)
            else:
                play_again = input('')