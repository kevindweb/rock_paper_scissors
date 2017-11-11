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
win_loss = ''
# the next two variables show the user is
# playing smart or predictable
suspicion = False
predictable = True
ai_data = {'list': {'r': 0, 'p': 0, 's': 0}, 'majority': None, 'lose_r': None, 'lose_p': None, 'lose_s': None,
           'after_draw': None, 'win_r': None, 'win_p': None, 'win_s': None}
ai_count = 0
rps_list = ['rock', 'paper', 'scissors']
db = sql.connect('./my_data.db')
cursor = db.cursor()
print("Please enter the information below to begin.")


def update_data(username_field, games_played_field, other_data_field):
    if games_played_field:
        cursor.execute("UPDATE rps_data SET games_played=? WHERE username=?", (games_played_field, username_field))
    if other_data_field:
        other_data_field = str(other_data_field)
        cursor.execute("UPDATE rps_data SET other_data=? WHERE username=?", (other_data_field, username_field))
    db.commit()


def insert_account(insert_username, insert_pass):
    cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (insert_username, insert_pass))
    db.commit()


def insert_data(username_field, games_played_field):
    cursor.execute("INSERT INTO rps_data VALUES (?, ?, ?)", (username_field, games_played_field, '[]'))


def ai_function(all_data):
    global ai_data
    for my_rps in ai_data['list']:
        ai_data['list'][my_rps] = 0
    draws_dict = {'r': 0, 'p': 0, 's': 0}
    losses_dict_r = {'r': 0, 'p': 0, 's': 0}
    losses_dict_p = {'r': 0, 'p': 0, 's': 0}
    losses_dict_s = {'r': 0, 'p': 0, 's': 0}
    wins_dict_r = {'r': 0, 'p': 0, 's': 0}
    wins_dict_p = {'r': 0, 'p': 0, 's': 0}
    wins_dict_s = {'r': 0, 'p': 0, 's': 0}
    for data_thing in range(0, len(all_data)):
        ai_data['list'][all_data[data_thing][0]] += 1
        # get all the users plays
        if data_thing is not len(all_data) - 1:
            if all_data[data_thing][2] == 'd':
                draws_dict[all_data[data_thing + 1][0]] += 1
            if all_data[data_thing][2] == 'w':
                if all_data[data_thing][0] == 'r':
                    losses_dict_r[all_data[data_thing + 1][0]] += 1
                elif all_data[data_thing][0] == 'p':
                    losses_dict_p[all_data[data_thing + 1][0]] += 1
                else:
                    losses_dict_s[all_data[data_thing + 1][0]] += 1
            else:
                if all_data[data_thing][0] == 'r':
                    wins_dict_r[all_data[data_thing + 1][0]] += 1
                elif all_data[data_thing][0] == 'p':
                    wins_dict_p[all_data[data_thing + 1][0]] += 1
                else:
                    wins_dict_s[all_data[data_thing + 1][0]] += 1
    ai_data['win_r'] = sorted(wins_dict_r, key=wins_dict_r.__getitem__, reverse=True)[0]
    ai_data['win_p'] = sorted(wins_dict_p, key=wins_dict_p.__getitem__, reverse=True)[0]
    ai_data['win_s'] = sorted(wins_dict_s, key=wins_dict_s.__getitem__, reverse=True)[0]
    ai_data['lose_r'] = sorted(losses_dict_r, key=losses_dict_r.__getitem__, reverse=True)[0]
    ai_data['lose_p'] = sorted(losses_dict_p, key=losses_dict_p.__getitem__, reverse=True)[0]
    ai_data['lose_s'] = sorted(losses_dict_s, key=losses_dict_s.__getitem__, reverse=True)[0]
    ai_data['after_draw'] = sorted(draws_dict, key=draws_dict.__getitem__, reverse=True)[0]
    ai_data['majority'] = sorted(ai_data['list'], key=ai_data['list'].__getitem__, reverse=True)[0]


def opposite_rps(rps):
    # return what would win against this play (if rock, play paper)
    if rps == 'r':
        return 'paper'
    elif rps == 'p':
        return 'scissors'
    else:
        return 'rock'


def print_data(which_data):
    loss_num = 0
    win_num = 0
    draw_num = 0
    if len(which_data) < 1:
        return "Not enough data to print."
    for data_thing in range(0, len(which_data)):
        if which_data[data_thing][2] == 'w':
            loss_num += 1
        elif which_data[data_thing][2] == 'l':
            win_num += 1
        else:
            draw_num += 1
    percentage_num = 100 * (float(win_num) / (win_num + loss_num))
    return "All previous data (draws amount to 0 in total percentage...): \n Total draws: " + \
        str(draw_num) + "\n Total wins: " + str(win_num) + "\n Total losses: " + str(loss_num) + \
        "\n Total percentage: " + str(win_num) + " / " + str(win_num + loss_num) + " (" + \
           str(round(percentage_num, 2)) + "%)"


