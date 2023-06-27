from tkinter import *
from tkinter import messagebox as msg
import sqlite3
from utilityFunctions import dateFormater


def status_changed(status_item_id):
    db_conn = sqlite3.connect('todoList.db')
    update_command = "UPDATE list SET status=1 WHERE ID={}".format(status_item_id)
    confirm = msg.askyesno("Confirm", "is this Task Completed?")
    if confirm:
        try:
            db_conn.execute(update_command)
            db_conn.commit()
            print("Successfully Deleted")

        except Exception as e:
            print("Couldn't update status because:", e)

    db_conn.close()
    viewDB()
    pass


def viewDB():
    for w in displayFrame.grid_slaves():
        w.grid_forget()

    db_conn = sqlite3.connect('todoList.db')
    try:
        myList = db_conn.execute("SELECT * FROM list")
        a = 5
        b = 1
        for i in myList:
            if i[2] == 0:
                status = "Pending"
                myCheck = Checkbutton(displayFrame, text='Done?',
                                      command=lambda d=i[0]: status_changed(d),
                                      onvalue=1,
                                      offvalue=0)
                myCheck.grid(row=[a], column=4)
            else:
                status = "Completed"
                itemDelete = Button(displayFrame, text="Delete", justify='right', )
                itemDelete.config(command=lambda d=i[0]: deleteItem(d))
                itemDelete.grid(row=[a], column=4, sticky='e')
            #  line for ID
            idLabel = Label(displayFrame, width=10)
            idLabel.grid(row=[a], column=0)
            idLabel.config(text=str(b))

            # line for Description
            taskLabel = Label(displayFrame, wraplength=300)
            taskLabel.grid(row=[a], column=1)
            taskLabel.config(text=i[1])

            # line for status
            statusLabel = Label(displayFrame, width=10)
            statusLabel.grid(row=[a], column=2)
            statusLabel.config(text=status)

            # line for date
            mydate = dateFormater(i[3])
            dateLabel = Label(displayFrame)
            dateLabel.grid(row=[a], column=3)
            dateLabel.config(text=mydate)

            print(i[0], i[1])




            a += 1
            b += 1

    except Exception as e:
        print("Couldn't Retrieve Information because:", e)
    db_conn.close()


def addItem(event):
    listItem = item.get()
    if listItem == "":
        msg.showerror("Error", "You cane Have a Blank task")
    else:
        db_conn = sqlite3.connect('todoList.db')
        print("Database Created")

        # Create a new table. Modify this to only be done if table hasn't originally been created
        try:
            db_conn.execute("CREATE TABLE list("
                            "ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                            "Item TEXT NOT NULL, "
                            "Status BOOL NOT NULL DEFAULT '0', "
                            "timeAdded TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
            db_conn.commit()
            print("List Table Created")
        except Exception as e:
            print(e)

        # Insert Values inside the table called list items
        try:
            insert_command = "INSERT INTO list(Item) VALUES('{}');".format(listItem)
            db_conn.execute(insert_command)
            db_conn.commit()
            print("Item Successfully in Database")
        except Exception as e:
            print("this error was found: ", e)

        db_conn.close()
        print("\nDatabase Closed")

    viewDB()


def deleteItem(item_id):
    db_conn = sqlite3.connect('todoList.db')
    delete_command = "DELETE FROM list WHERE ID={}".format(item_id)
    confirm = msg.askyesno("Delete", "Click Yes to confirm")
    if confirm:
        try:
            db_conn.execute(delete_command)
            db_conn.commit()
            msg.showerror("Successfully Deleted")
            print("Successfully Deleted")

        except Exception as e:
            print("Couldn't Retrieve Information because:", e)
    else:
        pass
    db_conn.close()
    viewDB()


root = Tk()
root.geometry('700x500')

root.title("Akomolafe To-do List")
mylabel_text = "Todo List"

Label(root, text="Enter new Item").grid(row=0)

item = Entry(root,  width=40)
item.grid(row=1, column=0)

addButton = Button(root, text="Add")
addButton.grid(row=1, column=1)
addButton.bind("<Button-1>", addItem)

displayFrame = Frame(root)
displayFrame.grid(row=2, sticky='we')

viewDB()
root.mainloop()
