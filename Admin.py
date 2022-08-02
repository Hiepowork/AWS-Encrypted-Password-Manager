import pymysql
from tkinter import *
hostt = ""
userr = ""
passwordd = ""
db = pymysql.connect(host=hostt,user=userr,password=passwordd)
cursor = db.cursor()

def deleteDatabase():
    cmd = """drop database tester"""
    cursor.execute(cmd)
    print("Successfully deleted Database")

def createDatabase():
    cmd = """
    create database if not exists tester
    """
    cursor.execute(cmd)
    cmd = "use tester"
    cursor.execute(cmd)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usernamesAndPasswords(
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    count TEXT NOT NULL,
    recovery TEXT NOT NULL);
    """)
    print("Successfully created Database")

def viewAllTables():
    cmd = "use tester"
    cursor.execute(cmd)
    cmd = "show tables"
    cursor.execute(cmd)
    data = cursor.fetchall()
    if len(data) > 0:
        print(data)
    else:
        print("No Tables to View")

def viewTable(table):
    cmd = "use tester"
    cursor.execute(cmd)
    cmd = "SELECT * FROM " + table
    cursor.execute(cmd)
    data = cursor.fetchall()
    if len(data) > 0:
        print(data)
    else:
        print("No Tables to View")

def deleteUser(name):
    cmd = "user tester"
    cursor.execute(cmd)
    cmd = "DROP TABLE " + name
    cursor.execute(cmd)

def reset():
    deleteDatabase()
    createDatabase()
    print("Successfully reset Database")

def runAdmin():
    window = Tk()
    window.geometry("500x500")
    viewTables = Button(window, text="ViewAllTables", command=lambda:viewAllTables())
    viewTables.pack()
    tableName = Entry(window, width = 100)
    tableName.pack()
    tableNameView = Button(window, text="ViewSpecificTable", command = lambda:viewTable(tableName.get()))
    tableNameView.pack()

    deleteDB = Button(window, text="Delete DB", command=lambda:deleteDatabase())
    deleteDB.pack()
    createDB = Button(window, text="Create DB", command=lambda:createDatabase())
    createDB.pack()
    resetDB = Button(window, text = "Reset DB", command = lambda:reset())
    resetDB.pack()

    window.mainloop()

runAdmin()