def letter_to_word(letter):
    if letter == 'r':
        return 'rock'
    elif letter == 'p':
        return 'paper'
    else:
        return 'scissors'


def who_wins(user, computer):
    global win_loss
    if user == computer:
        win_loss = 'd'
        return "There was a draw with " + user
    elif user == 'rock' and computer == 'paper':
        win_loss = 'w'
        return "Computer wins with " + computer
    elif user == 'scissors' and computer == 'rock':
        win_loss = 'w'
        return "Computer wins with " + computer
    elif user == 'paper' and computer == 'scissors':
        win_loss = 'w'
        return "Computer wins with " + computer
    else:
        win_loss = 'l'
        return "User wins with " + user
while True:
    played = raw_input("You have played this program before? True or False: ")
    if played == "True" or played == "t" or played == "T" or played == "true":
        played = True
        break
    elif played == "False" or played == "f" or played == "F" or played == "false":
        played = False
        break
if not played:
    username = raw_input("Create username:  ")
    password = raw_input("Create password:  ")
    insert_account(username, password)
    insert_data(username, 0)
    data_list.append([])
while played:
    username = raw_input("Enter username:  ")
    password = raw_input("Enter password:  ")
    cursor.execute("SELECT * FROM accounts WHERE username=? and password=?", (username, password, ))
    for row in cursor.fetchall():
        if row[0] == username and row[1] == password:
            cursor.execute("SELECT * FROM rps_data WHERE username=?", (username, ))
            for thing in cursor.fetchall():
                data_list[0][0] = thing[1]
                my_stringify_array = ast.literal_eval(thing[2])
                data_list.append(my_stringify_array)
                break
            stop_loop = True
            break
    if stop_loop:
        break
    print("Please try again")
print "Welcome:  %s" % username
# iterating rock paper scissors game
while True:
    if count == 0:
        print("Whenever prompted, you may type 'quit' to exit the game...")
        print("You may also type 'info' to see all your past plays")
        print("Otherwise, type 'r' for rock, 's' for scissors, or 'p' for paper.")
        computer_turn = rps_list[randint(0, 2)]
    else:
        if data_list[0][0] < 11:
            computer_turn = rps_list[randint(0, 2)]
        else:
            if ai_count % 5 == 0:
                ai_function(data_list[1])
            if data_list[1][-1][2] and data_list[1][-2][2] and data_list[1][-3][2] == 'l':
                if suspicion:
                    predictable = False
                else:
                    suspicion = True
            if data_list[1][-1][2] == 'l':
                if data_list[1][-1][0] == 'r':
                    computer_turn = opposite_rps(ai_data['win_r'])
                    if ai_data['win_r'] == '':
                        computer_turn = opposite_rps(data_list[1][-1][0])
                elif data_list[1][-1][0] == 'p':
                    computer_turn = opposite_rps(ai_data['win_p'])
                    if ai_data['win_p'] == '':
                        computer_turn = opposite_rps(data_list[1][-1][0])
                else:
                    computer_turn = opposite_rps(ai_data['win_s'])
                    if ai_data['win_s'] == '':
                        computer_turn = opposite_rps(data_list[1][-1][0])
            elif data_list[1][-1][2] == 'd':
                computer_turn = opposite_rps(ai_data['after_draw'])
            else:
                if data_list[1][-1][0] == 'r':
                    computer_turn = opposite_rps(ai_data['lose_r'])
                    if ai_data['lose_r'] == '':
                        computer_turn = opposite_rps(ai_data['majority'])
                elif data_list[1][-1][0] == 'p':
                    computer_turn = opposite_rps(ai_data['lose_p'])
                    if ai_data['lose_p'] == '':
                        computer_turn = opposite_rps(ai_data['majority'])
                else:
                    computer_turn = opposite_rps(ai_data['lose_s'])
                    if ai_data['lose_s'] == '':
                        computer_turn = opposite_rps(ai_data['majority'])
            ai_count += 1
    while True:
        user_turn = raw_input("Rock, Paper, Scissors... Shoot!  ")
        if user_turn == 'r' or user_turn == 'p' or user_turn == 's' or user_turn == 'quit':
            break
        elif user_turn == 'info':
            print(print_data(data_list[1]))
            print("")
        else:
            print("Please type one of the options or 'quit' or 'info'...")
    if user_turn == 'quit':
        break
    if user_turn == 'r':
        user_turn = 'rock'
    elif user_turn == 'p':
        user_turn = 'paper'
    else:
        user_turn = 'scissors'
    print("User Response: " + user_turn)
    print("Computer Response:  " + str(computer_turn))
    print(who_wins(user_turn, computer_turn))
    data_list[0][0] += 1
    count += 1
    my_list_data = [user_turn[0], computer_turn[0], win_loss]
    data_list[1].append(my_list_data)
print("You played %i games this time!" % count)
print("Have a nice day!")
update_data(username, data_list[0][0], str(data_list[1]))
cursor.close()
db.close()
