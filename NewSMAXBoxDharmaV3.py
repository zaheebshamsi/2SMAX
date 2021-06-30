"""

1. All the files generated (created) during this code execution starts with MF_SMAX_<filename>.
Search for MF_SMAX string to quick access of those files.
"""
import ast
import threading
import time
from collections import OrderedDict
from tkinter.ttk import Combobox
import tkinter.font as font
import requests
import sys
import tkinter as tk
from tkinter import font as tkfont, ttk
import tkinter.messagebox
from json import dumps, loads, load, dump
from PIL import ImageTk, Image


# to store the token into a text file. - > NO


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

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
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
        for F in (SelectionSource, SelectionDestination, Mapping):  # , ApiPage, ResultsPage, PageTwo
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
        # global dropdown_value
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

        # def get_dropdown(event):
        #     global dropdown_value
        #     dropdown_value = dropdown.get()
        #     flag = True

        dropdown = Combobox(self, values=tools, state='readonly', width=20)
        dropdown.place(relx=0.5, rely=0.2)
        # dropdown.bind("<<ComboboxSelected>>", get_dropdown)

        label1 = tk.Label(self, text='Enter RESTFUL URL', bg='#fffdfd')
        label1.place(relx=0.41, rely=0.4)

        label2 = tk.Label(self, text='Enter Username', bg='#fffdfd')
        label2.place(relx=0.42, rely=0.5)

        label3 = tk.Label(self, text='Enter Password', bg='#fffdfd')
        label3.place(relx=0.42, rely=0.6)

        self.rest_url_textbox_source = tk.Text(self, height=2, width=50, font="Arial 10")
        self.rest_url_textbox_source.insert(tk.END,
                                            'https://btp-hvm01633.swinfra.net/rest/488330779/ems/Person?layout=Name,Email')
        self.rest_url_textbox_source.place(relx=0.64, rely=0.42, anchor="center")

        username_textbox_source = tk.Text(self, height=2, width=50, font='Arial 10')
        username_textbox_source.insert(tk.END, 'zaheeb')
        username_textbox_source.place(relx=0.64, rely=0.53, anchor="center")

        password_textbox_source = tk.Entry(self, width=50, font="Arial 10", show='*')
        password_textbox_source.insert(tk.END, 'Automation_123')
        password_textbox_source.place(relx=0.64, rely=0.63, anchor="center", height=37)

        def test_connection(rest_url_textbox_source, username_textbox_source, password_textbox_source, dropdown):
            # print(rest_url_textbox_source)
            rest_url_textbox_data_source = rest_url_textbox_source.get("1.0", "end-1c")
            username_textbox_data_source = username_textbox_source.get("1.0", "end-1c")
            password_textbox_data_source = password_textbox_source.get()
            dropdown_value = dropdown.get()
            try:
                if not rest_url_textbox_data_source or not username_textbox_data_source \
                        or not password_textbox_data_source or not dropdown_value:
                    tkinter.messagebox.showerror("FATAL!!", "Please fill all the fields")
                    return False
                elif 'lastupdatetime' in rest_url_textbox_data_source.lower():
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "LastUpdateTime layout can no longer be used to push the data, "
                                                   "Please remove 'LastUpdateTime' from the URI")
                    return False
                elif 'id' in rest_url_textbox_data_source.lower():
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "ID layout is already received from the REST Call, "
                                                   "Please remove 'ID' from the URI")
                    return False
                else:
                    if dropdown.get() == 'SMAX':
                        url = rest_url_textbox_source.get("1.0", "end-1c")

                        server_name_ip = url.split('/')[2]

                        tenant_id_1 = url.split('/')
                        res = [int(ele) if ele.isdigit() else ele for ele in tenant_id_1]
                        res1 = list(i for i in res if isinstance(i, int))
                        tenant_id = int(res1[0])
                        # print(url)
                        # print(server_name_ip)
                        # print(tenant_id_1)
                        # print(res)
                        # print(res1)
                        # print(tenant_id)

                        # server_name_ip = url.split('/')[2]
                        #
                        # tenant_id_find = url.find('TENANTID=')
                        # ampersand_find = url.find('&')
                        #
                        # tenant_id = url[tenant_id_find + 9:ampersand_find]
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
                                json_file = dumps(result_json_to_file, indent=4)
                                with open("source.json", "w") as outfile:
                                    outfile.write(json_file)
                            else:
                                tkinter.messagebox.showwarning("Response",
                                                               "Response Code: " + str(response.status_code))
                                return
                        else:
                            tkinter.messagebox.showwarning("Response",
                                                           "Response Code: " + str(response.status_code))
                            return
                    else:
                        pass

                    def pb_def_2():
                        pb.pack()
                        pb.start()
                        time.sleep(2)
                        pb.stop()
                        pb.pack_forget()

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

            except Exception as ssl:
                tkinter.messagebox.showerror("FATAL!!", str(ssl) + str(ssl.__class__))
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)

        pb = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=400)

        myFont = font.Font(family='Arial', size=10, weight='bold')
        # print("Init Selec Source: ")
        # print(self.rest_url_textbox_source)
        button1 = tk.Button(self, text='Test Connection', relief='raised',
                            command=lambda: [test_connection(self.rest_url_textbox_source, username_textbox_source,
                                                             password_textbox_source, dropdown),
                                             Mapping.map_1(self, self.rest_url_textbox_source)])
        button1['font'] = myFont
        button1.place(relx=0.54, rely=0.73)

        button2 = tk.Button(self, text='Select Destination API →', state='disabled', relief='raised',
                            command=lambda: controller.show_frame("SelectionDestination"))
        button2['font'] = myFont
        button2.place(relx=0.84, rely=0.9)


