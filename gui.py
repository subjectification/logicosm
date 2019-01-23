from tkinter import *

import datetime
import math
import random
import os
import sys
import readchar
import random
import colorama

### CONFIG
accounts = []
prizes = []
investments = ["FOOD", "HOUSE", "CLOTH"]
skills = ["ADDITION", "SUBTRACTION", "MULTIPLICATION", "DIVISION"]
threshold = 100 # when to unlock next skill
combo = 0       # increases chance of receiving reward
combo_increment = 5
current_skill = skills[0]
base_chance = 10
max_chance = 60
beep = '\a'


ranks = [colorama.Fore.YELLOW + "RECRUIT" + colorama.Fore.RESET,
    colorama.Fore.BLUE + "APPRENTICE" + colorama.Fore.RESET,
    colorama.Fore.CYAN + "ADEPT" + colorama.Fore.RESET,
    colorama.Fore.MAGENTA + "EXPERT" + colorama.Fore.RESET,
    colorama.Fore.GREEN + "ORACLE" + colorama.Fore.RESET]
if not os.path.exists("accounts"):
    os.mkdir("accounts")
#path = os.path.dirname(os.path.abspath(__file__))

path = os.path.abspath("accounts")

password = "abc"

###BACKEND

def save():
    file = open(os.path.join(path,current_account.name + ".acc"), "w")
    file.write(str(current_account.balance) + "\n")
    for asset in current_account.portfolio:
        file.write("i," + asset + "," + str(current_account.portfolio[asset]) + "\n")
    for skill in current_account.expertise:
        file.write("e," + skill + "," + str(current_account.expertise[skill]) + "\n")
    file.close()

class account:
    def __init__(self, input, bal):
        self.name = input
        self.balance = bal
        self.portfolio = {}
        self.expertise = {}

    def add(self, amount):
        self.balance += amount
        save()
    
    def subtract(self, amount):
        self.balance -= amount
        save()
		
    def buy(self, ticker, number):
        price = calcPrice(ticker,0) * number
        if self.balance >= price:
            self.subtract(price)
            self.portfolio[ticker] += number
            save()
            #refresh(3.1, "Successfully purchased " + str(number) + " " + ticker)
        else:
            save()#refresh(3.1, "Sorry, you don't have enough money :(")
    
    def sell(self, ticker, number):
        #printAcc()
        owned = self.portfolio[ticker]
        if owned >= number:
            self.subtract(number * calcPrice(ticker,0))
            self.portfolio[ticker] -= number
            save()
            #refresh(3.2, "Successfully sold " + number + " " + ticker)
        else:
            save()
            #refresh(3.2, "You don't own that many :(")
            
    def experience(self, skill, xp):
        self.expertise[skill] += xp
        save()

def load_account(name):
    global current_account
    filename = os.path.join(path, name) + ".acc"
    file = open(filename, "r")
    current_account = account(name, int(file.readline()))
    for asset in investments:
        current_account.portfolio[asset] = 0
    for skill in skills:
        current_account.expertise[skill] = 0
    for line in file:
        lst = line.split(",")
        if lst[0] == 'i':
            t = lst[1]
            if t in investments:
                current_account.portfolio[t] = int(lst[2])
        elif lst[0] == 'e':
            s = lst[1]
            current_account.expertise[s] = int(lst[2])
    raise_main()

def raise_main():
    global name_label
    global balance_label
    name_label = Label(main_screen, text=current_account.name)
    balance_label = Label(main_screen, text = str(current_account.balance))
    name_label.grid(row=0,column = 1)
    balance_label.grid(row=1,column=1)
    main_screen.tkraise()

def createAcc():
    n = name_entry.get()
    if n.lower() in (name.lower() for name in accounts):
        tk.messagebox.showerror("Error", "That account name already exists, please choose a unique name")
        name_entry.delete(0,END)
    else:
        global current_account
        current_account = account(n, 0)
        for asset in investments:
            current_account.portfolio[asset] = 0
        for skill in skills:
            current_account.expertise[skill] = 0
        save()
        raise_main()

def read_accounts():
    global accounts
    accounts = []
    for filename in os.listdir(path):
        if filename.endswith(".acc"):
            name = os.path.split(filename)[1].split(".")[0]
            accounts.append(name)

def learn():
    learning_activity.tkraise()
    fst = random.randint(0,9)
    snd = random.randint(0,9)
    q = ""
    if current_skill == '1':    # Addition
        q = str(fst) + " + " + str(snd) + " = ?"
        ans = fst+snd
    elif current_skill == '2':   # Subtraction
        q = str(fst) + " - " + str(snd) + " = ?"
        ans = fst-snd
    elif current_skill == '3':  # Multiplication
        q = str(fst) + " x " + str(snd) + " = ?"
        ans = fst*snd
    elif current_skill == '4':  # Division
        snd = random.randint(1,9)
        q = str(fst) + " / " + str(snd) + " = ?"
        ans = fst/snd
    global question
    question = Label(learning_activity, text=q)
    question.grid(row=0,column=0)
    global answer
    answer = Entry(learning_activity)
    answer.grid(row=1,column=0)

def check_answer: #TODO

def another_question: #TODO

def back_to_learning: #TODO

###GUI

root = Tk()


# login screen
login_screen = Frame(root)
login_screen.grid(row=0,column=0,sticky='news')

# Account list
account_list = Listbox(login_screen)
read_accounts()
for name in accounts:
    account_list.insert(END, name)
account_list.grid(row=0,column=0, rowspan=2)

# Login button
Button(login_screen, text = "Log in", command = lambda: load_account(accounts[account_list.curselection()[0]])).grid(row=0,column=1)

# Create account screen
create_acc_screen = Frame(root)
create_acc_screen.grid(row=0,column=0,sticky='news')

# Create Account button (on login screen)
Button(login_screen, text = "Create account", command = create_acc_screen.tkraise).grid(row=1,column=1)

# Create account button (on create account screen)
Button(create_acc_screen, text="Create account!", command = createAcc).grid(row=1,column=0)

# Name text entry field
name_entry = Entry(create_acc_screen)
name_entry.grid(row=0,column=0)

# Main screen
main_screen = Frame(root)
main_screen.grid(row=0,column=0,sticky='news')

# Main to learning button
Button(main_screen, text="Learning path", command = learning_main.tkraise).grid(row=0,column=0)


# Learning main screen
learning_main = Frame(main_screen)
learning_main.grid(row=0,column=0,sticky="NEWS")

#Learning screen button(s)
for index,skill in enumerate(skills):
    if skill == "ADDITION":
        Button(learning_main, text=skill, command=lambda: learn(skill)).grid(row=index, column=0)
    elif current_account.expertise[skills[index-1]] >= threshold:
        Button(learning_main, text=skill, command=lambda: learn(skill)).grid(row=index, column=0)

# Learning activity screen
learning_activity = Frame(learning_main)
learning_activity.grid(row=0, column=0, sticky="NEWS")

# Learning activity buttons
Button(learning_activity, text="Check answer", command = check_answer).grid(row=0,column=1)
Button(learning_activity, text="Another question", command = another_question).grid(row=1,column=1)
Button(learning_activity, text="Go back", command = back_to_learning).grid(row=2,column=1)

# Main to prizes button
Button(main_screen, text="Prizes", command = prizes_main.tkraise).grid(row=1,column=0)

# Main to exchange button
Button(main_screen, text="Exchange", command = exchange_main.tkraise).grid(row=2,column=0)

# Main to Achievements button
Button(main_screen, text="Achievements", command = achievements_main.tkraise).grid(row=3,column=0)



login_screen.tkraise()
root.mainloop()