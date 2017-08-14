from random import randint
import ast
import sqlite3 as sql
print("Welcome to my Rock, Paper, Scissors game. Made by Kevin Deems.")
print('')
count = 0
stop_loop = False
data_list = [[0]]
username = ''
password = ''
rock_amount = 0
paper_amount = 0
scissors_amount = 0
rps_list = ['rock', 'paper', 'scissors']
db = sql.connect('./my_data.db')
cursor = db.cursor()
print("Please enter the information below to begin.")


def update_data(username_field, games_played_field, other_data_field):
    if username_field:
        cursor.execute("UPDATE rps_data SET username=?", (username_field, ))
    if games_played_field:
        cursor.execute("UPDATE rps_data SET games_played=?", (games_played_field, ))
    if other_data_field:
        other_data_field = str(other_data_field)
        cursor.execute("UPDATE rps_data SET other_data=?", (other_data_field, ))
    db.commit()


def insert_account(insert_username, insert_pass):
    cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (insert_username, insert_pass))
    db.commit()


def who_wins(user, computer):
    if user == computer:
        return "There was a draw with " + user
    elif user == 'rock' and computer == 'paper':
        return "Computer wins with " + computer
    elif user == 'scissors' and computer == 'rock':
        return "Computer wins with " + computer
    elif user == 'paper' and computer == 'scissors':
        return "Computer wins with " + computer
    else:
        return "User wins with " + user
while True:
    played = raw_input("You have played this program before? True or False: ")
    if played == "True":
        played = True
        break
    elif played == "False":
        played = False
        my_number = 4
        break
if not played:
    username = raw_input("Create username:  ")
    password = raw_input("Create password:  ")
    insert_account(username, password)
    # data_list['times_played'] = 0
while played:
    username = raw_input("Enter username:  ")
    password = raw_input("Enter password:  ")
    cursor.execute("SELECT * FROM accounts WHERE username=? and password=?", (username, password, ))
    for row in cursor.fetchall():
        if row[0] == username and row[1] == password:
            cursor.execute("SELECT * FROM rps_data WHERE username=?", (username, ))
            for thing in cursor.fetchall():
                data_list[0] = [thing[1]]
                my_stringify_array = ast.literal_eval(thing[2])
                data_list.append(my_stringify_array)
            stop_loop = True
            break
    if stop_loop:
        break
    print("Please try again")
print "Welcome:  %s" % username
while True:
    if count == 0:
        print("Whenever prompted, you may type 'quit' to exit the game...")
        print("Otherwise, type 'r' for rock, 's' for scissors, or 'p' for paper.")
        # if data_list['times_played'] == 0:
        # print("Since this is your first time, you get infinite tries to beat computer.")
        # print("Restart with same username when ready to try with 5 lives")
        print("We are now going to start rock, paper, scissors.")
    elif count > 20:
        break
    computer_turn = rps_list[randint(0, 2)]
    while True:
        user_turn = raw_input("Rock, Paper, Scissors... Shoot!  ")
        if user_turn == 'r' or user_turn == 'p' or user_turn == 's' or user_turn == 'quit':
            break
        else:
            print("Please type one of the options or 'quit'...")
    if user_turn == 'quit':
        break
    if user_turn == 'r':
        user_turn = 'rock'
        rock_amount += 1
    elif user_turn == 'p':
        user_turn = 'paper'
        paper_amount += 1
    else:
        user_turn = 'scissors'
        scissors_amount += 1
    print("User Response: " + user_turn)
    print("Computer Response:  " + str(computer_turn))
    print(who_wins(user_turn, computer_turn))
    count += 1
print("You played %i games this time!" % count)
print("Have a nice day!")
# data_list['times_played'] += 1
cursor.close()
db.close()