class SelectionDestination(tk.Frame):
    def __init__(self, parent, controller):
        # global dropdown_value
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

        # def get_dropdown(event):
        #     global dropdown_value
        #     dropdown_value = dropdown.get()
        #     flag = True

        dropdown = Combobox(self, values=tools, state='readonly', width=20)
        dropdown.place(relx=0.5, rely=0.2)
        # dropdown.bind("<<ComboboxSelected>>", get_dropdown)

        label1 = tk.Label(self, text='Enter RESTFUL URL', bg='#fffdfd')
        label1.place(relx=0.41, rely=0.4)

        label2 = tk.Label(self, text='Enter Username', bg='#fffdfd')
        label2.place(relx=0.42, rely=0.5)

        label3 = tk.Label(self, text='Enter Password', bg='#fffdfd')
        label3.place(relx=0.42, rely=0.6)

        self.rest_url_textbox_destination = tk.Text(self, height=2, width=50, font="Arial 10")
        self.rest_url_textbox_destination.insert(tk.END,
                                                 'https://btp-hvm01633.swinfra.net/rest/488330779/ems/Person?layout=Name,Avatar')
        self.rest_url_textbox_destination.place(relx=0.64, rely=0.42, anchor="center")

        username_textbox_destination = tk.Text(self, height=2, width=50, font='Arial 10')
        username_textbox_destination.insert(tk.END, 'zaheeb')
        username_textbox_destination.place(relx=0.64, rely=0.53, anchor="center")

        password_textbox_destination = tk.Entry(self, width=50, font="Arial 10", show='*')
        password_textbox_destination.insert(tk.END, 'Automation_123')
        password_textbox_destination.place(relx=0.64, rely=0.63, anchor="center", height=37)

        def test_connection(rest_url_textbox_destination, username_textbox_destination,
                            password_textbox_destination,
                            dropdown):
            rest_url_textbox_data_destination = rest_url_textbox_destination.get("1.0", "end-1c")
            username_textbox_data_destination = username_textbox_destination.get("1.0", "end-1c")
            password_textbox_data_destination = password_textbox_destination.get()
            dropdown_value = dropdown.get()
            try:
                if not rest_url_textbox_data_destination or not username_textbox_data_destination \
                        or not password_textbox_data_destination or not dropdown_value:
                    tkinter.messagebox.showerror("FATAL!!", "Please fill all the fields")
                    return False
                elif 'lastupdatetime' in rest_url_textbox_data_destination.lower():
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "LastUpdateTime layout is already received from the REST Call, "
                                                   "Please remove 'LastUpdateTime' from the URI")
                    return False
                elif 'id' in rest_url_textbox_data_destination.lower():
                    tkinter.messagebox.showwarning("Layout Warning",
                                                   "ID layout is already received from the REST Call, "
                                                   "Please remove 'ID' from the URI")
                    return False
                else:
                    if dropdown.get() == 'SMAX':
                        url = rest_url_textbox_destination.get("1.0", "end-1c")

                        server_name_ip = url.split('/')[2]

                        tenant_id_1 = url.split('/')
                        res = [int(ele) if ele.isdigit() else ele for ele in tenant_id_1]
                        res1 = list(i for i in res if isinstance(i, int))
                        tenant_id = int(res1[0])

                        # server_name_ip = url.split('/')[2]
                        #
                        # tenant_id_find = url.find('TENANTID=')
                        # ampersand_find = url.find('&')
                        #
                        # tenant_id = url[tenant_id_find + 9:ampersand_find]
                        url_token = "https://" + str(
                            server_name_ip) + "/auth/authentication-endpoint/authenticate/login?TENANTID=" \
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
                        pb.pack()
                        pb.start()
                        time.sleep(2)
                        pb.stop()
                        pb.pack_forget()

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
                tkinter.messagebox.showerror("FATAL!!", ssl)
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                print("Exception type: ", exception_type)
                print("File name: ", filename)
                print("Line number: ", line_number)

        pb = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=400)

        myFont = font.Font(family='Arial', size=10, weight='bold')
        button1 = tk.Button(self, text='Test Connection', relief='raised',
                            command=lambda: [test_connection(self.rest_url_textbox_destination,
                                                             username_textbox_destination,
                                                             password_textbox_destination, dropdown),
                                             Mapping.map_2(self, self.rest_url_textbox_destination)])
        button1['font'] = myFont
        button1.place(relx=0.54, rely=0.73)

        button2 = tk.Button(self, text='Map APIs →', state='disabled', relief='raised',
                            command=lambda: controller.show_frame("Mapping"))
        button2['font'] = myFont
        button2.place(relx=0.84, rely=0.9)


