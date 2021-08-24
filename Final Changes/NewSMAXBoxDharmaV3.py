"""

1. __author__: @Zaheeb Shamsi
2. __date_created__: 01/06/2021
3. __last_modified__: 24/08/2021
4. Draft Versions Rejected: 4
5. Times Refactored after production : 0 (Please increase +1 as a counter if code is refactored
                                       or changes are made to the functionality or UI after Production)
6. Team Members: Zaheeb Shamsi(Developer), Chaya TD(Developer), Sunil Nair(Solution Architect),
                 Dharmakrishna Thomas(Consultant), Praveen V(Consultant), Vaasuthevan Gopalakrishnan(Consultant).
-------------------------------------------------------------------------------------------------------------------
@Todo: Add more Menu Bar Items (Line-61)
@Todo: Provide operation based on Update/Create -> Done
@Todo: (HOLD)Add a blocker for sending and receiving at least 10 fields and if it is more than 10 - ask them to come us.
@Todo: Add multithreading to handle different processes at the same time to avoid 'Not Responding'.
@Todo: (HOLD)Some key based licencing to add.
__________________________________________________________________
@Jay: 1. To validate if the drop-down is not empty.
2. To return a dict/list of entries failed with their IDs.. (connection class to ref the Transfer class). -> done
3. Add a askquestion on the transfer all entries button to confirm to push all entries. (Message: Its irreversible) -> done
4. Remove edit button...
5. Provide invalid pass or username instead of Resp 500
6. Change Source/Destination to the dropdown SNOW/SMAX
7. Add Msgbox to the third page.
8. Interchange the functionality of third page --> Source(dropdown left) and destination (fixed label right)
    [Left - static / right dynamic] -----> DONE
__________________________________________________________
// Ask to install in root folder
//Check for proxy code.. and add it in the code.
-------------------------------------------------------------------------------------------------------------------
Classes:
- ToSMAXApp: Base class (root in tkinter) which creates root GUI and instantiates other 4 classes.
- SelectionSource: The class for selection of entries from source.
- SelectionDestination: The class for selection of entries from destination.
- Mapping: The class which maintain records of mapping from source to destination.
- Transfer: The class which handles transfer of data from source to destination.
--------------------------------------------------------------------------------------------------------------------
1. All the external files generated (created) during this code execution starts with MF_SMAX_<filename>.
2. Line-117/267 The MF Logo On the LEFT side of most screens.
3. Line-132 : tools (list) --> more elements can be added and can be programmed using if/else/elif : Line 161
4. Line-170/175/327/332: ID and LastUpdateTime not to be used in layout as it is already received from the JSON Response.
5. Line- 209: If there is any exception that arises during writing to a file, it is handed and the file is automatically
   deleted using system module.
6. Line- 237/378: Call of a thread.
7. Line-490/511: Adding 'Id' to both -- options(right dropdown) and source labels (left)
8.Line-542: Deleting (Popping) 'lastUpdateTime' from the source.json
9.Line-564: Replacing ' with \' to escape names containing single quote.
  Eg: 'Brian O' Healey' --> 'Brian O\' Healey'

"""
import ast
import re
import sys
import threading
import time
from collections import OrderedDict
from datetime import datetime
from tkinter.ttk import Combobox
import tkinter.font as font
import requests
import tkinter as tk
from tkinter import font as tkfont
import tkinter.messagebox
from json import dumps, loads, load
from PIL import ImageTk, Image
from os import system

from transfer_records import connect


class ToSMAXApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Arial', size=20, weight="bold", slant="italic")
        self.button_font = tkfont.Font(family='Arial', size=10, weight="bold", slant="italic")

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        sub_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=sub_menu)
        sub_menu.add_command(label="Exit", command=self.destroy)

        sub_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=sub_menu)

        def about_us():
            tk.messagebox.showinfo("Micro Focus 2SMAX", "Migrate your data to SMAX using REST.\n"
                                                        "Designed by @zaheeb_shamsi ITSM Micro Focus®\n"
                                                        "\tAll License Reserved©")

        sub_menu.add_command(label="About Us", command=about_us)

        """
            The container is where we'll stack a bunch of frames on top of each other, 
            then the one we want visible will be raised above the others..
        """
        self.title("Microfocus 2SMAX")
        self.geometry("1350x800+0+0")
        self.state("zoomed")
        container = tk.Frame(self, bd=5, width=1280, height=1057, bg="#24353d", padx=5, pady=5,  # F1F2F3 #0073e7
                             relief='ridge')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        photo = tk.PhotoImage(file="C:\\Users\\ZShamsi\\Desktop\\n_icon_dark-top.png")
        self.iconphoto(False, photo)

        self.frames = {}
        for F in (SelectionSource, SelectionDestination, Mapping, Transfer):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SelectionSource")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class SelectionSource(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#fffdfd')  # #3d3d5c #1a2933  fffdfd
        self.controller = controller

        img = ImageTk.PhotoImage(Image.open('C:\\Users\\ZShamsi\\Desktop\\mf_1.png'))
        panel = tk.Label(self, image=img)
        panel.photo = img
        panel.place(relx=0.051, rely=0.17)

        label = tk.Label(self, text="Micro Focus 2SMAX \n Easier Migration to SMAX...", width=20,
                         font=controller.title_font, bg='#fffdfd')
        label.place(relx=0.051, rely=0.47)

        label = tk.Label(self, text="SOURCE REST API", width=20, font=controller.title_font, bg='#fffdfd')
        label.place(relx=0.35, rely=0.07)

        label = tk.Label(self, text="Select ITSM Tool", width=20, bg='#fffdfd')
        label.place(relx=0.38, rely=0.2)

        tools = ['SMAX', 'SNOW']

        self.dropdown_source = Combobox(self, values=tools, state='readonly', width=20)
        self.dropdown_source.place(relx=0.5, rely=0.2)

        label1 = tk.Label(self, text='Enter RESTFUL URL', bg='#fffdfd')
        label1.place(relx=0.41, rely=0.4)

        label2 = tk.Label(self, text='Enter Username', bg='#fffdfd')
        label2.place(relx=0.42, rely=0.5)

        label3 = tk.Label(self, text='Enter Password', bg='#fffdfd')
        label3.place(relx=0.42, rely=0.6)

        self.rest_url_textbox_source = tk.Text(self, height=2, width=50, font="Arial 10")
        self.rest_url_textbox_source.insert(tk.END,
                                            'https://btp-hvm01633.swinfra.net/rest/488330779/ems/Incident?layout=Status,DisplayLabel,Description,RequestedByPerson,ImpactScope,RegisteredForActualService,Urgency')
        self.rest_url_textbox_source.place(relx=0.64, rely=0.42, anchor="center")

        username_textbox_source = tk.Text(self, height=2, width=50, font='Arial 10')
        username_textbox_source.insert(tk.END, 'zaheeb')
        username_textbox_source.place(relx=0.64, rely=0.53, anchor="center")

        password_textbox_source = tk.Entry(self, width=50, font="Arial 10", show='*')
        password_textbox_source.insert(tk.END, 'Automation_123')
        password_textbox_source.place(relx=0.64, rely=0.63, anchor="center", height=37)

        def test_connection(rest_url_textbox_source, username_textbox_source, password_textbox_source, dropdown_source):
            rest_url_textbox_data_source = rest_url_textbox_source.get("1.0", "end-1c")
            username_textbox_data_source = username_textbox_source.get("1.0", "end-1c")
            password_textbox_data_source = password_textbox_source.get()
            dropdown_value = dropdown_source.get()
            try:
                if not rest_url_textbox_data_source or not username_textbox_data_source \
                        or not password_textbox_data_source or not dropdown_value:
                    tkinter.messagebox.showerror("FATAL!!", "Please fill all the fields")
                    return False
                elif re.search(r'\blastupdatetime\b', rest_url_textbox_data_source.lower()):
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "LastUpdateTime layout can no longer be used to push the data, "
                                                   "Please remove 'LastUpdateTime' from the URI")
                    self.controller.show_frame("SelectionSource")
                    return False
                elif re.search(r'\bid\b', rest_url_textbox_data_source.lower()):
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "ID layout is already received from the REST Call, "
                                                   "Please remove 'ID' from the URI")
                    self.controller.show_frame("SelectionSource")
                    return False
                else:
                    if dropdown_source.get() == 'SMAX':
                        url = rest_url_textbox_source.get("1.0", "end-1c")

                        server_name_ip = url.split('/')[2]

                        tenant_id_1 = url.split('/')
                        res = [int(ele) if ele.isdigit() else ele for ele in tenant_id_1]
                        res1 = list(i for i in res if isinstance(i, int))
                        tenant_id = int(res1[0])

                        url_token = "https://" + str(
                            server_name_ip) + "/auth/authentication-endpoint/authenticate/login?TENANTID=" \
                                    + str(tenant_id)
                        payload = {"Login": username_textbox_data_source, "password": password_textbox_data_source}
                        headers = {"Content-Type": "application/json"}

                        response = requests.post(url_token, data=dumps(payload), headers=headers, verify=False)
                        if response.status_code == 200:
                            token_source = response.text

                            headers = {"Content-Type": "application/json",
                                       "Cookie": "LWSSO_COOKIE_KEY={}".format(token_source)}

                            response = requests.get(rest_url_textbox_data_source, headers=headers, verify=False)
                            if response.status_code == 200:
                                result_json = response.content.decode('utf-8')
                                result_json_to_file = loads(result_json)
                                failure = result_json_to_file['meta']['completion_status']
                                if str(failure).lower() == 'failed':
                                    tk.messagebox.showerror(
                                        "httpStatus: " + str(result_json_to_file['meta']['errorDetails']['httpStatus']),
                                        "Invalid Response from the Source API\n\n" + str(
                                            result_json_to_file['meta']['errorDetails'][
                                                'message']) + "\n\n\nPlease close this window and try again!!")
                                    return False
                                json_file = dumps(result_json_to_file, indent=4)
                                try:
                                    with open("MF_SMAX_source.json", "w") as outfile:
                                        outfile.write(json_file)
                                except Exception:
                                    system("del /f MF_SMAX_source.json")
                            else:
                                tkinter.messagebox.showwarning("Response",
                                                               "Response Code: " + str(response.status_code))
                                return
                        else:
                            tkinter.messagebox.showwarning("Token Response",
                                                           "Invalid Username/Password - Response Code: " +
                                                           str(response.status_code) +
                                                           '\n')
                            return
                    else:
                        pass

                    def pb_def_2():
                        time.sleep(1)

                        button1['state'] = 'normal'
                        rest_url_textbox_source['state'] = 'normal'
                        username_textbox_source['state'] = 'normal'
                        password_textbox_source['state'] = 'normal'

                    rest_url_textbox_source['state'] = 'disabled'
                    username_textbox_source['state'] = 'disabled'
                    password_textbox_source['state'] = 'disabled'
                    button1['state'] = 'disabled'
                    threading.Thread(target=pb_def_2()).start()

                    tkinter.messagebox.showinfo("Success", "Connection Successful")
                    button2['state'] = 'normal'

            except NameError:
                tkinter.messagebox.showerror("FATAL!!", "Please fill all the fields")
                return
            except requests.exceptions.ConnectionError:
                tkinter.messagebox.showerror("FATAL!!",
                                             "Can not find the host: " + rest_url_textbox_data_source.split('/')[2])

            except Exception as ssl:
                tkinter.messagebox.showerror("FATAL!!", str(ssl) + str(ssl.__class__))

        button1 = tk.Button(self, text='Test Connection', relief='raised', font=controller.button_font,
                            command=lambda: [test_connection(self.rest_url_textbox_source, username_textbox_source,
                                                             password_textbox_source, self.dropdown_source),
                                             Mapping.map_1(self, self.rest_url_textbox_source)])
        button1.place(relx=0.54, rely=0.73)

        button2 = tk.Button(self, text='Select Destination API →', state='disabled', relief='raised',
                            font=controller.button_font,
                            command=lambda: controller.show_frame("SelectionDestination"))
        button2.place(relx=0.84, rely=0.9)


