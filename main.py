import datetime
import math
import random
import os
import sys
import readchar

accounts = []
investments = ["FOOD", "HOUSE", "CLOTH"]
state = 0
status = "Welcome!"

if not os.path.exists("accounts"):
    os.mkdir("accounts")
#path = os.path.dirname(os.path.abspath(__file__))

path = os.path.abspath("accounts")

password = "abc"




#nowdate = datetime.datetime.strptime(nowstring, "%Y-%m-%d %H:%M:%S.%f")

def hash(password):
    key = "1"*len(password)
    encrypted_int = [ord(a)^ord(b) for a,b in zip(password, key)]
    encrypted_string = "".join([str(a) for a in encrypted_int])
    return encrypted_string

def createMenu(items):
    selected = ">>>>>>>>  "
    deselected = "          "
    i = 0
    rtn = ""
    for item in items:
        if menustate == i:
            rtn = rtn + selected + menu[item]
            i += 1
        else:
            rtn += deselected + menu[item]
            i += 1
    return rtn

class account:
    def __init__(self, input, bal, pas):
        self.name = input
        self.password = pas
        self.balance = bal
        self.portfolio = {}
        global current_account
        current_account = self
        save()
	
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
            return 1
        return 0
    
    def sell(self, ticker, number):
        printAcc()
        owned = self.portfolio[ticker]
        if owned >= number:
            self.subtract(number * calcPrice(ticker,0))
            self.portfolio[ticker] -= number
            save()
            return 1
        return 0


def calcPrice(tick, history):
    today = datetime.datetime.now()
    difference = today - datetime.datetime(2000,1,1)
    num = difference.days - history
    return {
        investments[0] : (num % 2) + 1,
        investments[1] : (num % 3) + 2,
        investments[2] : int(round(math.sin(num)* 6 + 6))}[tick]
          

def read_database():
    global accounts
    accounts = []
    count = 0
    for filename in [os.path.abspath(os.path.join("accounts",x)) for x in os.listdir(path)]:
        if filename.endswith(".acc"):
            name = os.path.split(filename)[1].split(".")[0]
            file = open(filename, "r")
            if os.stat(filename).st_size == 0:
                accounts.append(account(name, 100,"password"))
            else:
                accounts.append(account(name, int(file.readline()), file.readline()))
            for asset in investments:
                accounts[count].portfolio[asset] = 0
            for line in file:
                lst = line.split(",")
                t = lst[0]
                if t in investments:
                    accounts[count].portfolio[t] = int(lst[1])
            count += 1
            file.close()    


def clear():
    os.system('cls||clear')

def printAcc():
    print (current_account.name + "'s balance: \t" + str(current_account.balance) + "\n")
    print (current_account.name + "'s portfolio:")
    for asset in current_account.portfolio:
        print (asset + ":\t\t\t" + str(current_account.portfolio[asset]))

def selected(num):
    out = blanks.copy()
    out[num] = cursor
    return out

def selectAcc():
    read_database()
    global current_account
    if len(accounts) > 0:
        print ("Which account would you like to access? Or press 'n' to create a new account")
        for count in range(len(accounts)):
            print(str(count) + ": " + accounts[count].name)
        n = input("")
        if n == "n":
            createAcc()
            return True
        elif any(x.name.lower() == n.lower() for x in accounts):
            n = [x for x in accounts if x.name.lower() == n.lower()]
            pw = hash(input("Please enter your password:"))
            if pw == n[0].password:
                current_account = n[0]
                return True
            else:
                return False
        elif str.isdigit(n):
            if int(n) <= len(accounts):
                pw = hash(input("Please enter your password:"))
                if pw == accounts[int(n)].password:
                    current_account = accounts[int(n)]
                    return True
                else:
                    return False
            return False
        else:
            return False
    else:
        print("No accounts detected!")
        createAcc()
        return True

def createAcc():
    acc = input("Please enter a name for the new account:")
    if any(x.name.lower() == acc.lower() for x in accounts):
        print("An account already exists with that name! Please choose a unique name.\n")
        createAcc()
    else:
        pw = hash(input("Please enter a password for this account:"))
        global current_account
        current_account = account(acc, 100, pw)
        for asset in investments:
            current_account.portfolio[asset] = 0

