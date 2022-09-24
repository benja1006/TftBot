# CLEAR
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import re
import os
import myFuncs
os.system("clear")
# CLEAR

champ_list = myFuncs.open_file()
window = Tk()
myDict = {}
dx = 25
dy = 25
cur_list = []


SUNKABLE_BUTTON = 'SunkableButton.TButton'
style = ttk.Style()


def start(button):
    button.state(['pressed', 'disabled'])
    style.configure(SUNKABLE_BUTTON, relief=tk.SUNKEN)


def stop(button):
    button.state(['!pressed', '!disabled'])
    style.configure(SUNKABLE_BUTTON, relief=tk.RAISED)


def clearButtons():
    for j in range(0, 1):  # 1 costs
        for i in range(len(champ_list[j])):
            stop(myDict["button_" + str(i)])


for j in range(0, 5):  # 1 costs
    for i in range(len(champ_list[j])):
        champ = champ_list[j][i]
        myDict["button_" + str(i)+str(j)] = ttk.Button(window, text=champ_list[j][i], command=lambda i=i, j=j: [
            myFuncs.add(cur_list, champ_list[j][i]), start(myDict["button_" + str(i)+str(j)])], style=SUNKABLE_BUTTON)
        myDict["button_" + str(i)+str(j)].place(x=dx * (j*5), y=dy * i)


print_list = Button(window, text='print', command=lambda: print(cur_list))
print_list.place(x=400, y=400)

clear_list = Button(window, text="clear", command=lambda: [
                    cur_list.clear(), clearButtons()])
clear_list.place(x=500, y=400)

window.title('Hello Python')
window.geometry("800x500+10+10")
window.mainloop()
