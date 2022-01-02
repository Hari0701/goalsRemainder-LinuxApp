# Import the required library
import sqlite3 as sql
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkcalendar import *

import paths
import speak

# Create an instance of tkinter window
root = Tk()
root.title("Goals")
icon = PhotoImage(file=paths.icon)
root.iconphoto(False, icon)
# Define the geometry of the window
root.geometry("1200x750")

my_notebook = ttk.Notebook(root)
my_notebook.pack()

# sqlite3 Connection
conn = sql.connect(paths.database, timeout=10)
# create cursor
c = conn.cursor()


# function to perform add new goal
def save():
    day = int(str(target_date.get())[:2])
    month = int(str(target_date.get())[3:5])
    year = int(str(target_date.get())[6:10])
    hour = int(target_time.get()[:2])
    minute = int(target_time.get()[7:9])

    # create table
    c.execute(""" CREATE TABLE IF NOT EXISTS Goals(
                title text,
                day integer,
                month integer,
                year integer,
                hour integer,
                minute integer,
                description text); """)

    # Insert into table
    c.execute("INSERT INTO Goals VALUES(:title, :day, :month, :year,:hour, :minute, :description)", {
        'title': title.get(),
        'day': day,
        'month': month,
        'year': year,
        'hour': hour,
        'minute': minute,
        'description': description.get(1.0, "end-1c")
    })
    title.delete(0, END)
    description.delete("1.0", "end")
    # commit changes
    conn.commit()

    # close connection
    conn.close()


tab1 = Frame(my_notebook, width=1200, height=800, bg="#013DC4", borderwidth=0)
tab2 = Frame(my_notebook, width=1200, height=800, bg="#013DC4", borderwidth=0)
tab1.pack(fill='both', expand=1)
tab2.pack(fill='both', expand=1)

my_notebook.add(tab1, text="Your List")
my_notebook.add(tab2, text="Create New")

# tab 2
label1 = Label(tab2, text="Title:",
               font=("Helvetica", 18, 'bold'), fg="#E2D3F4", bg="#013DC4")
title = Entry(tab2, background="white", borderwidth=0, font=("Helvetica", 14))
label1.grid(pady=20, padx=30, ipadx=10, row=0, column=0)
title.grid(ipadx=300, ipady=15, pady=(20, 0), padx=(0, 100), row=0, column=1)

label2 = Label(tab2, text="Date:",
               font=("Helvetica", 18, 'bold'), fg="#E2D3F4", bg="#013DC4")
target_date = DateEntry(tab2, year=datetime.today().year, month=datetime.today().month,
                        day=datetime.today().day,
                        date_pattern='dd/mm/y')
label2.grid(pady=(20, 2), ipadx=10, row=1, column=0)
target_date.grid(pady=30, row=1, column=1, ipadx=50, ipady=10)

label3 = Label(tab2, text="Time:",
               font=("Helvetica", 18, 'bold'), fg="#E2D3F4", bg="#013DC4")
target_time = Entry(tab2, background="white", borderwidth=0, font=("Helvetica", 12))
target_time.insert(0, '00Hr : 00Min')
label3.grid(pady=20, padx=30, ipadx=10, row=2, column=0)
target_time.grid(ipadx=0, ipady=10, pady=(20, 20), row=2, column=1)

label4 = Label(tab2, text="Description:",
               font=("Helvetica", 18, 'bold'), fg="#E2D3F4", bg="#013DC4")
description = Text(tab2, background="white", borderwidth=0, font=("Helvetica", 14), height=5, width=20)
label4.grid(pady=(20, 2), padx=30, ipadx=10, row=3, column=0)
description.grid(ipadx=300, ipady=100, row=3, column=1, padx=(0, 100))

# Button to save data to database
submit_btn = Button(tab2, height=2,
                    width=8,
                    text="Save", font=("Helvetica", 14, 'bold'), fg="#ffffff", bg="#000000", border="0",
                    command=save)
submit_btn.grid(pady=(20, 80), row=4, column=1)

# tab 1
try:
    c.execute("SELECT * FROM Goals")
    records = c.fetchall()

    def tkinter_data():
        count = 0
        for i in range(0, len(records)):
            date = datetime(year=records[i][3], month=records[i][2], day=records[i][1],
                            hour=records[i][4], minute=records[i][5])
            countdown = date - datetime.now()
            titles = Label(tab1, text=str(i + 1) + ". " + records[i][0] + ":",
                           font=("Helvetica", 18, 'bold'), fg="#E2D3F4", bg="#013DC4")
            counter = Label(tab1, text=str(countdown)[:-7] + " Minutes to go",
                            font=("Helvetica", 17, 'bold'), fg="#E2D3F4", bg="#013DC4")
            titles.grid(row=count, column=0, pady=20, ipadx=10, ipady=10)
            counter.grid(row=count, column=1, pady=20, ipadx=10, ipady=10)
            count += 1
            if records[i][6] != '':
                desc = Label(tab1, text=records[i][6],
                             font=("Helvetica", 17, 'bold'), fg="#E2D3F4", bg="#013DC4")
                desc.grid(row=count, column=1, pady=20, ipadx=10, ipady=10)
                count += 1

    def speak_data():
        for i in range(0, len(records)):
            date = datetime(year=records[i][3], month=records[i][2], day=records[i][1],
                            hour=records[i][4], minute=records[i][5])
            countdown = date - datetime.now()
            speak.content("You have " + str(countdown)[:-7] + "Minutes to go" + " for " + records[i][0], tkinter_data())
        speak.default()


    if __name__ == "__main__":
        tkinter_data()

except:
    print("No Records Found")

root.mainloop()
