from tkinter import *


def raise_frame(frame):
    frame.tkraise()

accounts = ["David", "Samson", "Rosalie", "Sage"]

root = Tk()

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

account_list = Listbox(f1)
for name in accounts:
    account_list.insert(END, name)
account_list.pack()

Button(f1, text='Login', command=lambda:raise_frame(f2)).pack()
Label(f1, text='FRAME 1').pack()

Label(f2, text='FRAME 2').pack()
Button(f2, text='Go to frame 3', command=lambda:raise_frame(f3)).pack()

Label(f3, text='FRAME 3').pack(side='left')
Button(f3, text='Go to frame 4', command=lambda:raise_frame(f4)).pack(side='left')

Label(f4, text='FRAME 4').pack()
Button(f4, text='Goto to frame 1', command=lambda:raise_frame(f1)).pack()

raise_frame(f1)
root.mainloop()