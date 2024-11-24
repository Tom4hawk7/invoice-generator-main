from customtkinter import *
from database import add_client
from datetime import datetime

PADX=15
PADY=10
WIDTH=300
today = datetime.today()

class ClientForm(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Client Creator")

        # TODO Make sure these fields clear once you click submit

        # name
        self.name = CTkEntry(self, placeholder_text="Name", width=WIDTH)
        self.name.pack(padx=PADX, pady=PADY)

        # date of birth
        self.dob = CTkEntry(self, placeholder_text="Date of birth: DD/MM/YYYY", width=WIDTH)
        self.dob.pack(padx=PADX, pady=PADY)

        # parent
        self.parent = CTkEntry(self, placeholder_text="Parent", width=WIDTH)
        self.parent.pack(padx=PADX, pady=PADY)

        # email
        self.email = CTkEntry(self, placeholder_text="Email", width=WIDTH)
        self.email.pack(padx=PADX, pady=PADY)

        # address line 1
        self.address1 = CTkEntry(self, placeholder_text="Address line 1", width=WIDTH)
        self.address1.pack(padx=PADX, pady=PADY)

        # address line 2
        self.address2 = CTkEntry(self, placeholder_text="Address line 2", width=WIDTH)
        self.address2.pack(padx=PADX, pady=PADY)

        # participant number
        self.participant_number = CTkEntry(self, placeholder_text="Participant number", width=WIDTH)
        self.participant_number.pack(padx=PADX, pady=PADY)

        # plan manager
        self.plan_manager = CTkEntry(self, placeholder_text="Plan manager", width=WIDTH)
        self.plan_manager.pack(padx=PADX, pady=PADY)

        # plan manager email
        self.plan_manager_email = CTkEntry(self, placeholder_text="Plan manager email", width=WIDTH)
        self.plan_manager_email.pack(padx=PADX, pady=PADY)

        # submit button
        self.submit = CTkButton(self, text="Add Client", command=self.add_client, width=WIDTH)
        self.submit.pack(padx=PADX, pady=PADY)
    
    def add_client(self):
        ABOVE_SEVEN_CODE = "15_622_0128_1_3"
        BELOW_SEVEN_CODE = "15_005_0118_1_3"

        # define the values as variables
        name = self.name.get()
        dob = self.dob.get()
        parent = self.parent.get()
        email = self.email.get()
        address1 = self.address1.get()
        address2 = self.address2.get()
        participant_number = self.participant_number.get()
        plan_manager = self.plan_manager.get()
        plan_manager_email = self.plan_manager_email.get()

        # clear the form after submission
        self.name.delete(0, END)
        self.dob.delete(0, END)
        self.parent.delete(0, END)
        self.email.delete(0, END)
        self.address1.delete(0, END)
        self.address2.delete(0, END)
        self.participant_number.delete(0, END)
        self.plan_manager.delete(0, END)
        self.plan_manager_email.delete(0, END)

        # calculate the defined attributes
        date_dob = datetime.strptime(dob, "%d/%m/%Y").date()

        if (today.year - date_dob.year) > 7:
            item_number = ABOVE_SEVEN_CODE
        else:
            item_number = BELOW_SEVEN_CODE

        # hand off the information to the database
        client = [(name, dob, parent, email, address1, address2,
                   participant_number, plan_manager, plan_manager_email, item_number)]
        
        add_client(client)