def printInvestments():
    print ("Today's investment prices:")
    for asset in investments:
        print (asset + ":\t\t\t" + str(calcPrice(asset,0)))

def save():
    file = open(os.path.join(path,current_account.name + ".acc"), "w")
    file.write(str(current_account.balance) + "\n")
    file.write(current_account.password + "\n")
    for asset in current_account.portfolio:
        file.write(asset + "," + str(current_account.portfolio[asset]) + "\n")
    file.close()

def quit():
    save()
    clear()
    sys.exit()

def refresh():
    clear()
    global status
    global state
    print(status + "\n\n")
    if state != 4:
        printInvestments()
        print("\n")
    if state != 0:
        printAcc()
        print("\n")
    (state, status) = dialogue()
    

def printHistory():
    for asset in investments:
        print (asset + " prices: ")
        for i in range(-1*int(hist_length),-1):
            print (str(calcPrice(asset,i)) + ", ", end="")
        print(str(calcPrice(asset,0)))
        

def dialogue():
    if state == 0:          # account not selected
        if selectAcc():
            return (1, "Successfully logged in!")
        else:
            return (0, "There was a problem with your username or password, please try again")
    if state == 1:           # accunt selected, main screen
        inp = input("Press 'b' to buy, 's' to sell, 'c' to change accounts, 'h' to check price history, '+' to add money (requires password), '-' to spend (requires password), or 'q' to save and quit.\n")
        if inp == '+':
            pw = input("Please enter the password to unlock this feature:")
            if pw != password:
                return (1, "Sorry! That is the wrong password!")
            num = input("How much would you like to add?\n")
            current_account.add(int(num))
            return (1, "Successfully added " + num)
        elif inp == '-':
            pw = input("Please enter the password to unlock this feature:")
            if pw != password:
                return (1, "Sorry! That is the wrong password!")
            num = input("How much would you like to spend?\n")
            if int(num) <= current_account.balance:
                current_account.subtract(int(num))
                return (1, "Successfully spent " + num + "!")
            else:
                return (1, "You don't have that much!")
        elif inp == 'b':
            return (2, "Shares: buying")
        elif inp == 's':
            return (3, "Shares: selling")
        elif inp == 'c':
            save()
            return (0, "Choose an account")
        elif inp == 'h':
            global hist_length
            hist_length = input("How many days back do you want to display prices for?")
            return (4, "Price history")
        elif inp == 'q':
            quit()
        else:
            return (1, "I don't know what that means!")
    if state == 2:          # buying shares
        t =  input("Which investment would you like to buy? Or press q to return to the main screen\n")
        if t == "q":
            return (1, "Welcome!\n\n")
        if t not in investments:
            return (2, "Please enter the name of a valid investment to purchase!")
        n = input("How much " + t + " would you like to buy? Or press q to return to the main screen\n")
        if n == "q":
            return (1, "Welcome!\n\n")
        done = current_account.buy(t.upper(), int(n))
        if done == 1:
            return (1, "Successfully purchased " + n + t.upper() + "!")
        else:
            return (2, "There was a problem with your purchase, please try again")
    if state == 3:          #selling shares
        t =  input("Which investment would you like to sell? Or press q to return to the main screen\n")
        if t == "q":
            return (1, "Welcome!")
        if current_account.portfolio[t] <= 0:
            return (3, "You do not have any of that investment to sell!")
        n = input("How much " + t + " would you like to sell? Or press q to return to the main screen\n")
        if n == "q":
            return (1, "Welcome!")
        done = current_account.sell(t.upper(), int(n))
        if done == 1:
            return (1, "Successfully sold " + n + t.upper() + "!")
        else:
            return (2, "There was a problem with your sale, please try again")
    if state == 4:       # checking price history
        printHistory()
        b = input("Select a new number of days to look back on, or press 'b' to go back to the main menu\n")
        if b == 'b':
            return (1, "Welcome!")
        else:
            if str.isdigit(b):
                hist_length = int(b)
            return (4, "Price history")
    
    
   
while True:
    refresh()