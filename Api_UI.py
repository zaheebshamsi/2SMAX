from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox
import requests


def get_requests(source_api_textbox):
    try:
        url = source_api_textbox.get("1.0", "end-1c")
        print(url)
        response = requests.post(url, verify=False)
        res_content = response.content.decode('ascii')
        res_json = json.loads(res_content)
        print(res_json)
    except Exception as ssl:
        print(ssl)
        print(ssl.__class__)
        tkinter.messagebox.showinfo("FATAL!!", ssl)


def design_get_api(LeftFrame0):
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

    source_api_textbox = Text(LeftFrame0, height=2, width=38, font="Arial 10")
    destination_api_textbox = Text(LeftFrame0, height=2, width=38, font="Arial 10")

    source_api_textbox.insert(END, 'Enter the URI')
    destination_api_textbox.insert(END, 'Enter the URI')

    source_api_textbox.grid(row=0, column=1, padx=10, pady=10)
    destination_api_textbox.grid(row=1, column=1, padx=10, pady=10)

    # --------------------Button for API URL-------------------#

    get_button = Button(LeftFrame0, text="GET", height=2, width=10, command=lambda: get_requests(source_api_textbox))
    get_button.grid(row=2, sticky="nsew", padx=10, pady=10)
