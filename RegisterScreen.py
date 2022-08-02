from tkinter import *
import pyperclip
import uuid
from Encryption import hashInput

def importData(dataWindow, bd):
    global window
    window = dataWindow
    global db
    db = bd
    global cursor
    cursor = db.cursor()

def register():
    for widget in window.winfo_children():  # used to make sure that we delete widgets before making new screen
        widget.destroy()
    window.geometry("250x250")
    lblUsername = Label(window, text="Username").pack()
    txtUsername = Entry(window, width=20)
    txtUsername.pack()

    lblPassword = Label(window, text="Password").pack()
    txtPassword = Entry(window, width=20)
    txtPassword.pack()

    lblConfirmPassword = Label(window, text="Confirm Password").pack()
    txtConfirmPassword = Entry(window, width=20)
    txtConfirmPassword.pack()

    def hasUsername():
        return txtUsername.get() != ""

    def passwordsMatch():
        return txtPassword.get() == txtConfirmPassword.get()

    def passwordNotEmpty():
        return txtPassword.get() != "" and txtConfirmPassword.get() != ""

    def userNotInDB():
        cursor.execute('SELECT * FROM usernamesAndPasswords')
        data = cursor.fetchall()
        for users in data:
            if users[0] == txtUsername.get():
                return False
        return True
    recoveryKey = str(uuid.uuid4().hex)
    recoveryKey = hashInput(recoveryKey)

    def addToDatabase(username, password):
        insert_user = """INSERT INTO usernamesAndPasswords(username, password, count, recovery)
        VALUES(%s, %s, %s, %s)"""
        cursor.execute(insert_user, (hashInput(username), hashInput(password), 0, hashInput(recoveryKey)))
        db.commit()
        newDB = "CREATE TABLE IF NOT EXISTS " + hashInput(username) + "(id TEXT NOT NULL, website TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL);"
        cursor.execute(newDB)
        db.commit()

    import LoginScreen

    def finished():
        if passwordsMatch() and userNotInDB() and hasUsername():
            addToDatabase(txtUsername.get(), txtPassword.get())
            recoveryKeyScreen(recoveryKey)
        elif not hasUsername():
            lblNoUsername = Label(window, text="Please enter a Username").pack()
        elif not passwordNotEmpty():
            lblPasswordsNotEmpty = Label(window, text="One or more password fields are empty").pack()
        elif not passwordsMatch():
            lblNotMatch = Label(window, text="Passwords do not match").pack()
        elif not userNotInDB():
            lblUserExists = Label(window, text="Username already exists").pack()
    btnFinish = Button(window, text="Finished", command=finished).pack()
    btnCancel = Button(window, text="Cancel", command=LoginScreen.loginScreen).pack()

def recoveryKeyScreen(recoveryKey):
    for widget in window.winfo_children():  # used to make sure that we delete widgets before making new screen
        widget.destroy()
    window.geometry("650x150")
    import LoginScreen

    def copyRecoveryKey():
        pyperclip.copy(recoveryKey)

    lblUsername = Label(window, text=recoveryKey).pack()
    lblInstruction = Label(window, text="This is your recovery key").pack()
    lblInstruction2 = Label(window, text="Please save this for if you forget your password").pack()
    btnCopy = Button(window, text="Copy", command=copyRecoveryKey).pack()
    btnFinish = Button(window, text="Finished", command=LoginScreen.loginScreen).pack()
