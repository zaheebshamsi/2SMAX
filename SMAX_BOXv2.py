from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox


def reset_dropdown():
    # delete items of Combobox
    # drop.clear()
    tkinter.messagebox.showinfo("Microfocus 2SMAX", "Reset Done")


class SmaxBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Microfocus 2SMAX")
        self.root.geometry("1350x800+0+0")
        self.root.state("zoomed")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        self.root.configure(background='powder blue')
        # self.root.configure(background='red')

        # adding action to button

    @staticmethod
    def design():
        data = SmaxBox.json_load("snow.json")

        customer_ticket_tool = open("snow.json", "r").name.split('.')[0].upper()

        # pass
        """Outer Main Frame"""
        MainFrame = Frame(root, bd=20, width=1280, height=1057, bg="cadet blue", padx=20, pady=20,
                          relief=RIDGE)
        MainFrame.pack()

        LeftMainFrame = Frame(MainFrame, bd=10, width=640, height=657, bg="powder blue", relief=RIDGE)
        LeftMainFrame.pack(side=LEFT, fill=BOTH)

        LeftFrame0 = Frame(LeftMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        LeftFrame0.grid(row=0, column=0, sticky="nsew")

        LeftFrame1 = Frame(LeftMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        LeftFrame1.grid(row=0, column=1, sticky="nsew")

        RightMainFrame = LabelFrame(MainFrame, bd=10, width=640, height=457, bg="powder blue", relief=RIDGE)
        RightMainFrame.pack(side=RIGHT, fill=BOTH)

        RightFrame0 = Frame(RightMainFrame, bd=10, width=400, height=558, bg="#3d3d5c", relief=RIDGE)
        RightFrame0.grid(row=0, column=0, sticky="nsew")

        """Labels"""
        var = StringVar()
        label = Label(LeftFrame1, textvariable=var)
        var.set("SMAX")
        label.grid(row=0, column=10)

        var = StringVar()
        label = Label(LeftFrame0, textvariable=var)
        var.set(customer_ticket_tool)
        label.grid(row=0, column=1)

        var = StringVar()
        label = Label(RightFrame0, textvariable=var, font="Arial 12")
        var.set("Micro Focus 2SMAX \nEasier Migration to SMAX... ")
        label.grid(row=0, column=0)

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
            label = Label(LeftFrame0, textvariable=var, bd=5, relief=RIDGE, padx=5, pady=5)
            var.set(label_json_key)
            label.grid(row=i, column=1, sticky="nsew")

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

        for i in range(len(remove_duplicates_from_json)):
            drop = ttk.Combobox(LeftFrame1, state='readonly', values=options, font="29")
            drop.grid(row=i + 1, column=10, sticky="nsew")
            # drop.current(0)

        """Buttons"""
        push_button = Button(RightMainFrame, text="Push", padx=10, pady=10)
        push_button.grid(row=1, column=0, sticky="nsew")

        reset_button = Button(RightMainFrame, text="Reset", command=reset_dropdown, padx=10, pady=10)
        reset_button.grid(row=2, column=0, sticky="nsew")

        reset_button = Button(RightMainFrame, text="Exit", command=root.destroy, padx=10, pady=10)
        reset_button.grid(row=3, column=0, sticky="nsew")

    # --------------------------------------------------------- #

    @staticmethod
    def json_load(json_file):
        with open(json_file, 'r') as j:
            data = json.load(j)
        return data


if __name__ == '__main__':
    root = Tk()
    application = SmaxBox(root)
    SmaxBox.design()
    root.mainloop()
