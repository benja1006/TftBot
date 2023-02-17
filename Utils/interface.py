from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import re
import os
import Utils.myFuncs as myFuncs
cur_list = []

class MyWindow:
    def __init__(self, win):
        self.tk = win
        champ_list = myFuncs.open_file()
        myDict = {}
        dx = 25
        dy = 25

        SUNKABLE_BUTTON = 'SunkableButton.TButton'
        style = ttk.Style()

        # Create buttons
        for j in range(0, 5):  # 1 costs
            for i in range(len(champ_list[j])):
                champ = champ_list[j][i]
                myDict["button_" + str(i)+str(j)] = ttk.Button(win, text=champ_list[j][i], command=lambda i=i, j=j: [
                    myFuncs.add(cur_list, champ_list[j][i]), start(myDict["button_" + str(i)+str(j)])], style=SUNKABLE_BUTTON)
                myDict["button_" + str(i)+str(j)].place(x=dx * (j*5), y=dy * i)

        # Print list button
        print_list = Button(win, text='print',
                            command=lambda: print(cur_list))
        print_list.place(x=400, y=400)

        # Clear list button
        clear_list = Button(win, text="clear", command=lambda: [
                            cur_list.clear(), clearButtons()])
        clear_list.place(x=500, y=400)

        # Pressed Button
        def start(button):
            button.state(['pressed', 'disabled'])
            style.configure(SUNKABLE_BUTTON, relief=tk.SUNKEN)

        # Depressed Button
        def stop(button):
            button.state(['!pressed', '!disabled'])
            style.configure(SUNKABLE_BUTTON, relief=tk.RAISED)

        def clearButtons():
            for j in range(0, 5):  # 1 costs
                for i in range(len(champ_list[j])):
                    stop(myDict["button_" + str(i)+str(j)])

        # Get list
    def getList(self):
        return cur_list

    def reset(self):
        cur_list.clear()
        MyWindow.clearButtons()


def main():
    window = Tk()
    mywin = MyWindow(window)
    window.title('Champs List')
    window.geometry("800x500+10+10")
    # window.mainloop()
    return mywin


if __name__ == "__main__":
    main()
