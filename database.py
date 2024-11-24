import sqlite3
from datetime import datetime

# database utilities
def close_database(connection):
    connection.commit()
    connection.close()

# client utilities
def add_client(client):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS client
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name,
                dob,
                parent,
                email,
                address1,
                address2,
                participant_number,
                plan_manager,
                plan_manager_email,
                item_number);""")
    
    # there must be a better way than executemany()
    # but the non list variations haven't worked so far
    # need to look into it a bit more
    cursor.executemany("""INSERT INTO client(
                       name,
                       dob,
                       parent,
                       email,
                       address1,
                       address2,
                       participant_number,
                       plan_manager,
                       plan_manager_email,
                       item_number)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", client)
    
    close_database(connection)

def retrieve_clients():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS client
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name,
                dob,
                parent,
                email,
                address1,
                address2,
                participant_number,
                plan_manager,
                plan_manager_email,
                item_number);""")

    cursor.execute("""SELECT * FROM client""")
    data = cursor.fetchall()

    close_database(connection)
    return data

# TODO add a function that retrieves a client as an object from an id
# not actually sure if I have to implement this anymore

def retrieve_client_session_info():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS client
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name,
                dob,
                parent,
                email,
                address1,
                address2,
                participant_number,
                plan_manager,
                plan_manager_email,
                item_number);""")

    cursor.execute("""SELECT id, name, item_number FROM client""")
    data = cursor.fetchall()

    # turn the client tuples into dictionaries with attributes
    client_list = []
    for i in range(len(data)):
        client = {
            "id": data[i][0],
            "name": data[i][1],
            "item_number": data[i][2],
        }

        client_list.append(client)

    return client_list

def add_session(session):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS session
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    date, 
                    description, 
                    item_number, 
                    unit_price, 
                    client_id,
                    FOREIGN KEY(client_id) REFERENCES client(client_id));""")
    
    cursor.executemany("""INSERT INTO session(
                       date,
                       description,
                       item_number,
                       unit_price,
                       client_id)
                       VALUES (?, ?, ?, ?, ?)""", session)
    
    close_database(connection)

def retreive_sessions(client_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # define todays month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    cursor.execute("""CREATE TABLE IF NOT EXISTS session
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    date, 
                    description, 
                    item_number, 
                    unit_price, 
                    client_id,
                    FOREIGN KEY(client_id) REFERENCES client(client_id));""")

    cursor.execute("""SELECT date, description, item_number, printf("%.2f", unit_price) AS unit_price
                   FROM session
                   WHERE client_id = ?
                   ORDER BY date""", (client_id,))
    
    # NOTE for future self
    # make sure the client id is in a tuple with a trailing comma
    # otherwise it doesn't count as a real comparison tsktsktsk...

    data = cursor.fetchall()
    close_database(connection)
    
    # filter for only the sessions in the current year and month
    filtered_sessions = []
    for sessions in data:
        # 
        session_date = datetime.strptime(sessions[0], "%d/%m/%Y")
        if (session_date.year == current_year and session_date.month == current_month):
            filtered_sessions.append(sessions)
    
    return filtered_sessions

def create_invoice():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS invoice
                   (invoice_number INTEGER PRIMARY KEY AUTOINCREMENT)""")
    
    cursor.execute("""INSERT INTO invoice DEFAULT VALUES""")

    close_database(connection)

def retreive_invoice():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS invoice
                   (invoice_number INTEGER PRIMARY KEY AUTOINCREMENT)""")

    cursor.execute("""SELECT invoice_number 
                   FROM invoice
                   ORDER BY invoice_number DESC""")
    
    data = cursor.fetchone()
    close_database(connection)

    return data