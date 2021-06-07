from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox


def design_get_api(root, LeftFrame0):

    # --------------------Labels for API URL-------------------#

    var = StringVar()
    label = Label(LeftFrame0, textvariable=var, width=17, height=2)
    var.set("Enter Source URL")
    label.grid(row=0, column=0, padx=10, pady=10)
    # label.grid()

    var = StringVar()
    label = Label(LeftFrame0, textvariable=var, width=17, height=2)
    var.set("Enter Destination URL")
    label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    # label.grid()

    # --------------------Text box for API URL-------------------#

    source_api_textbox = Text(LeftFrame0, height=2, width=45, font="Arial 10")
    destination_api_textbox = Text(LeftFrame0, height=2, width=45, font="Arial 10")

    source_api_textbox.insert(END, 'Enter the URI')
    destination_api_textbox.insert(END, 'Enter the URI')

    source_api_textbox.grid(row=0, column=1, padx=10, pady=10)
    destination_api_textbox.grid(row=1, column=1, padx=10, pady=10)

