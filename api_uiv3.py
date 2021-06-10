from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
import itertools
import tkinter.messagebox
import requests
# global server_name_ip
from get_resultv3 import *


def fetch_source_data_button_func(server_name_ip_textbox_source, username_textbox_source,
                                  tenant_id_textbox_source, password_textbox_source,
                                  module_textbox_source, layout_textbox_source):
    try:
        server_name_ip = server_name_ip_textbox_source.get("1.0", "end-1c")
        username = username_textbox_source.get("1.0", "end-1c")
        password = password_textbox_source.get("1.0", "end-1c")
        tenant_id = tenant_id_textbox_source.get("1.0", "end-1c")
        module = module_textbox_source.get("1.0", "end-1c")
        layout = layout_textbox_source.get("1.0", "end-1c")
        print(server_name_ip, username, password, tenant_id, module, layout)

        # if not server_name_ip or not username or not password or not tenant_id or not module or not layout:
        #     tkinter.messagebox.showinfo("Source REST Call", "Entries can not be left blank")

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

        url_token = "https://" + str(server_name_ip) + "/auth/authentication-endpoint/authenticate/login?TENANTID=" + \
                    str(tenant_id)
        payload = {"Login": username, "Password": password}
        headers = {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
        response_token = requests.post(url_token, data=json.dumps(payload), headers=headers, verify=False)
        token = response_token.text

        # ---------------Get the details after receiving the TOKEN---------------#

        url_get = "https://" + str(server_name_ip) + "/rest/" + str(tenant_id) + "/ems/" + module + \
                  "?layout=" + layout
        headers = {
            "Content-Type": "application/json",
            "Cookie": "LWSSO_COOKIE_KEY={}".format(token)
        }
        response_data = requests.get(url_get, headers=headers, verify=False)
        print(response_data.status_code)
        source_data_get = response_data.content.decode('ascii')
        print(source_data_get)

        send_source_data(source_data_get)

    except Exception as ssl:
        print(ssl)
        print(ssl.__class__)
        tkinter.messagebox.showinfo("FATAL!!", ssl)


def fetch_destination_data_func(server_name_ip_textbox_destination, username_textbox_destination,
                                tenant_id_textbox_destination, password_textbox_destination,
                                module_textbox_destination, layout_textbox_destination):
    pass


def get_requests_destination(destination_api_textbox):
    try:
        url = destination_api_textbox.get("1.0", "end-1c")
        print(url)
    except Exception as e:
        print(e)
        tkinter.messagebox.showinfo("FATAL!!", e)


def design_get_api(LeftFrame0):
    # --------------------Labels for API URL-------------------#

    var = StringVar()
    label = Label(LeftFrame0, textvariable=var, width=17, height=2)
    var.set("Source REST Call")
    # label.grid(row=0, column=1, padx=10, pady=10)
    # label.grid()
    label.place(relx=0.5, rely=0.04, anchor="center")

    var = StringVar()
    label = Label(LeftFrame0, textvariable=var, width=17, height=2)
    var.set("Destination REST Call")
    # label.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")
    # label.grid()
    label.place(relx=0.5, rely=0.58, anchor="center")

    # --------------------Drop down for API GET/POST-------------------#

    # drop = ttk.Combobox(LeftFrame0, state='readonly', values=["GET", "POST", "PUT", "DELETE"])
    # drop.grid(row=0, column=0, sticky="nsew", padx=10, pady=15)
    #
    # drop = ttk.Combobox(LeftFrame0, state='readonly', values=["GET", "POST", "PUT", "DELETE"])
    # drop.grid(row=2, column=0, sticky="nsew", padx=10, pady=15)

    # --------------------Text box for API URL-------------------#
    # ---------------------------Source---------------------------#

    server_name_ip_textbox_source = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    server_name_ip_textbox_source.insert(END, 'Enter the FQDN/IP of Server')
    # server_name_ip_textbox.grid(row=1, column=0, padx=10, pady=10)
    server_name_ip_textbox_source.place(relx=0.25, rely=0.13, anchor="center")

    username_textbox_source = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    username_textbox_source.insert(END, 'Enter the username')
    # username_textbox_source.grid(row=1, column=1, padx=10, pady=10)
    username_textbox_source.place(relx=0.74, rely=0.13, anchor="center")

    tenant_id_textbox_source = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    tenant_id_textbox_source.insert(END, 'Enter the Tenant ID')
    # tenant_id_textbox.grid(row=2, column=0, padx=10, pady=10)
    tenant_id_textbox_source.place(relx=0.25, rely=0.21, anchor="center")

    password_textbox_source = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    password_textbox_source.insert(END, 'Enter the Password')
    # password_textbox.grid(row=2, column=1, padx=10, pady=10)
    password_textbox_source.place(relx=0.74, rely=0.21, anchor="center")

    module_textbox_source = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    module_textbox_source.insert(END, 'Module- Eg: Incident,Change')
    module_textbox_source.place(relx=0.25, rely=0.29, anchor="center")

    layout_textbox_source = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    layout_textbox_source.insert(END, 'Layout')
    layout_textbox_source.place(relx=0.74, rely=0.29, anchor="center")

    # ---------------------------Destination---------------------------#

    server_name_ip_textbox_destination = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    server_name_ip_textbox_destination.insert(END, 'Enter the FQDN/IP of Server')
    # server_name_ip_textbox.grid(row=1, column=0, padx=10, pady=10)
    server_name_ip_textbox_destination.place(relx=0.25, rely=0.67, anchor="center")

    username_textbox_destination = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    username_textbox_destination.insert(END, 'Enter the username')
    # username_textbox.grid(row=1, column=1, padx=10, pady=10)
    username_textbox_destination.place(relx=0.74, rely=0.67, anchor="center")

    tenant_id_textbox_destination = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    tenant_id_textbox_destination.insert(END, 'Enter the Tenant ID')
    # tenant_id_textbox.grid(row=2, column=0, padx=10, pady=10)
    tenant_id_textbox_destination.place(relx=0.25, rely=0.75, anchor="center")

    password_textbox_destination = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    password_textbox_destination.insert(END, 'Enter the Password')
    # password_textbox.grid(row=2, column=1, padx=10, pady=10)
    password_textbox_destination.place(relx=0.74, rely=0.75, anchor="center")

    module_textbox_destination = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    module_textbox_destination.insert(END, 'Module- Eg: Incident,Change')
    module_textbox_destination.place(relx=0.25, rely=0.83, anchor="center")

    layout_textbox_destination = Text(LeftFrame0, height=2, width=25, font="Arial 10")
    layout_textbox_destination.insert(END, 'Layout')
    layout_textbox_destination.place(relx=0.74, rely=0.83, anchor="center")

    # --------------------Button for API URL-------------------#

    fetch_source_data_button = Button(LeftFrame0, relief=RAISED, text="↑ Fetch Source Data", height=2,
                                      width=30,
                                      command=lambda: fetch_source_data_button_func(server_name_ip_textbox_source,
                                                                                    username_textbox_source,
                                                                                    tenant_id_textbox_source,
                                                                                    password_textbox_source,
                                                                                    module_textbox_source,
                                                                                    layout_textbox_source)
                                      )
    fetch_source_data_button.place(relx=0.5, rely=0.40, anchor="center")

    fetch_destination_data_button = Button(LeftFrame0, relief=RAISED, text="↑ Fetch Destination Data", height=2,
                                           width=30,
                                           command=lambda: fetch_destination_data_func(
                                               server_name_ip_textbox_destination,
                                               username_textbox_destination,
                                               tenant_id_textbox_destination,
                                               password_textbox_destination,
                                               module_textbox_destination,
                                               layout_textbox_destination))
    fetch_destination_data_button.place(relx=0.50, rely=0.93, anchor="center")
