from tkinter import *


class Buttons:

    def __init__(self, master):
        # master means the main window
        frame = Frame(master)
        frame.pack()

        self.printButton = Button(frame, text = "Print Message", command = self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text = "Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("How this actually worked!")


root = Tk()
b = Buttons(root)
root.mainloop()
