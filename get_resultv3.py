from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox


def reset_dropdown(drop_event_reset):
    # delete items of Combobox
    print("Hello")
    print(drop_event_reset)
    print("End")
    for drop_combo in drop_event_reset:
        drop_combo.set(' ')
    # drop.set(' ')
    tkinter.messagebox.showinfo("Microfocus 2SMAX", "Reset Done")


def design_get_result(root, LeftFrame2, LeftFrame1, RightFrame0):
    data = json_load("snow.json")

    customer_ticket_tool = open("snow.json", "r").name.split('.')[0].upper()

    """Labels"""
    var = StringVar()
    label = Label(LeftFrame2, textvariable=var)
    var.set("SMAX")
    label.grid(row=0, column=1)

    var = StringVar()
    label = Label(LeftFrame1, textvariable=var)
    var.set(customer_ticket_tool)
    label.grid(row=0, column=1)

    var = StringVar()
    label = Label(RightFrame0, textvariable=var, font="Arial 12")
    var.set("Micro Focus 2SMAX \nEasier Migration to SMAX... ")
    label.grid(row=0, column=0, padx=10, pady=10)

    """Display JSON keys as labels"""
    i = 0
    res = list()
    print(data)
    for ticket_details in data['ticket']:
        res.append(list(ticket_details.keys()))
    remove_dict = list(itertools.chain.from_iterable(res))
    remove_duplicates_from_json = []
    [remove_duplicates_from_json.append(x) for x in remove_dict if x not in remove_duplicates_from_json]

    print(remove_duplicates_from_json)

    for label_json_key in remove_duplicates_from_json:
        i += 1
        var = StringVar()
        label = Label(LeftFrame1, textvariable=var, bd=5, relief=RIDGE, padx=5, pady=5)
        var.set(label_json_key)
        label.grid(row=i, column=1, sticky="nsew", padx=12, pady=12)

    """Drop Down under SMAX Label"""
    # Dropdown SMAX menu options
    options = ["Ticket Number", "Ticket Age", "Email", "First Name", "Middle Name", "Last Name", "Emp ID",
               "Problem Description", "Technician Name", "Solution Description", "Resolution Time (min)"]

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set("SMAX Menu")

    # Create Dropdown menus on count of the keys in the json.

    '''drop = OptionMenu(LeftFrame1, clicked, *options)

    drop.pack()

    drop1 = OptionMenu(LeftFrame1, clicked, *options1)

    drop1.pack()'''

    global drop
    drop_event_reset = []
    for i in range(len(remove_duplicates_from_json)):
        drop = ttk.Combobox(LeftFrame2, state='readonly', values=options, font="20")
        print(drop)
        drop.grid(row=i + 1, column=1, sticky="nsew", padx=10, pady=15)
        drop_event_reset.append(drop)
        # drop.current(0)

    """Buttons"""
    push_button = Button(RightFrame0, text="POST", height=2)
    push_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    reset_button = Button(RightFrame0, text="Reset", command=lambda: reset_dropdown(drop_event_reset), height=2)
    reset_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    reset_button = Button(RightFrame0, text="Exit", command=root.destroy, height=2)
    reset_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)


# --------------------------------------------------------- #

def json_load(json_file):
    with open(json_file, 'r') as j:
        data = json.load(j)
    return data