class SelectionDestination(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#fffdfd')  # #3d3d5c #1a2933  fffdfd
        self.controller = controller

        img = ImageTk.PhotoImage(Image.open('C:\\Users\\ZShamsi\\Desktop\\mf_1.png'))
        panel = tk.Label(self, image=img)
        panel.photo = img
        panel.place(relx=0.051, rely=0.17)

        label = tk.Label(self, text="Micro Focus 2SMAX \n Easier Migration to SMAX...", width=20,
                         font=controller.title_font, bg='#fffdfd')
        label.place(relx=0.051, rely=0.47)

        label = tk.Label(self, text="DESTINATION REST API", width=20, font=controller.title_font, bg='#fffdfd')
        label.place(relx=0.35, rely=0.07)

        label = tk.Label(self, text="Select ITSM Tool", width=20, bg='#fffdfd')
        label.place(relx=0.38, rely=0.2)

        tools = ['SMAX', 'SNOW']

        self.dropdown_destination = Combobox(self, values=tools, state='readonly', width=20)
        self.dropdown_destination.place(relx=0.5, rely=0.2)

        label1 = tk.Label(self, text='Enter RESTFUL URL', bg='#fffdfd')
        label1.place(relx=0.41, rely=0.4)

        label2 = tk.Label(self, text='Enter Username', bg='#fffdfd')
        label2.place(relx=0.42, rely=0.5)

        label3 = tk.Label(self, text='Enter Password', bg='#fffdfd')
        label3.place(relx=0.42, rely=0.6)

        self.rest_url_textbox_destination = tk.Text(self, height=2, width=50, font="Arial 10")
        self.rest_url_textbox_destination.insert(tk.END,
                                                 'https://btp-hvm01633.swinfra.net/rest/936071520/ems/Incident?layout=Status,DisplayLabel,Description,RequestedByPerson,ImpactScope,RegisteredForActualService,Urgency')
        self.rest_url_textbox_destination.place(relx=0.64, rely=0.42, anchor="center")

        self.username_textbox_destination = tk.Text(self, height=2, width=50, font='Arial 10')
        self.username_textbox_destination.insert(tk.END, 'zaheeb')
        self.username_textbox_destination.place(relx=0.64, rely=0.53, anchor="center")

        self.password_textbox_destination = tk.Entry(self, width=50, font="Arial 10", show='*')
        self.password_textbox_destination.insert(tk.END, 'Automation_123')
        self.password_textbox_destination.place(relx=0.64, rely=0.63, anchor="center", height=37)

        def test_connection(rest_url_textbox_destination, username_textbox_destination,
                            password_textbox_destination,
                            dropdown_destination):
            rest_url_textbox_data_destination = rest_url_textbox_destination.get("1.0", "end-1c")
            username_textbox_data_destination = username_textbox_destination.get("1.0", "end-1c")
            password_textbox_data_destination = password_textbox_destination.get()
            dropdown_value = dropdown_destination.get()
            try:
                if not rest_url_textbox_data_destination or not username_textbox_data_destination \
                        or not password_textbox_data_destination or not dropdown_value:
                    tkinter.messagebox.showerror("FATAL!!", "Please fill all the fields")
                    return False
                elif re.search(r'\blastupdatetime\b', rest_url_textbox_data_destination.lower()):
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "LastUpdateTime layout is already received from the REST Call, "
                                                   "Please remove 'LastUpdateTime' from the URI")
                    self.controller.show_frame("SelectionDestination")
                    return False
                elif re.search(r'\bid\b', rest_url_textbox_data_destination.lower()):
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "ID layout is already received from the REST Call, "
                                                   "Please remove 'ID' from the URI")
                    self.controller.show_frame("SelectionDestination")
                    return False
                else:
                    if dropdown_destination.get() == 'SMAX':
                        url = rest_url_textbox_destination.get("1.0", "end-1c")

                        server_name_ip = url.split('/')[2]

                        tenant_id_1 = url.split('/')
                        res = [int(ele) if ele.isdigit() else ele for ele in tenant_id_1]
                        res1 = list(i for i in res if isinstance(i, int))
                        tenant_id = int(res1[0])

                        url_token = "https://" \
                                    + str(server_name_ip) \
                                    + "/auth/authentication-endpoint/authenticate/login?TENANTID=" \
                                    + str(tenant_id)
                        payload = {"Login": username_textbox_data_destination,
                                   "password": password_textbox_data_destination}
                        headers = {"Content-Type": "application/json"}

                        response = requests.post(url_token, data=dumps(payload), headers=headers, verify=False)
                        if response.status_code == 200:
                            pass
                        else:
                            tkinter.messagebox.showwarning("Response",
                                                           "Response Code: " + str(response.status_code))
                            return False
                    else:
                        pass

                    def pb_def_2():
                        time.sleep(1)

                        button1['state'] = 'normal'
                        rest_url_textbox_destination['state'] = 'normal'
                        username_textbox_destination['state'] = 'normal'
                        password_textbox_destination['state'] = 'normal'

                    rest_url_textbox_destination['state'] = 'disabled'
                    username_textbox_destination['state'] = 'disabled'
                    password_textbox_destination['state'] = 'disabled'
                    button1['state'] = 'disabled'
                    threading.Thread(target=pb_def_2()).start()

                    tkinter.messagebox.showinfo("Success", "Connection Successful")
                    button2['state'] = 'normal'

            except NameError:
                tkinter.messagebox.showerror("FATAL!!", "Please fill all the fields")
                return False

            except Exception as ssl:
                tkinter.messagebox.showerror("FATAL!!", str(ssl) + str(ssl.__class__))

        button1 = tk.Button(self, text='Test Connection', relief='raised',
                            command=lambda: [test_connection(self.rest_url_textbox_destination,
                                                             self.username_textbox_destination,
                                                             self.password_textbox_destination,
                                                             self.dropdown_destination),
                                             Mapping.map_2(self, self.rest_url_textbox_destination)])
        button1['font'] = controller.button_font
        button1.place(relx=0.54, rely=0.73)

        button2 = tk.Button(self, text='Map APIs →', state='disabled', relief='raised',
                            command=lambda: controller.show_frame("Mapping"))
        button2['font'] = controller.button_font
        button2.place(relx=0.84, rely=0.9)


