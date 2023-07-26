from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import re
import os
import Utils.myFuncs as myFuncs
SUNKABLE_BUTTON = 'SunkableButton.TButton'

class MyWindow:
    def __init__(self, win):
        self.tk = win
        self.champ_list = myFuncs.open_file()
        self.myDict = {}
        dx = 25
        dy = 25
        self.closed = False
        self.cur_list = []
        
        self.style = ttk.Style()

        # Create buttons
        for j in range(0, 5):  # 1 costs
            for i in range(len(self.champ_list[j])):
                champ = self.champ_list[j][i]
                self.myDict["button_" + str(i)+str(j)] = ttk.Button(win, text=self.champ_list[j][i], command=lambda i=i, j=j: [
                    myFuncs.add(self.cur_list, self.champ_list[j][i]), self.start(self.myDict["button_" + str(i)+str(j)])], style=SUNKABLE_BUTTON)
                self.myDict["button_" + str(i)+str(j)].place(x=dx * (j*5), y=dy * i)

        # Print list button
        print_list = Button(win, text='print',
                            command=lambda: print(self.cur_list))
        print_list.place(x=400, y=400)

        # Clear list button
        clear_list = Button(win, text="clear", command=lambda: [
                            self.cur_list.clear(), self.clearButtons()])
        clear_list.place(x=500, y=400)

    # Pressed Button
    def start(self, button):
        button.state(['pressed', 'disabled'])
        self.style.configure(SUNKABLE_BUTTON, relief=tk.SUNKEN)

    # Depressed Button
    def stop(self, button):
        button.state(['!pressed', '!disabled'])
        self.style.configure(SUNKABLE_BUTTON, relief=tk.RAISED)

    def clearButtons(self):
        for j in range(0, 5):  # 1 costs
            for i in range(len(self.champ_list[j])):
                self.stop(self.myDict["button_" + str(i)+str(j)])

    def close(self):
        self.closed = True

    # Get list
    def getList(self):
        return self.cur_list

    def reset(self):
        self.cur_list.clear()
        self.clearButtons()


def main():
    window = Tk()
    mywin = MyWindow(window)
    window.title('Champs List')
    window.geometry("800x500+10+10")
    window.protocol("WM_DELETE_WINDOW", mywin.close)
    # window.mainloop()
    return mywin


if __name__ == "__main__":
    main()
