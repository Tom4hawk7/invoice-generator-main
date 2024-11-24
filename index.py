from customtkinter import *
from tkinter import ttk
from datetime import datetime
from client_form import ClientForm
from invoice_generator import generate_invoice
import database

# set appearance
set_appearance_mode("System")
set_default_color_theme("blue")

# instatiate the application
class App(CTk):
    def __init__(self):
        super().__init__()

        self.title("Invoice generator")
        self.geometry("900x350")

        self.invoice_form = InvoiceForm(self)

        columns = ("date", "description", "item_number", "unit_price")
        self.invoice_viewer = ttk.Treeview(master=self, columns=columns, show="headings")

        # define the headings
        # TODO fix the scaling issues
        self.invoice_viewer.heading("date", text="Date")
        self.invoice_viewer.heading("description", text="Service Description")
        self.invoice_viewer.heading("item_number", text="Item No.")
        self.invoice_viewer.heading("unit_price", text="Unit Price")

        self.invoice_viewer.grid(row=2, column=0, columnspan=5, padx=30, pady=10, sticky="news")

        # TODO add a command to this that uses sql data
        self.add_client_button = CTkButton(self, text="Create Client", command=self.open_client_form)
        self.add_client_button.grid(row=3, column=0, columnspan=5, sticky="news", padx=20, pady=5)

        self.client_form = None
        self.invoice_generation_label = None

        # TODO also add a command to this that uses sql data
        self.generate_invoice_button = CTkButton(self, text="Generate Invoice", command=self.create_invoice)
        self.generate_invoice_button.grid(row=4, column=0, columnspan=5, sticky="news", padx=20, pady=5)

    def open_client_form(self):
        if self.client_form is None or not self.client_form.winfo_exists():
            self.client_form = ClientForm(self)
        else:
            self.client_form.focus()
    
    def create_invoice(self):
        generate_invoice()

        if self.invoice_generation_label is None:
            self.invoice_generation_label = CTkLabel(self, text="Client Invoice Generated")
            self.invoice_generation_label.grid(row=5, column=0, columnspan=5, sticky="news", padx=20, pady=5)


# define the client names
client_list = database.retrieve_client_session_info()

client_names = []
if len(client_list) != 0:
    for client in client_list:
        id_and_name = f"{client["id"]} {client["name"]}"
        client_names.append(id_and_name)

# define constants for calculating invoice variables
PRICE_PER_HOUR = 193.99
MINUTES_PER_HOUR = 60

# define the client identifiers
class InvoiceForm(CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.client_menu_value = StringVar(value="Select a client")

        self.client_menu = CTkOptionMenu(master, values=client_names, variable=self.client_menu_value, command=self.switch_client)
        self.client_menu.grid(row=0, column=0, padx=20, pady=20)

        self.date = CTkEntry(master, placeholder_text="Date: DD/MM/YYYY")
        self.date.insert(END, datetime.today().strftime("%d/%m/%Y"))
        self.date.grid(row=0, column=1, padx=20, pady=20)

        self.minutes = CTkEntry(master, placeholder_text="Minutes")
        self.minutes.grid(row=0, column=2, padx=20, pady=20)

        self.description = CTkEntry(master, placeholder_text="Description")
        self.description.grid(row=0, column=3, padx=20, pady=20)

        self.submit = CTkButton(master, text="Add Session", command=self.add_session)
        self.submit.grid(row=0, column=4,  padx=20, pady=20)

        # columns = ("Date", "Service Description", "Item No.", "Unit Price")
        # self.invoice_viewer = InvoiceViewer(master=self, columns=columns, show="headings")
    
    def add_session(self):
        # obtain values from the input fields
        option = self.client_menu.get()

        # date = datetime.strptime(self.date.get(), "%d/%m/%Y").date()
        date = self.date.get()
        minutes = int(self.minutes.get())
        description = self.description.get()
        
        # calculate derived values
        price = round(PRICE_PER_HOUR * minutes / MINUTES_PER_HOUR, 2)
        total_description = f"Speech pathology services - {minutes} - {description}"

        # loop through clients and find one with right identifiers
        for client in client_list:
            client_identifiers = f"{client["id"]} {client["name"]}"
            if option == client_identifiers:
                client_id = client["id"]
                item_number = client["item_number"]
                break
        # TODO might want to add a "break" statement after this if statement
        
        # TODO remember this when populating the tree upon switch
        session_info = [date, total_description, item_number, price]
        app.invoice_viewer.insert("", 0, values=session_info)

        # store this in the database
        session = [(date, total_description, item_number, price, client_id)]
        database.add_session(session)
        
        # clear out the input fields
        self.minutes.delete(0, END)
        self.description.delete(0, END)
    
    def switch_client(self, value):

        # NOTE thought I found a really annoying bug here
        # then i realised this function was being given two positional arguments
        # i added another variable to the input and found out that the
        # callback function automatically gives you the value of the option selected
        # how cool! and also extremely annoying

        # i swear i don't like duplicated code as much as it seems
        # this is just a hacky tool so mum doesn't have to spend a full day doing invoices
        # full-fledged application will come later
        
        # clears the table when switching to a new client
        for item in app.invoice_viewer.get_children():
            app.invoice_viewer.delete(item)

        # get the sessions for the respective client
        for client in client_list:
            client_identifiers = f"{client["id"]} {client["name"]}"
            if value == client_identifiers:
                client_id = client["id"]
                break
        
        sessions = database.retreive_sessions(client_id)

        for session in sessions:
            app.invoice_viewer.insert("", 0, values=session)
        # apparently tuples work brilliant here, who would've thought
        # guess the underlying method goes through them with an iterator
        # session[i]


app = App()
app.mainloop()