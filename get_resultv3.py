from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox
from api_uiv3 import *
global drop


def send_source_data(source_data_get):
    return source_data_get


def reset_dropdown(drop_event_reset):
    # delete items of Combobox
    for drop_combo in drop_event_reset:
        drop_combo.set(' ')
    tkinter.messagebox.showinfo("Microfocus 2SMAX", "Reset Done")


def update_size(event):
    widget_width = 0
    widget_height = float(event.widget.index(END))
    for line in event.widget.get("1.0", END).split("\n"):
        if len(line) > widget_width:
            widget_width = len(line) + 1
    event.widget.config(width=widget_width, height=widget_height)


def design_get_result(root, LeftFrame2, LeftFrame1, RightFrame0):
    data = json_load('snow.json')

    # customer_ticket_tool = open("snow.json", "r").name.split('.')[0].upper()

    # ---------------Labels---------------#

    var = StringVar()
    label = Label(LeftFrame2, textvariable=var, font="Arial 12")
    var.set("SMAX API Variables")
    label.grid(row=0, column=1, padx=10, pady=10)

    var = StringVar()
    label = Label(LeftFrame1, textvariable=var, font="Arial 12")
    var.set("Source API Variables")
    label.grid(row=0, column=1, padx=10, pady=10)

    var = StringVar()
    label = Label(RightFrame0, textvariable=var, font="Arial 12")
    var.set("Micro Focus 2SMAX \nEasier Migration to SMAX... ")
    label.grid(row=0, column=0, padx=10, pady=10)

    # ---------------Display JSON keys as labels---------------#

    i = 0
    res = list()
    for json_data_get_response in data['entities']:
        # print(json_data_get_response)
        for json_data_key in json_data_get_response['properties'].keys():
            res.append(json_data_key)
    remove_duplicates_from_json = []
    [remove_duplicates_from_json.append(x) for x in res if x not in remove_duplicates_from_json]
    print(remove_duplicates_from_json)

    for label_json_key in remove_duplicates_from_json:
        i += 1
        var = StringVar()
        label = Label(LeftFrame1, textvariable=var, bd=5, relief=RIDGE, padx=5, pady=5)
        var.set(label_json_key)
        label.grid(row=i, column=1, sticky="nsew", padx=12, pady=12)
        label.bind("<Key>", update_size)

    # ---------------Drop Down under SMAX Label---------------#

    # Dropdown SMAX menu options
    options = ["Ticket Number", "Ticket Age", "Email", "First Name", "Middle Name", "Last Name", "Emp ID",
               "Problem Description", "Technician Name", "Solution Description", "Resolution Time (min)"]

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set("SMAX Menu")

    # Create Dropdown menus on count of the keys in the json.
    drop_event_reset = []
    for i in range(len(remove_duplicates_from_json)):
        drop = ttk.Combobox(LeftFrame2, state='readonly', values=options, font="20")
        drop.grid(row=i + 1, column=1, sticky="nsew", padx=10, pady=15)
        drop_event_reset.append(drop)
        # drop.current(0)

    # ---------------Buttons---------------#

    push_button = Button(RightFrame0, text="POST", height=2)
    push_button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    reset_button = Button(RightFrame0, text="🔄 Reset", command=lambda: reset_dropdown(drop_event_reset), height=2)
    reset_button.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    reset_button = Button(RightFrame0, text="❌ Exit", command=root.destroy, height=2)
    reset_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)


# --------------------------------------------------------- #

def json_load(json_file):
    with open(json_file, 'r') as j:
        data = json.load(j)
    return data
