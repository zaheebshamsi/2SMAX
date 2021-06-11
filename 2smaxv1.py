try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
    from PIL.ImageTk import PhotoImage
    import tkinter.messagebox
    import os
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2

    os.system('pip install PIL')


class ToSMAXApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

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
        print(self.frames)

        self.show_frame("ApiPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        print(page_name)
        frame = self.frames[page_name]
        frame.tkraise()


class ApiPage(tk.Frame):
    def __init__(self, parent, controller):
        def fetch_source_data_button_func(server_name_ip_textbox_source,
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
            except Exception as ssl:
                print(ssl)
                print(ssl.__class__)
                tkinter.messagebox.showinfo("FATAL!!", ssl)

        tk.Frame.__init__(self, parent, background='#1a2933')
        self.controller = controller
        # label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)

        img = PhotoImage(file="C:/Users/ZShamsi/Downloads/zaheebimg.png")  # make sure to add "/" not "\"
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
                                                              fetch_source_data_button_func(server_name_ip_textbox_source,
                                                                                            username_textbox_source,
                                                                                            tenant_id_textbox_source,
                                                                                            password_textbox_source,
                                                                                            module_textbox_source,
                                                                                            layout_textbox_source)])
        # command=self.sequence(controller.show_frame("ResultsPage")))

        # fetch_source_data_button = tk.Button(self, relief='raised', text="↑ Fetch Source Data", height=2,
        #                                   width=30,
        #                                   command=lambda: fetch_source_data_button_func(server_name_ip_textbox_source,
        #                                                                                 username_textbox_source,
        #                                                                                 tenant_id_textbox_source,
        #                                                                                 password_textbox_source,
        #                                                                                 module_textbox_source,
        #                                                                                 layout_textbox_source)
        fetch_source_data_button.place(relx=0.5, rely=0.40, anchor="center")

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("ApiPage"))
        button.pack()


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
