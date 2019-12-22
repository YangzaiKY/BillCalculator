from tkinter import *
from gui import App


if __name__ == '__main__':
    root = Tk()
    root.title('Bill Calculator')
    root.geometry('1000x800')

    App(root)
    root.mainloop()
