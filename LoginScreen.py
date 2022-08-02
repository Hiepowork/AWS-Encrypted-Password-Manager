from tkinter import *
import pyperclip
import uuid
from Encryption import hashInput

def importData(dataWindow,bd):
    global window
    window = dataWindow
    global db
    db = bd
    global cursor
    cursor = db.cursor()

def loginScreen():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("250x220")
    window.eval('tk::PlaceWindow . center')
    lblUsername = Label(window, text="Username").pack()
    txtUsername = Entry(window, width=20)
    txtUsername.pack()

    lblPassword = Label(window, text="Password").pack()
    txtPassword = Entry(window, width=20)
    txtPassword.pack()

    btnLogin = Button(window, text="Login", command=(lambda:login(hashInput(txtUsername.get()), hashInput(txtPassword.get())))).pack()
    import RegisterScreen
    btnRegister = Button(window, text="Register", command=RegisterScreen.register).pack()
    btnForgotPassword = Button(window, text="Forgot Password", command=passwordResetScreen).pack()

def login(username, password):
    cursor.execute('SELECT * FROM usernamesAndPasswords')
    data = cursor.fetchall()

    def userExists():
        i = 0
        for users in data:
            if users[0] == username:
                return i
            i = i + 1
        return i
    k = userExists()
    if not k >= len(data) and data[k][1] == password:
        import PasswordScreen
        PasswordScreen.passwordScreen(username)
    else:
        lblUserExists = Label(window, text="Username or Password is incorrect")
        lblUserExists.pack()

def passwordResetScreen():
    for widget in window.winfo_children():  # used to make sure that we delete widgets before making new screen
        widget.destroy()

    def checkCredentials(username, key):
        cursor.execute('SELECT * FROM usernamesAndPasswords')
        data = cursor.fetchall()
        def userExists():
            i = 0
            for users in data:
                if users[0] == username:
                    return i
                i = i + 1
            return i
        k = userExists()
        if not k >= len(data) and data[k][3] == key:
            resetPassword(username)

    lblUsername = Label(window, text="Enter your username").pack()
    txtUsername = Entry(window, width=20)
    txtUsername.pack()

    lblKey = Label(window, text="Enter your recovery key").pack()
    txtKey = Entry(window, width=20)
    txtKey.pack()

    btnCancel = Button(window, text="Cancel", command=loginScreen).pack()
    btnFinish = Button(window, text="Finish", command=lambda:checkCredentials(hashInput(txtUsername.get()), hashInput(txtKey.get()))).pack()

def resetPassword(username):
    for widget in window.winfo_children():  # used to make sure that we delete widgets before making new screen
        widget.destroy()

    def changePassword(password):
        update = "UPDATE usernamesAndPasswords SET password = %s WHERE username = %s"
        cursor.execute(update, (hashInput(password), username))
        db.commit()
        recoveryKey = str(uuid.uuid4().hex)
        recoveryKey = hashInput(recoveryKey)
        update = "UPDATE usernamesAndPasswords SET recovery = %s WHERE username = %s"
        cursor.execute(update, (hashInput(recoveryKey), username))
        db.commit()
        newRecoveryKey(recoveryKey)

    def newRecoveryKey(recoveryKey):
        for widget in window.winfo_children():  # used to make sure that we delete widgets before making new screen
            widget.destroy()
        window.geometry("650x150")
        def copyRecoveryKey():
            pyperclip.copy(recoveryKey)
        lbl1 = Label(window, text = "Your password was successfully changed").pack()
        lbl2 = Label(window, text = recoveryKey).pack()
        lbl3 = Label(window, text = "This is your new recovery key, please save this for safe keeping").pack()
        btnCopy = Button(window, text="Copy", command=copyRecoveryKey).pack()
        btnFinish = Button(window, text="Finished", command=loginScreen).pack()

    lblPassword = Label(window, text="Enter your new password").pack()
    txtPassword = Entry(window, width=20)
    txtPassword.pack()
    btnCancel = Button(window, text="Cancel", command=loginScreen).pack()
    btnFinish = Button(window, text="Finish", command=lambda:changePassword(txtPassword.get())).pack()