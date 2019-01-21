import datetime
import math
import random
import os
import sys
import readchar

accounts = []
prizes = []
investments = ["FOOD", "HOUSE", "CLOTH"]
state = 0   # Which interface is displayed
            # 0: Choose account
            # 0.1: Main interface
            # 1: TODO: Learning path?
            # 2: TODO: Prizes?
            # 3: Exchange main page
            # 3.1: Exchange: buy investments
            # 3.2 Exchange: sell investments
            # 3.3 Exchange: history
            # 4: TODO: Profile/achievements?
            
            
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

class account:
    def __init__(self, input, pas, bal):
        self.name = input
        self.password = pas
        self.balance = bal
        self.portfolio = {}
        #global current_account
        #current_account = self
        #save()
	
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
            return (3.1, "Successfully purchased " + str(number) + " " + ticker)
        else:
            return (3.1, "Sorry, you don't have enough money :(")
    
    def sell(self, ticker, number):
        printAcc()
        owned = self.portfolio[ticker]
        if owned >= number:
            self.subtract(number * calcPrice(ticker,0))
            self.portfolio[ticker] -= number
            save()
            return (3.2, "Successfully sold " + number + " " + ticker)
        else:
            return (3.2, "You don't own that many :(")


def calcPrice(tick, history):
    today = datetime.datetime.now()
    difference = today - datetime.datetime(2000,1,1)
    num = difference.days - history
    return {
        investments[0] : (num % 2) + 1,
        investments[1] : (num % 3) + 2,
        investments[2] : int(round(math.sin(num)* 6 + 6))}[tick]
          

def read_accounts():
    global accounts
    accounts = []
    for filename in os.listdir(path):
        if filename.endswith(".acc"):
            name = os.path.split(filename)[1].split(".")[0]
            file = open(os.path.join(path, filename), "r")
            pw = file.readline().rstrip()
            accounts.append((name,pw)) # new addition
            file.close()    


# clear the terminal
def clear():
    os.system('cls||clear')

# print the information associated with the current account
def print_balance():
    print ("\n" + current_account.name + "'s balance: \t" + str(current_account.balance))

def print_portfolio():
    print ("\n" + current_account.name + "'s portfolio:")
    for asset in current_account.portfolio:
        print (asset + ":\t\t\t" + str(current_account.portfolio[asset]))

# load a selected account as the current account
def load_account(name):
    global current_account
    filename = os.path.join(path, name) + ".acc"
    file = open(filename, "r")
    current_account = account(name, file.readline().rstrip(), int(file.readline()))
    for asset in investments:
        current_account.portfolio[asset] = 0
    for line in file:
        lst = line.split(",")
        t = lst[0]
        if t in investments:
            current_account.portfolio[t] = int(lst[1])
    return (0.1, "Successfully logged in!")
            #file = open(filename, "r")
            #if os.stat(filename).st_size == 0:
            #    accounts.append(account(name, 100,hash("password")))
            #else:
            #    accounts.append(account(name, int(file.readline()), file.readline().rstrip()))
            #for asset in investments:
            #    accounts[count].portfolio[asset] = 0
            #for line in file:
            #    lst = line.split(",")
            #    t = lst[0]
            #    if t in investments:
            #        accounts[count].portfolio[t] = int(lst[1])
            #count += 1

def createAcc():
    name = input("Please enter a name for the new account:")
    if any(x.lower() == name.lower() for x in accounts):
        return (0, "An account already exists with that name!")
    else:
        pw = hash(input("Please enter a password for this account:"))
        global current_account
        current_account = account(name, pw, 0)
        for asset in investments:
            current_account.portfolio[asset] = 0
        save()
        return (0.1, "Successfully created account!")

def printInvestments():
    print ("\nToday's investment prices:")
    for asset in investments:
        print (asset + ":\t\t\t" + str(calcPrice(asset,0)))

def save():
    file = open(os.path.join(path,current_account.name + ".acc"), "w")
    file.write(str(current_account.password) + "\n")
    file.write(str(current_account.balance) + "\n")
    for asset in current_account.portfolio:
        file.write(asset + "," + str(current_account.portfolio[asset]) + "\n")
    file.close()

def quit():
    save()
    clear()
    sys.exit()
    
def select_account():
    if len(accounts) > 0:
        print ("\nWhich account would you like to access? Or press 'n' to create a new account")
        for index,(name,truepw) in enumerate(accounts):
            print(str(index) + ": " + name)
        n = input("")
        if n == "n":
            return createAcc()
        elif str.isdigit(n):
            if int(n) <= len(accounts):
                pw = hash(input("Please enter your password:"))
                if pw == truepw:
                    return load_account(name)
                else:
                    return (0, "Incorrect password!")
            return (0, "That account does not exist!")
        elif n.lower() in (name.lower() for (name,pw) in accounts):
            acc = [(x,y) for x,y in accounts if x.lower() == n.lower()]
            pw = hash(input("Please enter your password:"))
            if pw == acc[0][1]:
                return load_account(acc[0][0])
            else:
                return (0, "Incorrect password!")
        else:
            return (0, "I didn't understand what you wrote :(")
    else:
        print("\nNo accounts detected!")
        return createAcc()