class Mapping(SelectionSource, SelectionDestination):
    def __init__(self, parent, controller):
        global frame_canvas
        global source_variable
        global dropdown
        global button_create_json
        global button_transfer_one_entry
        global created_json_text_box
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

        myFont = font.Font(family='Arial', size=15, weight='bold', slant="italic")

        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='#fffdfd')
        var.set("  SOURCE API COLUMNS -----")
        # label.pack(side='left')
        label.grid(row=0, column=0)

        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='#fffdfd')
        var.set("DESTINATION API COLUMNS")
        # label.pack(side='right')
        label.grid(row=0, column=1)

        button_create_json = tk.Button(self, text='Create JSON Body', bg='pink', relief='ridge',
                                       width=17, height=2, fg='black',
                                       font=self.controller.button_font)
        button_create_json.place(relx=0.7, rely=0.1)

        # button_transfer_one_entry = tk.Button(self, text='Transfer One Entry', bg='pink', relief='ridge',
        #                                       width=17, height=2, fg='black', state='disabled')
        #
        # button_transfer_one_entry.place(relx=0.8, rely=0.4)
        created_json_text_box = tk.Text(self, width=75, height=23, bg='cyan')
        created_json_text_box.place(relx=0.5, rely=0.2)

        button_transfer_one_entry = tk.Button(self, text='Transfer One Entry', bg='pink',
                                              relief='ridge', width=17, height=2, fg='black',
                                              state='disabled', font=self.controller.button_font)

        button_transfer_one_entry.place(relx=0.7, rely=0.81)

    # @staticmethod
    def map_1(self, rest_url_textbox_source):
        global row_array_layout
        row_array_layout = []
        global row_array_dropdown
        row_array_dropdown = list()
        rest_url_textbox_data_source = rest_url_textbox_source.get("1.0", "end-1c")

        sp = rest_url_textbox_data_source.split('layout=')
        sp_layout = sp[-1]
        if '&' in sp_layout:
            layout = sp_layout.split('&')[0].split(',')

        else:
            layout = sp_layout.split(',')

        print(layout)
        layout.append('Id')
        # layout.append('LastUpdateTime')
        print(layout)
        x = 1
        for i in range(len(layout)):
            source_variable = tk.Text(frame_canvas, width=25, height=1, bg='#fffdfd', font=25)
            source_variable.insert(tk.END, layout[i])
            row_array_layout.append(source_variable)
            row_array_layout[i].grid(row=x, column=0, padx=5, pady=5)
            # source_variable.grid(row=x, column=0, padx=5, pady=5)
            # source_variable.bindtags((source_variable, self, "all"))
            row_array_layout[i].bindtags((source_variable, self, "all"))
            x += 1
        # button_create_json['command'] = lambda: Mapping.push_and_map(self, source_variable_mapping=row_array)
        # print(row_array)

    # @staticmethod
    def map_2(self, rest_url_textbox_destination):
        rest_url_textbox_data_destination = rest_url_textbox_destination.get("1.0", "end-1c")

        sp = rest_url_textbox_data_destination.split('layout=')
        sp_layout = sp[-1]
        # print(sp_layout)
        if '&' in sp_layout:
            # print('yes')
            options = sp_layout.split('&')[0].split(',')
            # print(options)

        else:
            options = sp_layout.split(',')
            # print(options)
        options.append('Id')
        # options.append('LastUpdateTime')
        y = 1
        for j in range(len(options)):
            dropdown = Combobox(frame_canvas, values=options, state='readonly', font=25)
            row_array_dropdown.append(dropdown)
            row_array_dropdown[j].grid(row=y, column=1, sticky="nsew", padx=10, pady=25)
            # dropdown.grid(row=y, column=1, padx=10, pady=25)
            y += 1
        button_create_json['command'] = lambda: Mapping.push_and_map(self, source_variable_mapping=row_array_layout,
                                                                     dropdown_value_mapping=row_array_dropdown)

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

        print(temp_source, temp_destination)
        print("&&&&&&&&&")

        # temp_source = sorted(temp_source)
        # temp_destination = sorted(temp_destination)

        print(temp_source, temp_destination)

        print("Push happened")

        with open('source.json') as sj:
            source_data = load(sj)
        # print(source_data)

        sorted_on_temp_source = []
        for del_last_update_time in source_data['entities']:
            prop = del_last_update_time['properties']
            prop.pop('LastUpdateTime')
            index_map = {v: i for i, v in enumerate(temp_source)}
            y = sorted(prop.items(), key=lambda pair: index_map[pair[0]])
            di = dict(y)
            sorted_on_temp_source.append(di)
        print(sorted_on_temp_source)

        # popping LastUpdateTime ---> Discard - added code to automatiocally add LastUpdateTime in both lists
        # for del_last_update_time in destination_data['entities']:
        #     prop = del_last_update_time['properties']
        #     prop.pop('LastUpdateTime')

        # print(destination_data)
        entitiy_type = source_data['entities'][0]['entity_type']
        operation = 'UPDATE'

        json_layout = [{"entities": [{"entity_type": entitiy_type, "properties": {}}], "operation": operation}]

        # Adding the indices of temp_destination in a format - {value: <value>}
        for i in range(len(temp_destination)):
            json_layout[0]['entities'][0]['properties'][temp_destination[i]] = '<' + temp_source[i] + '>'
        # print(json_layout)

        new_json_layout = []
        for i in range(len(source_data['entities'])):
            new_json_layout.append(json_layout[0])
        print(new_json_layout)

        for x in sorted_on_temp_source:
            for k, v in x.items():
                if "\'" in v:
                    v = v.replace('\'', "\\'")
                for y in new_json_layout:
                    pass
                new_json_layout = str(new_json_layout).replace('<' + k + '>', v, 1)

        print(new_json_layout)
        print(type(new_json_layout))
        print("String")
        new_json_layout_list = ast.literal_eval(new_json_layout)
        print(new_json_layout_list)
        print(type(new_json_layout_list))

        new_json_layout_json = dumps(new_json_layout_list, indent=4)
        with open("for_destination_updated_file.json", "w") as outfile:
            outfile.write(new_json_layout_json)
        print(new_json_layout_json)
        print(type(new_json_layout_json))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>")
        idk = loads(new_json_layout_json)
        print(idk[0])

        created_json_text_box.insert(tk.END, dumps(idk[0], indent=4))
        created_json_text_box['state'] = 'disabled'

        if len(loads(new_json_layout_json)) == len(source_data['entities']):
            tkinter.messagebox.showinfo("Success", "JSON Body Created Successfully")
            button_transfer_one_entry['state'] = 'normal'

        else:
            tkinter.messagebox.showerror("Error", "There was a problem parsing the JSON file, Please retry!")
            return False


if __name__ == "__main__":
    app = ToSMAXApp()
    app.mainloop()
