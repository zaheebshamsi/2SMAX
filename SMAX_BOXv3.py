from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox
from get_resultv3 import *
from api_uiv3 import *


class SmaxBox:
    def __init__(self, root, root_get_api):
        self.root = root
        self.root.title("Microfocus 2SMAX")
        self.root.geometry("1350x800+0+0")
        self.root.state("zoomed")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        self.root.configure(background='powder blue')

        self.MainFrame = Frame(self.root, bd=20, width=1280, height=1057, bg="cadet blue", padx=20, pady=20,
                               relief=RIDGE)
        self.canvas = Canvas(self.MainFrame, relief=SUNKEN)
        self.LeftMainFrame = Frame(self.MainFrame, bd=10, width=640, height=657, bg="powder blue", relief=RIDGE)
        self.RightMainFrame = LabelFrame(self.MainFrame, bd=10, width=640, height=457, bg="powder blue", relief=RIDGE)
        self.RightFrame0 = Frame(self.RightMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        self.LeftFrame0 = Frame(self.LeftMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        self.LeftFrame1 = Frame(self.LeftMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        self.LeftFrame2 = Frame(self.LeftMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        self.scrollbar_source = Scrollbar(self.LeftFrame1, orient="vertical", command=self.canvas.yview)
        self.scrollbar_destination = Scrollbar(self.LeftFrame2, orient="vertical", command=self.canvas.yview)

    def design_frames(self):
        """Outer Main Frame"""
        self.MainFrame.pack()

        self.LeftMainFrame.pack(side=LEFT, fill=BOTH)
        self.RightMainFrame.pack(side=RIGHT, fill=BOTH)

        self.LeftFrame0.grid(row=0, column=0, sticky="nsew")
        self.LeftFrame1.grid(row=0, column=1, sticky="nsew")
        self.LeftFrame2.grid(row=0, column=2, sticky="nsew")

        self.RightFrame0.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_source.grid(row=3, column=2, sticky="ns", rowspan=2)
        self.scrollbar_destination.grid(row=4, column=2, sticky="ns", rowspan=2)

        # -----------------This line creating problem------------------#
        # self.canvas.create_window((0, 0), window=None, anchor="nw")  #
        # -------------------------------------------------------------#

        self.canvas.config(yscrollcommand=self.scrollbar_source.set, scrollregion=self.canvas.bbox("all"),
                           width=200, height=200)
        self.canvas.config(yscrollcommand=self.scrollbar_destination.set, scrollregion=self.canvas.bbox("all"),
                           width=200, height=200)

    def execute(self):
        design_get_result(root, application.LeftFrame2, application.LeftFrame1, application.RightFrame0)
        design_get_api(application.LeftFrame0)


if __name__ == '__main__':
    root = Tk()
    application = SmaxBox(root, None)
    application.design_frames()
    application.execute()
    root.mainloop()
