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
    file.write(str(current_account.password) + "\n")
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
    print("logged into " + current_account.name)
    global main_screen
    main_screen = create_screen()
    add_label(main_screen, current_account.name)
    add_label(main_screen, str(current_account.balance))
    login_screen.destroy()
    main_screen.tkraise()
    #refresh(0.1, "Successfully logged in!")

def createAcc(n):
    #n = input("Please enter a name for the new account:")
    if n.lower() in (name.lower() for name in accounts):
        save()
        #refresh(0, "An account already exists with that name!")
    else:
        #pw = hash(input("Please enter a password for this account:"))
        global current_account
        current_account = account(n, 0)
        for asset in investments:
            current_account.portfolio[asset] = 0
        for skill in skills:
            current_account.expertise[skill] = 0
        save()
        #refresh(0.1, "Successfully created account!")

def read_accounts():
    global accounts
    accounts = []
    for filename in os.listdir(path):
        if filename.endswith(".acc"):
            name = os.path.split(filename)[1].split(".")[0]
            #file = open(os.path.join(path, filename), "r")
            #pw = file.readline().rstrip()
            accounts.append(name) # new addition
            #file.close() 


###GUI

root = Tk()

def hello():
    print("hello!")

menubar = Menu(root)

# login screen

login_screen = Frame(root, background = "", height = HEIGHT, width = WIDTH)
login_screen.pack()

# Account list
account_list = Listbox(login_screen)
account_list.pack(side = "left")
read_accounts()
for name in accounts:
    print (name)
    account_list.insert(END, name)

# Login button
login_button = Button(login_screen, text = "Log in", command = lambda: load_account(accounts[account_list.curselection()[0]]))
login_button.pack()

# New account button
new_account_button = Button(login_screen, text = "New account", command = createAcc)
new_account_button.pack()

# main screen
def create_screen():
    screen = Frame(root, background = "", height = HEIGHT, width = WIDTH)
    screen.pack()
    return screen

def add_label(master, str):
    label = Label(master, textvariable = str)
    label.pack()
    return label


# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)



# display the menu
root.config(menu=menubar)

root.mainloop()