def printHistory(days):
    for asset in investments:
        print (asset + " prices: ")
        for i in range(-1*days,-1):
            print (str(calcPrice(asset,i)) + ", ", end="")
        print(str(calcPrice(asset,0)))
        
def read_prizes():
    global prizes
    file = open(os.path.join(path,"prizes.config"), "r")
    for line in file:
        info = line.split(",")
        prizes.append((info[0],info[1].rstrip()))

def refresh():
    clear()
    global status
    global state
    print(status)
    (state, status) = interface()

def interface():
    if state == 0:          # account not selected
        read_accounts()
        return select_account()
    elif state == 0.1:           # account selected, main screen
        print_balance()
        print("\n1:\tLearning path\n2:\tPrize shop\n3:\tExchange market\n4:\tAchievements\n5:\tAdd money\n\nOr press 'q' to save and quit\n")
        inp = input("")
        if inp == '1':
            return(1, "Learning path has not yet been built")
        elif inp == '2':
            return (2,"Prize shop")
        elif inp == '3':
            return (3, "Exchange market")
        elif inp == '4':
            return (4, "Acievements have not yet been built")
        elif inp == '5':
            pw = input("Please enter the password to access this feature:")
            if pw != password:
                return (0.1, "Sorry! That password was not correct!")
            else:
                num = input("How much would you like to add?\n")
                current_account.balance += int(num)
                return (0.1, "Successfully added $" + num + "!")
        elif inp == 'q':
            quit()
        else:
            return (0.1, "I don't know what that means!")
    elif state == 1:          # Learning path
        t =  input("Press any key to return to the main screen\n")
        return (0.1, "Check back soon for learning path")

    elif state == 2:          #prizes
        for index, (prize, price) in enumerate(prizes):
            print(str(index) + ":\t" + prize + " for $" + price)
        print_balance()
        t = input("\nWhich prize would you like to buy? Or, press 'q' to return to the main menu\n")
        if t == 'q':
            return (0.1, "Welcome!")
        elif t.isdigit() and int(t) < len(prizes):
            price = int(prizes[int(t)][1])
            if current_account.balance >= price:
                current_account.subtract(price)
                return (2, "Successfully bought " + prizes[int(t)][0])
            else:
                return (2, "You can't afford that prize!")
        else:
            return (2, "That isn't an input I recognise :(")
                    
    elif state == 3:       # Exchange market
        printInvestments()
        print_balance()
        print_portfolio()
        inp = input("Press 'b' to buy, 's' to sell, 'h' to check the history of prices, or 'q' to return to the main screen\n")
        if inp == 'b':
            return (3.1, "Exchange market: buying")
        elif inp == 's':
            return (3.2, "Exchange market: selling")
        elif inp == "h":
            return (3.3, "Exchange market: history")
        elif inp == "q":
            return (0.1, "Welcome!")
        else:
            return (3, "I don't know what you want to do :(")
    elif state == 3.1:      #Exchange: buying
        printInvestments()
        print_balance()
        inp = ("What would you like to buy?\n")
        if inp.isdigit() and int(inp) < len(investments):
            n = input("How much " + investments[int(imp)] + " would you like to buy?\n")
            return current_account.buy(inp, int(n))
        elif n.upper() in investments:
            n = input("How much " + n.upper() + " would you like to buy?\n")
            return current_account.buy(inp.upper(), int(n))
        else:
            return (3.1, "I don't know what that is :(")
    elif state == 3.2:       #Exchange: selling
        printInvestments()
        print_portfolio()
        inp = ("What would you like to sell?\n")
        if inp.isdigit() and int(inp) <= len(investments):
            n = input("How much " + investments[int(imp)] + " would you like to sell?\n")
            return current_account.sell(inp, int(n))
        elif n.upper() in investments:
            n = input("How much " + n.upper() + " would you like to sell?\n")
            return current_account.sell(inp.upper(), int(n))
        else:
            return (3.2, "I don't know what that is :(")
    elif state == 3.3:      #price history
        l = input("Select a number of days to look back on, press 'e' to go back to the exchange market, or press 'q' to go back to the main menu\n")
        if l == 'q':
            return (0.1, "Welcome!")
        elif l == 'e':
            return (3, "Exchange market")
        else:
            if str.isdigit(l):
                printHistory(int(l))
            else:
                return (3.3, "Please enter a number!")
        inp = input("Press 'e' to return to the exchange market, 'q' to return to the main menu, or 'h' to check the history again:")
        if inp == 'e':
            return (3, "Exchange market")
        elif inp == 'q':
            return (0.1, "Welcome!")
        elif inp == 'h':
            return (3.3, "Exchange: price history")
        else:
            return (3.3, "I don't know what that means :(")
    
    
read_prizes()

while True:
    refresh()