class Mapping(SelectionSource, SelectionDestination):
    def __init__(self, parent, controller):
        global frame_canvas, source_variable, button_create_json, \
            button_transfer_one_entry, created_json_text_box, operation_dropdown
        SelectionSource.__init__(self, parent, controller)
        SelectionDestination.__init__(self, parent, controller)

        tk.Frame.__init__(self, parent, background='#fffdfd')  # #3d3d5c #1a2933
        self.controller = controller

        def scrollbar_bind(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=593, height=633)  # 1179 full screen

        canvas = tk.Canvas(self, bg='#fffdfd')
        frame_canvas = tk.Frame(canvas, bg='#fffdfd')
        myscrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right", fill="y")
        canvas.pack(side=tk.LEFT)
        canvas.create_window((0, 0), window=frame_canvas, anchor='nw')
        frame_canvas.bind_all("<Configure>", scrollbar_bind)

        # myFont = font.Font(family='Arial', size=15, weight='bold', slant="italic")

        # var = tk.StringVar()
        # label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='grey')
        # # var.set("  SOURCE API COLUMNS")
        # var.set("{} API COLUMNS".format(self.dropdown_source.get()))
        # label.grid(row=1, column=1, padx=8)
        #
        # var = tk.StringVar()
        # label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='grey')
        # # var.set("DESTINATION API COLUMNS")
        # var.set("{} API COLUMNS".format(str(self.dropdown_destination.get())))
        # label.grid(row=1, column=0, padx=8)

        operation_textbox = tk.Text(frame_canvas, width=25, height=1, bg='#fffdfd', font=25, bd=3)
        operation_textbox.insert(tk.END, "Operation")
        operation_textbox.grid(row=0, column=0, padx=5, pady=5)
        operation_textbox.bindtags((operation_textbox, self, "all"))

        operation_values = ["Create", "Update"]
        operation_dropdown = Combobox(frame_canvas, values=operation_values, state='readonly', font=25)
        operation_dropdown.grid(row=0, column=1, sticky="nsew", padx=10, pady=25)

        button_create_json = tk.Button(self, text='Create JSON Body', bg='pink', relief='ridge',
                                       width=17, height=2, fg='black',
                                       font=self.controller.button_font)
        button_create_json.place(relx=0.7, rely=0.1)

        created_json_text_box = tk.Text(self, width=75, height=23, bg='cyan')
        created_json_text_box.place(relx=0.5, rely=0.2)

        button_transfer_all_entries = tk.Button(self, text='Transfer All Entries Page →', bg='pink',
                                                relief='ridge', width=25, height=2, fg='black',
                                                font=self.controller.button_font,
                                                command=lambda: [controller.show_frame("Transfer"),
                                                                 Transfer.display_json_to_textbox(self)])

        button_transfer_one_entry = tk.Button(self, text='Transfer One Entry', bg='pink',
                                              relief='ridge', width=17, height=2, fg='black',
                                              state='disabled', font=self.controller.button_font,
                                              command=lambda: Transfer.transfer_one(self,
                                                                                    button_transfer_all_entries,
                                                                                    button_transfer_one_entry))

        button_transfer_one_entry.place(relx=0.7, rely=0.81)

    # @staticmethod
    def map_1(self, rest_url_textbox_source):
        global row_array_layout, row_array_dropdown

        myFont = font.Font(family='Arial', size=15, weight='bold', slant="italic")
        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='grey')
        # var.set("  SOURCE API COLUMNS")
        var.set("{} API COLUMNS".format(self.dropdown_source.get()))
        label.grid(row=1, column=1, padx=8)

        row_array_layout = []
        row_array_dropdown = list()
        rest_url_textbox_data_source = rest_url_textbox_source.get("1.0", "end-1c")

        sp = rest_url_textbox_data_source.split('layout=')
        sp_layout = sp[-1]
        if '&' in sp_layout:
            layout = sp_layout.split('&')[0].split(',')

        else:
            layout = sp_layout.split(',')
        res = 'id' in (string.lower() for string in layout)
        if not res:
            layout.append('Id')

        x = 2
        for i in range(len(layout)):
            source_variable = tk.Text(frame_canvas, width=25, height=1, bg='#fffdfd', font=25, bd=3)
            source_variable.insert(tk.END, layout[i])
            row_array_layout.append(source_variable)
            row_array_layout[i].grid(row=x, column=1, padx=5, pady=5)
            row_array_layout[i].bindtags((source_variable, self, "all"))
            x += 1

    def map_2(self, rest_url_textbox_destination):

        myFont = font.Font(family='Arial', size=15, weight='bold', slant="italic")
        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='grey')
        # var.set("DESTINATION API COLUMNS")
        var.set("{} API COLUMNS".format(str(self.dropdown_destination.get())))
        label.grid(row=1, column=0, padx=8)

        rest_url_textbox_data_destination = rest_url_textbox_destination.get("1.0", "end-1c")

        sp = rest_url_textbox_data_destination.split('layout=')
        sp_layout = sp[-1]
        if '&' in sp_layout:
            options = sp_layout.split('&')[0].split(',')

        else:
            options = sp_layout.split(',')
        res = 'id' in (string.lower() for string in options)
        if not res:
            options.append('Id')

        y = 2
        for j in range(len(options)):
            dropdown = Combobox(frame_canvas, values=options, state='readonly', font=25)
            row_array_dropdown.append(dropdown)
            row_array_dropdown[j].grid(row=y, column=0, sticky="nsew", padx=10, pady=25)
            y += 1
        try:
            button_create_json['command'] = lambda: Mapping.push_and_map(self, source_variable_mapping=row_array_layout,
                                                                         dropdown_value_mapping=row_array_dropdown)
        except Exception:
            tkinter.messagebox.showerror("ERROR", "Key Error, Please Fill all the fields")

    def push_and_map(self, source_variable_mapping=None, dropdown_value_mapping=None):
        temp_source = []
        temp_destination = []

        if source_variable_mapping and dropdown_value_mapping:
            for row_array_get_layout in source_variable_mapping:
                temp_source.append(row_array_get_layout.get("1.0", "end-1c"))

            for row_array_get_dropdown in dropdown_value_mapping:
                if not row_array_get_dropdown.get():
                    tkinter.messagebox.showwarning("FATAL!!", "Please fill all the fields")
                    return False
                temp_destination.append(row_array_get_dropdown.get())

        with open('MF_SMAX_source.json') as sj:
            source_data = load(sj)
        failure = source_data['meta']['completion_status']
        if str(failure).lower() == 'failed':
            tk.messagebox.showerror("httpStatus: " + str(source_data['meta']['errorDetails']['httpStatus']),
                                    "Invalid Response from the Source API\n\n" + str(source_data['meta'][
                                                                                         'errorDetails']) + "\n\n\nPlease close this window and try again!!")
            return False

        sorted_on_temp_source = []
        for del_last_update_time in source_data['entities']:
            prop = del_last_update_time['properties']
            prop.pop('LastUpdateTime')
            index_map = {v: i for i, v in enumerate(temp_source)}
            y = sorted(prop.items(), key=lambda pair: index_map[pair[0]])
            di = dict(y)
            sorted_on_temp_source.append(di)

        entitiy_type = source_data['entities'][0]['entity_type']
        operation = str(operation_dropdown.get()).upper()

        json_layout = [{"entities": [{"entity_type": entitiy_type, "properties": {}}], "operation": operation}]

        # Adding the indices of temp_destination in a format - {value: <value>}
        for i in range(len(temp_destination)):
            json_layout[0]['entities'][0]['properties'][temp_destination[i]] = '<' + temp_source[i] + '>'

        new_json_layout = []
        for i in range(len(source_data['entities'])):
            new_json_layout.append(json_layout[0])

        for x in sorted_on_temp_source:
            for k, v in x.items():
                if "\'" in v:
                    v = v.replace('\'', "\\'")
                for _ in new_json_layout:
                    pass
                new_json_layout = str(new_json_layout).replace('<' + k + '>', v, 1)

        new_json_layout_list = ast.literal_eval(new_json_layout)

        new_json_layout_json = dumps(new_json_layout_list, indent=4)
        with open("MF_SMAX_for_destination_updated_file.json", "w") as outfile:
            outfile.write(new_json_layout_json)
        idk = loads(new_json_layout_json)

        created_json_text_box.insert(tk.END, dumps(idk[0], indent=4))
        # created_json_text_box['state'] = 'disabled' # Editable option for user enabled.

        if len(loads(new_json_layout_json)) == len(source_data['entities']):
            tkinter.messagebox.showinfo("Success", "JSON Body Created Successfully")
            button_transfer_one_entry['state'] = 'normal'

        else:
            tkinter.messagebox.showerror("Error", "There was a problem parsing the JSON file, Please retry!")
            return False


