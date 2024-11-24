from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
import database
import os

def generate_invoice():
    current_date = datetime.strftime(datetime.now().date(), '%d/%m/%Y')
    title_date = datetime.now().date()

    # creating the folder
    download_folder = str(os.path.join(Path.home(), "Downloads"))
    download_path = str(os.path.join(download_folder, f"Tax Invoices {title_date}"))
    print(download_path)

    try:
        # TODO have these display a pop up
        os.mkdir(download_path)
        print(f"Directory created successfully at {download_path}")
    except OSError as error:
        print(f"Directory already exists at {download_path}")

    # initialising the document
    document_path = Path(__file__).parent / "Invoice Template.docx"
    doc = DocxTemplate(document_path)

    # lets start by automating client data
    clients = database.retrieve_clients()

    # big-ass for loop coming right up
    for client in clients:
        # get external info
        sessions = database.retreive_sessions(client[0])
        
        database.create_invoice()
        invoice = database.retreive_invoice()

        # calculate sum of invoices
        session_sum = 0
        for s in sessions:
            session_sum += float(s[3])
        
        # id is 0, and we ain't including it
        context = {
            "NAME": client[1],
            "DOB": client[2],
            "PARENT": client[3],
            "EMAIL": client[4],
            "ADDRESS_LINE_1": client[5],
            "ADDRESS_LINE_2": client[6],
            "PARTICIPANT_NUMBER": client[7],
            "PLAN_MANAGER": client[8],
            "PLAN_MANAGER_EMAIL": client[9],
            "INVOICE": invoice[0],
            "TODAY": current_date,
            "TOTAL": '{0:.2f}'.format(session_sum),
            "sessions": sessions,
        }

        doc.render(context)
        output_path = str(os.path.join(download_path, f"Tax-Invoice-{client[1]}-{invoice[0]}.docx"))
        doc.save(output_path)
    
    print(f"Invoices generated at {download_path}")