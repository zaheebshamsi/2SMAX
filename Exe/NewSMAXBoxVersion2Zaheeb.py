import threading
import time
from tkinter.ttk import Combobox
import tkinter.font as font
import requests
import sys
import tkinter as tk
from tkinter import font as tkfont, ttk
import tkinter.messagebox
from json import dumps, loads
from PIL import ImageTk, Image


class ToSMAXApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Arial', size=20, weight="bold", slant="italic")

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
        # rest_url_textbox.insert(tk.END, '')
        self.rest_url_textbox_source.place(relx=0.64, rely=0.42, anchor="center")

        username_textbox_source = tk.Text(self, height=2, width=50, font='Arial 10')
        # rest_url_textbox.insert(tk.END, '')
        username_textbox_source.place(relx=0.64, rely=0.53, anchor="center")

        password_textbox_source = tk.Entry(self, width=50, font="Arial 10", show='*')
        # rest_url_textbox.insert(tk.END, '')
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
                    return
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
                            token = response.text

                            headers = {"Content-Type": "application/json",
                                       "Cookie": "LWSSO_COOKIE_KEY={}".format(token)}

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
                    return

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
        # rest_url_textbox.insert(tk.END, '')
        self.rest_url_textbox_destination.place(relx=0.64, rely=0.42, anchor="center")

        username_textbox_destination = tk.Text(self, height=2, width=50, font='Arial 10')
        # rest_url_textbox.insert(tk.END, '')
        username_textbox_destination.place(relx=0.64, rely=0.53, anchor="center")

        password_textbox_destination = tk.Entry(self, width=50, font="Arial 10", show='*')
        # rest_url_textbox.insert(tk.END, '')
        password_textbox_destination.place(relx=0.64, rely=0.63, anchor="center", height=37)

        def test_connection(rest_url_textbox_destination, username_textbox_destination, password_textbox_destination,
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
                            token = response.text

                            headers = {"Content-Type": "application/json",
                                       "Cookie": "LWSSO_COOKIE_KEY={}".format(token)}

                            response = requests.get(rest_url_textbox_data_destination, headers=headers, verify=False)
                            if response.status_code == 200:
                                result_json = response.content.decode('utf-8')
                                result_json_to_file = loads(result_json)
                                self.json_file = dumps(result_json_to_file, indent=4)
                                with open("destination.json", "w") as outfile:
                                    outfile.write(self.json_file)
                            else:
                                tkinter.messagebox.showwarning("Response",
                                                               "Response Code: " + str(response.status_code))
                                return False
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
                    return True

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
        self.bind('<Return>', lambda: [test_connection(self.rest_url_textbox_destination,
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
        canvas.pack()
        canvas.create_window((0, 0), window=frame_canvas, anchor='nw')
        frame_canvas.bind_all("<Configure>", scrollbar_bind)

        myFont = font.Font(family='Arial', size=15, weight='bold')

        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='#fffdfd')
        var.set("     SOURCE API COLUMNS -----")
        # label.pack(side='left')
        label.grid(row=0, column=0)

        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=myFont, bg='#fffdfd')
        var.set("DESTINATION API COLUMNS")
        # label.pack(side='right')
        label.grid(row=0, column=1)

        # x = 1
        # for i in layout:
        #     source_variable = tk.Text(frame_canvas, width=25, height=2, bg='#fffdfd', font=25)
        #     source_variable.insert(tk.END, i)
        #     source_variable.grid(row=x, column=0, padx=5, pady=5)
        #     source_variable.bindtags((source_variable, self, "all"))
        #     x += 1

        # options = ['Id', 'Name', 'Email']

        # y = 1
        # for j in range(len(layout)):
        #     dropdown = Combobox(frame_canvas, values=options, state='readonly', font=25)
        #     dropdown.grid(row=y, column=1, padx=10, pady=25)
        #     y += 1

        button_push = tk.Button(self, text='PUSH', width=17, height=2)
        # button_push.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        button_push.place(relx=0.8, rely=0.2)

    # @staticmethod
    def map_1(self, rest_url_textbox_source):
        rest_url_textbox_data_source = rest_url_textbox_source.get("1.0", "end-1c")

        sp = rest_url_textbox_data_source.split('layout=')
        sp_layout = sp[-1]
        if '&' in sp_layout:
            layout = sp_layout.split('&')[0].split(',')

        else:
            layout = sp_layout.split(',')

        x = 1
        for i in layout:
            source_variable = tk.Text(frame_canvas, width=25, height=2, bg='#fffdfd', font=25)
            source_variable.insert(tk.END, i)
            source_variable.grid(row=x, column=0, padx=5, pady=5)
            source_variable.bindtags((source_variable, self, "all"))
            x += 1

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
        y = 1
        for j in range(len(options)):
            dropdown = Combobox(frame_canvas, values=options, state='readonly', font=25)
            dropdown.grid(row=y, column=1, padx=10, pady=25)
            y += 1


if __name__ == "__main__":
    app = ToSMAXApp()
    app.mainloop()