class Transfer(Mapping):
    def __init__(self, parent, controller):
        SelectionSource.__init__(self, parent, controller)
        SelectionDestination.__init__(self, parent, controller)

        tk.Frame.__init__(self, parent, background='#fffdfd')  # #3d3d5c #1a2933
        self.controller = controller

        global transfer_text_box_all_json, return_to_first_page_button, exit_button, edit_button, push_button, \
            error_output_textbox

        transfer_text_box_all_json = tk.Text(self, width=75, height=36, bg='cyan')
        transfer_text_box_all_json.pack(side=tk.LEFT)
        error_output_textbox = tk.Text(self, width=55, height=36, bg='powder blue')
        error_output_textbox.pack(side=tk.RIGHT)

        def edit():
            tkinter.messagebox.showwarning("2SMAX EDIT WARNING", "The data shown is auto-generated, "
                                                                 "please edit on your own risk!!")
            transfer_text_box_all_json['state'] = 'normal'

        edit_button = tk.Button(self, text='Edit Entries', font=controller.button_font,
                                command=edit)
        edit_button.place(relx=0.5, rely=0.4, anchor=tk.W)

        push_button = tk.Button(self, text='Push All Entries', font=controller.button_font,
                                command=lambda: self.transfer_all())
        push_button.place(relx=0.5, rely=0.5)

        return_to_first_page_button = tk.Button(self, text="Return to First Page",
                                                font=controller.button_font,
                                                command=lambda: controller.show_frame("SelectionSource"))

        exit_button = tk.Button(self, text="EXIT",
                                font=controller.button_font,
                                command=controller.destroy)

    def display_json_to_textbox(self):
        with open('MF_SMAX_for_destination_updated_file.json') as dufl:
            data = load(dufl)

        transfer_text_box_all_json.insert(tk.END, dumps(data, indent=4))
        transfer_text_box_all_json['state'] = 'disabled'

    def transfer_one(self, button_transfer_all_entries, button_transfer_one_entry):
        #########################################
        # Do some task here to push one record  #
        #########################################
        global status_code, result, completion_status

        url = self.rest_url_textbox_destination.get("1.0", "end-1c")
        server_name_ip = url.split('/')[2]

        tenant_id_1 = url.split('/')
        res = [int(ele) if ele.isdigit() else ele for ele in tenant_id_1]
        res1 = list(i for i in res if isinstance(i, int))
        tenant_id = int(res1[0])

        # result = None

        try:

            ticket_count, status_code, completion_status, record_id, error_details = connect(
                external_access_host=server_name_ip,
                tenant_id=tenant_id,
                user_name=self.username_textbox_destination.get(
                    "1.0", "end-1c"),
                password=self.password_textbox_destination.get(),
                json_to_push=loads(
                    created_json_text_box.get("1.0",
                                              "end-1c")),
                single_record=True)
            if ticket_count == 1 and status_code == 200 and not str(completion_status).lower() == 'failed':
                tk.messagebox.showinfo("Success", "One Entry Transferred Successfully")
                button_transfer_one_entry.place_forget()
                button_transfer_all_entries.place(relx=0.7, rely=0.81)
            else:
                tk.messagebox.showerror("Transfer Failed",
                                        "Failed One Entry Transfer Failed. \nID: " + record_id + "\nCompletion_status: " + completion_status
                                        + "\nError Details: " + str(error_details))
        except Exception:
            tk.messagebox.showerror("Failed", "ERROR SENDING DATA")

    def transfer_all(self):
        #########################################
        # Do some task here to push all records  #
        #########################################
        global status_code1, result1, completion_status1
        confirm_push = tk.messagebox.askquestion("Transfer All",
                                                 "Are you sure you want to transfer all data ?\n It is irreversable. ")
        if confirm_push.lower() == 'yes':
            with open('MF_SMAX_for_destination_updated_file.json') as dufl:
                data = load(dufl)

            url = self.rest_url_textbox_destination.get("1.0", "end-1c")
            server_name_ip = url.split('/')[2]

            tenant_id_1 = url.split('/')
            res = [int(ele) if ele.isdigit() else ele for ele in tenant_id_1]
            res1 = list(i for i in res if isinstance(i, int))
            tenant_id = int(res1[0])

            try:
                ticket_count1, status_code1, completion_status1, success_record_id1, failure_record_details1 = connect(
                    external_access_host=server_name_ip,
                    tenant_id=tenant_id,
                    user_name=self.username_textbox_destination.get(
                        "1.0",
                        "end-1c"),
                    password=self.password_textbox_destination.get(),
                    json_to_push=loads(
                        transfer_text_box_all_json.get(
                            "1.0",
                            "end-1c")),
                    multi_record=True)
                if ticket_count1 == len(data) and status_code1 is None and not str(
                        completion_status1).lower() == 'failed' \
                        and not failure_record_details1:
                    tk.messagebox.showinfo("Success", "All Entries Transferred Successfully")
                    error_output_textbox.insert(tk.END, "Transfer Completed Successfully: \n" + str(
                        ticket_count1) + " Entry(s) Transferred out of " + str(
                        len(data)) + " Entry(s)")
                else:
                    tk.messagebox.showinfo("Partial", str(ticket_count1) + " Entry(s) Transferred out of " + str(
                        len(data)) + " Entry(s)")
                    output_display = "***This output is logged in a logfile - 2smax.log*** \n\nPartial Transfer: \n" + str(
                        ticket_count1) + " Entry(s) Transferred out of " + str(
                        len(data)) + " Entry(s)\nFailure Entry(s) Details: " + str(
                        dumps(failure_record_details1, indent=4))
                    output_log = str(datetime.utcnow()) + "\n\nPartial Transfer: \n" + str(
                        ticket_count1) + " Entry(s) Transferred out of " + str(
                        len(data)) + " Entry(s)\nFailure Entry(s) Details: " + str(
                        dumps(failure_record_details1, indent=4))
                    error_output_textbox.insert(tk.END, output_display)
                    open('2SMAX.log', 'w').write(output_log)

                save_file = tk.messagebox.askquestion("Save", "Do you want to save the JSON Files(s) "
                                                              "created during the execution ?")
                if save_file.lower() == 'yes':
                    pass
                else:
                    system("del /f MF_SMAX_source.json, MF_SMAX_for_destination_updated_file.json")
                    tkinter.messagebox.showinfo("Done", "Removed Files successfully")

                edit_button.place_forget()
                push_button.place_forget()

                return_to_first_page_button.place(relx=0.5, rely=0.4)
                exit_button.place(relx=0.5, rely=0.5)

            except Exception:
                tk.messagebox.showerror("Failed", "ERROR SENDING DATA")
                # exception_type, exception_object, exception_traceback = sys.exc_info()
                # filename = exception_traceback.tb_frame.f_code.co_filename
                # line_number = exception_traceback.tb_lineno
                # print("Exception type: ", exception_type)
                # print("File name: ", filename)
                # print("Line number: ", line_number)
        else:
            tk.messagebox.showinfo("Transfer All", "Transfer All Cancelled")
            save_file = tk.messagebox.askquestion("Save", "Do you want to save the JSON Files(s) "
                                                          "created during the execution ?")
            if save_file.lower() == 'yes':
                pass
            else:
                system("del /f MF_SMAX_source.json, MF_SMAX_for_destination_updated_file.json")
                tkinter.messagebox.showinfo("Done", "Removed Files successfully")

            edit_button.place_forget()
            push_button.place_forget()
            exit_button.place(relx=0.5, rely=0.5)


if __name__ == "__main__":
    app = ToSMAXApp()
    app.mainloop()
