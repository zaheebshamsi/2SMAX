from tkinter.ttk import Combobox

import requests
from requests import get, post
import sys
import tkinter as tk
from tkinter import font as tkfont
import tkinter.messagebox
from json import dumps, loads, load, dump


class ToSMAXApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.title("Microfocus 2SMAX")
        self.geometry("1350x800+0+0")
        self.state("zoomed")
        container = tk.Frame(self, bd=20, width=1280, height=1057, bg="#24353d", padx=20, pady=20,  # F1F2F3 #0073e7
                             relief='ridge')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ApiPage, ResultsPage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ApiPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class ApiPage(tk.Frame):
    def fetch_source_data_button_func2(self,
                                       server_name_ip_textbox_source,
                                       username_textbox_source,
                                       tenant_id_textbox_source,
                                       password_textbox_source,
                                       module_textbox_source,
                                       layout_textbox_source):
        print(server_name_ip_textbox_source.get("1.0", "end-1c"))
        return server_name_ip_textbox_source.get("1.0", "end-1c")

    def __init__(self, parent, controller):

        def fetch_source_data_button_func1(server_name_ip_textbox_source,
                                           username_textbox_source,
                                           tenant_id_textbox_source,
                                           password_textbox_source,
                                           module_textbox_source,
                                           layout_textbox_source):
            try:
                server_name_ip = server_name_ip_textbox_source.get("1.0", "end-1c")
                username = username_textbox_source.get("1.0", "end-1c")
                password = password_textbox_source.get("1.0", "end-1c")
                tenant_id = tenant_id_textbox_source.get("1.0", "end-1c")
                module = module_textbox_source.get("1.0", "end-1c")
                layout = layout_textbox_source.get("1.0", "end-1c")

                print(server_name_ip, username, password, tenant_id, module, layout)
                print("This is inside seq")

                if server_name_ip == "Enter the FQDN/IP of Server":
                    server_name_ip = None
                if username == "Enter the username":
                    username = None
                if password == "Enter the Password":
                    password = None
                if tenant_id == "Enter the Tenant ID":
                    tenant_id = None
                if module == "Module- Eg: Incident,Change":
                    module = None
                if layout == "":
                    pass

                if server_name_ip is None or username is None or password is None or \
                        tenant_id is None or module is None or layout is None:
                    tkinter.messagebox.showinfo("Source REST Call", "Entries can not be default text, "
                                                                    "Please remove default text from the entry box")
                    return False

                url_token = "https://" + str(
                    server_name_ip) + "/auth/authentication-endpoint/authenticate/login?TENANTID=" + \
                            str(tenant_id)
                payload = {"Login": username, "Password": password}
                headers = {
                    "Content-Type": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept": "*/*",
                    "Connection": "keep-alive"
                }
                response_token = post(url_token, data=dumps(payload), headers=headers, verify=False)
                token = response_token.text

                # ---------------Get the details after receiving the TOKEN---------------#

                url_get = "https://" + str(server_name_ip) + "/rest/" + str(tenant_id) + "/ems/" + module + \
                          "?layout=" + layout
                headers = {
                    "Content-Type": "application/json",
                    "Cookie": "LWSSO_COOKIE_KEY={}".format(token)
                }
                response_data = get(url_get, headers=headers, verify=False)
                print(response_data.status_code)
                source_data_get = response_data.content.decode('ascii')
                source_data_get_json = loads(source_data_get)

                json_file = dumps(source_data_get_json, indent=4)
                print(json_file)
                print(type(json_file))
                print(type(source_data_get_json))
                return json_file

            except Exception as ssl:
                print(ssl)
                print(ssl.__class__)
                tkinter.messagebox.showwarning("FATAL!!", ssl)

        tk.Frame.__init__(self, parent, background='#1a2933')
        self.controller = controller
        # label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)

        # img = PhotoImage(file="C:/Users/ZShamsi/Downloads/zaheebimg.png")  # make sure to add "/" not "\"
        button1 = tk.Button(self, text="Go to Results Page", bg='powder blue', fg='black', relief='raised',
                            command=lambda: controller.show_frame("ResultsPage"))
        # button1.config(image=img)
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack(side="right")
        button2.pack(side="left")

        var = tk.StringVar()
        label = tk.Label(self, textvariable=var, width=17, height=2)
        var.set("Source REST Call")
        # label.grid(row=0, column=1, padx=10, pady=10)
        # label.grid()
        label.place(relx=0.5, rely=0.04, anchor="center")

        var = tk.StringVar()
        label = tk.Label(self, textvariable=var, width=17, height=2)
        var.set("Destination REST Call")
        # label.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")
        # label.grid()
        label.place(relx=0.5, rely=0.58, anchor="center")

        # --------------------Text box for API URL-------------------#
        # ---------------------------Source---------------------------#

        server_name_ip_textbox_source = tk.Text(self, height=2, width=25, font="Arial 10")
        # server_name_ip_textbox_source.insert(END, 'Enter the FQDN/IP of Server')
        server_name_ip_textbox_source.insert(tk.END, 'btp-hvm01633.swinfra.net')
        # server_name_ip_textbox.grid(row=1, column=0, padx=10, pady=10)
        server_name_ip_textbox_source.place(relx=0.25, rely=0.13, anchor="center")

        username_textbox_source = tk.Text(self, height=2, width=25, font="Arial 10")
        # username_textbox_source.insert(END, 'Enter the username')
        username_textbox_source.insert(tk.END, 'zaheeb')
        # username_textbox_source.grid(row=1, column=1, padx=10, pady=10)
        username_textbox_source.place(relx=0.74, rely=0.13, anchor="center")

        tenant_id_textbox_source = tk.Text(self, height=2, width=25, font="Arial 10")
        # tenant_id_textbox_source.insert(END, 'Enter the Tenant ID')
        tenant_id_textbox_source.insert(tk.END, '488330779')
        # tenant_id_textbox.grid(row=2, column=0, padx=10, pady=10)
        tenant_id_textbox_source.place(relx=0.25, rely=0.21, anchor="center")

        password_textbox_source = tk.Text(self, height=2, width=25, font="Arial 10")
        # password_textbox_source.insert(END, 'Enter the Password')
        password_textbox_source.insert(tk.END, 'Automation_123')
        # password_textbox.grid(row=2, column=1, padx=10, pady=10)
        password_textbox_source.place(relx=0.74, rely=0.21, anchor="center")

        module_textbox_source = tk.Text(self, height=2, width=25, font="Arial 10")
        # module_textbox_source.insert(END, 'Module- Eg: Incident,Change')
        module_textbox_source.insert(tk.END, 'Person')
        module_textbox_source.place(relx=0.25, rely=0.29, anchor="center")

        layout_textbox_source = tk.Text(self, height=2, width=25, font="Arial 10")
        # layout_textbox_source.insert(END, 'Layout')
        layout_textbox_source.insert(tk.END, 'Id,Name,Email')
        layout_textbox_source.place(relx=0.74, rely=0.29, anchor="center")

        # ---------------------------Destination---------------------------#

        server_name_ip_textbox_destination = tk.Text(self, height=2, width=25, font="Arial 10")
        server_name_ip_textbox_destination.insert(tk.END, 'Enter the FQDN/IP of Server')
        # server_name_ip_textbox.grid(row=1, column=0, padx=10, pady=10)
        server_name_ip_textbox_destination.place(relx=0.25, rely=0.67, anchor="center")

        username_textbox_destination = tk.Text(self, height=2, width=25, font="Arial 10")
        username_textbox_destination.insert(tk.END, 'Enter the username')
        # username_textbox.grid(row=1, column=1, padx=10, pady=10)
        username_textbox_destination.place(relx=0.74, rely=0.67, anchor="center")

        tenant_id_textbox_destination = tk.Text(self, height=2, width=25, font="Arial 10")
        tenant_id_textbox_destination.insert(tk.END, 'Enter the Tenant ID')
        # tenant_id_textbox.grid(row=2, column=0, padx=10, pady=10)
        tenant_id_textbox_destination.place(relx=0.25, rely=0.75, anchor="center")

        password_textbox_destination = tk.Text(self, height=2, width=25, font="Arial 10")
        password_textbox_destination.insert(tk.END, 'Enter the Password')
        # password_textbox.grid(row=2, column=1, padx=10, pady=10)
        password_textbox_destination.place(relx=0.74, rely=0.75, anchor="center")

        module_textbox_destination = tk.Text(self, height=2, width=25, font="Arial 10")
        module_textbox_destination.insert(tk.END, 'Module- Eg: Incident,Change')
        module_textbox_destination.place(relx=0.25, rely=0.83, anchor="center")

        layout_textbox_destination = tk.Text(self, height=2, width=25, font="Arial 10")
        layout_textbox_destination.insert(tk.END, 'Layout')
        layout_textbox_destination.place(relx=0.74, rely=0.83, anchor="center")

        # --------------------Button for API URL-------------------#
        fetch_source_data_button = tk.Button(self, relief='raised', text="↑ Fetch Source Data", height=2, width=30,
                                             command=lambda: [controller.show_frame("ResultsPage"),
                                                              ResultsPage.fetch_source_data_button_func(
                                                                  self,
                                                                  server_name_ip_textbox_source,
                                                                  username_textbox_source,
                                                                  tenant_id_textbox_source,
                                                                  password_textbox_source,
                                                                  module_textbox_source,
                                                                  layout_textbox_source)])
        fetch_source_data_button.place(relx=0.5, rely=0.40, anchor="center")
        # command=self.sequence(controller.show_frame("ResultsPage")))

        # fetch_source_data_button = tk.Button(self, relief='raised', text="↑ Fetch Source Data", height=2,
        #                                   width=30,
        #                                   command=lambda: fetch_source_data_button_func(server_name_ip_textbox_source,
        #                                                                                 username_textbox_source,
        #                                                                                 tenant_id_textbox_source,
        #                                                                                 password_textbox_source,
        #                                                                                 module_textbox_source,
        #                                                                                 layout_textbox_source)

        fetch_destination_data_button = tk.Button(self, relief='raised', text="↑ Fetch Destination Data", height=2,
                                                  width=30)

        # fetch_destination_data_button = tk.Button(self, relief='raised', text="↑ Fetch Destination Data", height=2,
        #                                        width=30,
        #                                        command=lambda: fetch_destination_data_func(
        #                                            server_name_ip_textbox_destination,
        #                                            username_textbox_destination,
        #                                            tenant_id_textbox_destination,
        #                                            password_textbox_destination,
        #                                            module_textbox_destination,
        #                                            layout_textbox_destination))
        fetch_destination_data_button.place(relx=0.50, rely=0.93, anchor="center")


class ResultsPage(tk.Frame):
    @staticmethod
    def fetch_source_data_button_func(server_name_ip_textbox_source,
                                      username_textbox_source,
                                      tenant_id_textbox_source,
                                      password_textbox_source,
                                      module_textbox_source,
                                      layout_textbox_source):
        try:
            max_tries = 5
            attempt = 0

            server_name_ip = server_name_ip_textbox_source.get("1.0", "end-1c")
            username = username_textbox_source.get("1.0", "end-1c")
            password = password_textbox_source.get("1.0", "end-1c")
            tenant_id = tenant_id_textbox_source.get("1.0", "end-1c")
            module = module_textbox_source.get("1.0", "end-1c")
            layout = layout_textbox_source.get("1.0", "end-1c")

            print(server_name_ip, username, password, tenant_id, module, layout)
            print("This is inside seq")

            if server_name_ip == "Enter the FQDN/IP of Server":
                server_name_ip = None
            if username == "Enter the username":
                username = None
            if password == "Enter the Password":
                password = None
            if tenant_id == "Enter the Tenant ID":
                tenant_id = None
            if module == "Module- Eg: Incident,Change":
                module = None
            if layout == "":
                pass

            if server_name_ip is None or username is None or password is None or \
                    tenant_id is None or module is None or layout is None:
                tkinter.messagebox.showinfo("Source REST Call", "Entries can not be default text, "
                                                                "Please remove default text from the entry box")
                return False

            url_token = "https://" + str(
                server_name_ip) + "/auth/authentication-endpoint/authenticate/login?TENANTID=" + \
                        str(tenant_id)
            payload = {"Login": username, "Password": password}
            headers = {
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
                "Connection": "keep-alive"
            }
            while attempt <= max_tries:
                response_token = post(url_token, data=dumps(payload), headers=headers, verify=False)
                token = response_token.text

                # ---------------Get the details after receiving the TOKEN---------------#

                url_get = "https://" + str(server_name_ip) + "/rest/" + str(tenant_id) + "/ems/" + module + \
                          "?layout=" + layout
                headers = {
                    "Content-Type": "application/json",
                    "Cookie": "LWSSO_COOKIE_KEY={}".format(token)
                }
                response_data = get(url_get, headers=headers, verify=False)
                source_data_get = response_data.content.decode('utf-8')
                source_data_get_json = loads(source_data_get)
                json_file = dumps(source_data_get_json, indent=4)
                with open("snow.json", "w") as outfile:
                    outfile.write(json_file)

                # ---------------Display JSON keys as labels---------------#
                with open('snow.json') as env:
                    data = load(env)
                res = list()
                for json_data_get_response in data['entities']:
                    # print(json_data_get_response)
                    for json_data_key in json_data_get_response['properties'].keys():
                        res.append(json_data_key)
                remove_duplicates_from_json = []
                [remove_duplicates_from_json.append(x) for x in res if x not in remove_duplicates_from_json]
                print(remove_duplicates_from_json)
                # dumps(source_data_get_json, indent=4)

        except Exception as ssl:
            print(ssl)
            print(ssl.__class__)
            tkinter.messagebox.showwarning("FATAL!!", ssl)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#1a2933')
        self.controller = controller
        self.task(controller)

    def task(self, controller):
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=517, height=570)  # 1179 full screen
            print('in mf')

        self.controller = controller
        canvas = tk.Canvas(self, bg='powder blue')
        frame_canvas = tk.Frame(canvas, bg='cyan')
        myscrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        canvas.pack()
        canvas.create_window((0, 0), window=frame_canvas, anchor='nw')
        print('before mf')
        frame_canvas.bind_all("<Configure>", myfunction)
        print('after mf')

        # label = tk.Labelframe_canvas(frame, text="This is Results Page", font=controller.title_font)
        # label.pack(side="top", pady=10)
        #
        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=controller.title_font)
        var.set("Source API Variables")
        label.grid(row=0, column=0)
        # label.place(relx=0.2, rely=0.1, anchor="center")

        var = tk.StringVar()
        label = tk.Label(frame_canvas, textvariable=var, font=controller.title_font)
        var.set("SMAX API Variables")
        label.grid(row=0, column=3)
        # label.place(relx=0.51, rely=0.1, anchor="center")

        button = tk.Button(self, text="Go to the API page", relief='raised', height=2, width=30,
                           command=lambda: controller.show_frame("ApiPage"))
        button.place(relx=0.87, rely=0.5, anchor="center")  # relx=0.8, rely=0.1

        button_push = tk.Button(self, text="Push", relief='raised', height=2, width=30,
                                command=lambda: controller.show_frame("ApiPage"))
        button_push.place(relx=0.87, rely=0.4, anchor="center")  # relx=0.8, rely=0.1
        # ResultsPage.loads_json()

        # scrollbar_source = tk.Scrollbar(self, orient="vertical")
        # scrollbar_source.pack(side='right', fill='y')

        zzz = ['Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name',
               'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id',
               'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email',
               'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name',
               'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id', 'Email', 'Name', 'Id',
               'Email']
        x = 1
        y = 0
        for xxx in zzz:
            textbox_source_variables = tk.Text(frame_canvas, height=2, width=25, fg='black', font=controller.title_font,
                                               bg='powder blue')
            textbox_source_variables.insert(tk.END, xxx)
            # textbox_source_variables.place(relx=x, rely=y, anchor="center")
            textbox_source_variables.grid(row=x, column=y, padx=10, pady=10)
            textbox_source_variables.bindtags((textbox_source_variables, self, "all"))
            x = x + 1

        options = ["Ticket Number", "Ticket Age", "Email", "First Name", "Middle Name", "Last Name", "Emp ID",
                   "Problem Description", "Technician Name", "Solution Description", "Resolution Time (min)"]

        for i in range(len(zzz)):
            drop = Combobox(frame_canvas, state='readonly', values=options, font="20")
            drop.grid(row=i + 1, column=3, sticky="nsew", padx=10, pady=15)
        # scrollbar_source.config(command=textbox_source_variables.yview)
        # listbox = tk.Listbox(self, yscrollcommand=scrollbar_source.set, bg='#1a2933', fg='black', height=25,
        #                      font=controller.title_font, relief='ridge', borderwidth=0, highlightthickness=0,
        #                      background=self.cget("background"))
        # for label_json_key in zzz:
        #     i += 1
        #     listbox.insert(tk.END, str(label_json_key))
        # # listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        # listbox.place(relx=0.2, rely=0.58, anchor="center")
        # listbox.bindtags((listbox, self, "all"))
        # var = tk.StringVar()

        # label_show_json_source_variable = tk.Label(self, textvariable=var, bd=5, relief='ridge',
        #                                            # padx=5, pady=5,
        #                                            width=20, bg='black', fg='white', font=controller.title_font)
        # var.set(label_json_key)
        # label_show_json_source_variable.place(relx=x, rely=y, anchor="center")
        # y = y + 0.1
        # # x = x + 0.05
        # print(x, y)

        # scrollbar_source.config(command=label_show_json_source_variable.yview)
        # label.grid(row=i, column=1, sticky="nsew", padx=12, pady=12)
        # label.bind("<Key>", update_size)

    @staticmethod
    def loads_json():
        data = ResultsPage.fetch_source_data_button_func
        print("This is data", data)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("ApiPage"))
        button.pack()


if __name__ == "__main__":
    app = ToSMAXApp()
    app.mainloop()
