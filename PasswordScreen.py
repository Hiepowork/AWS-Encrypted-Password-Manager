import base64
from tkinter import *
from tkinter import ttk
from functools import partial
import random
import pyperclip
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from Encryption import encrypt, decrypt

def importData(dataWindow, bd):
    global window
    window = dataWindow
    global db
    db = bd
    global cursor
    cursor = db.cursor()

def addEntry(username):
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("850x425")
    lblWebsite = Label(window, text="Website").pack()
    txtWebsite = Entry(window, width=20)
    txtWebsite.pack()

    lblUsername = Label(window, text="Username").pack()
    txtUsername = Entry(window, width=20)
    txtUsername.pack()

    lblPassword = Label(window, text="Password").pack()
    txtPassword = Entry(window, width=20)
    txtPassword.pack()

    def insert():
        cursor.execute('SELECT * FROM usernamesAndPasswords where username =%s', (username,))
        userData = cursor.fetchall()
        db.commit()
        insertData = "INSERT INTO " + username + "(id, website, username, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insertData, (int(userData[0][2]),  encrypt(txtWebsite.get().encode('utf-8'), encryptionKey), encrypt(txtUsername.get().encode('utf-8'), encryptionKey), encrypt(txtPassword.get().encode('utf-8'), encryptionKey)))
        db.commit()
        updateCount = "UPDATE usernamesAndPasswords SET count = %s WHERE username = %s"
        countUpdate = int(userData[0][2]) + 1
        cursor.execute(updateCount, (countUpdate, username))
        db.commit()
        passwordScreen(username)

    btnCancel = Button(window, text="Cancel", command=lambda: passwordScreen(username)).pack()
    btnFinish = Button(window, text="Finished", command=insert).pack()

    def randomize(numChars):
        try:
            x = [
                ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z"],
                ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z"],
                ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]]
            z = []
            if az.get():
                z += x[0]
            if AZ.get():
                z += x[1]
            if num.get():
                z += x[2]
            if special.get():
                z += x[3]
            returner = ""
            if len(z) > 0:
                for i in range(0, int(numChars)):
                    number = random.randint(0, len(z) - 1)
                    returner += z[number]
                txtPassword.delete(0, END)
                txtPassword.insert(0, returner)
                txtPassword.pack()
        except:
            pass

    lblNumChars = Label(window, text = "Number of Characters").pack()
    txtNumChars = Entry(window, width=20)
    txtNumChars.pack()
    az = BooleanVar()
    o1 = Checkbutton(window, text="a-z", variable=az, onvalue=True, offvalue=False)
    o1.pack()

    AZ = BooleanVar()
    o2 = Checkbutton(window, text="A-Z", variable=AZ, onvalue=True, offvalue=False)
    o2.pack()

    num = BooleanVar()
    o3 = Checkbutton(window, text="0-9", variable=num, onvalue=True, offvalue=False)
    o3.pack()

    special = BooleanVar()
    o4 = Checkbutton(window, text="!@#$%%^&*()", variable=special, onvalue=True, offvalue=False)
    o4.pack()
    btnRandomize = Button(window, text="Randomize Password", command=lambda: randomize(txtNumChars.get()))
    btnRandomize.pack()


def editEntry(username, count, rowNum, data):
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("850x455")
    lblWebsite = Label(window, text="Website").pack()
    txtWebsite = Entry(window, width=20)
    txtWebsite.insert(0, decrypt(data[rowNum][1].encode('utf-8'), encryptionKey))
    txtWebsite.pack()

    lblUsername = Label(window, text="Username").pack()
    txtUsername = Entry(window, width=20)
    txtUsername.insert(0, decrypt(data[rowNum][2].encode('utf-8'), encryptionKey))
    txtUsername.pack()

    lblPassword = Label(window, text="Password").pack()
    txtPassword = Entry(window, width=20)
    txtPassword.insert(0, decrypt(data[rowNum][3].encode('utf-8'), encryptionKey))
    txtPassword.pack()

    def changeEntry():
        update1 = "UPDATE " + username + " SET website = %s WHERE id = %s"
        update2 = "UPDATE " + username + " SET username = %s WHERE id = %s"
        update3 = "UPDATE " + username + " SET password = %s WHERE id = %s"
        cursor.execute(update1, (encrypt(txtWebsite.get().encode('utf-8'), encryptionKey), count))
        cursor.execute(update2, (encrypt(txtUsername.get().encode('utf-8'), encryptionKey), count))
        cursor.execute(update3, (encrypt(txtPassword.get().encode('utf-8'), encryptionKey), count))
        db.commit()
        passwordScreen(username)

    def delete():
        remove = "DELETE FROM " + username + " WHERE id = %s"
        cursor.execute(remove, (str(count),))
        db.commit()
        passwordScreen(username)

    btnCancel = Button(window, text="Cancel", command=lambda: passwordScreen(username)).pack()
    btnConfirm = Button(window, text="Confirm", command=changeEntry).pack()
    btnDelete = Button(window, text="Delete", command=delete).pack()

    def randomize(numChars):
        x = [["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z"],
             ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"],
             ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
             ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]]
        z = []
        if az.get():
            z += x[0]
        if AZ.get():
            z += x[1]
        if num.get():
            z += x[2]
        if special.get():
            z += x[3]
        returner = ""
        if int(numChars) > 512:
            numChars = 512
        for i in range(0, int(numChars)):
            number = random.randint(0, len(z) - 1)
            returner += z[number]
        txtPassword.delete(0, END)
        txtPassword.insert(0, returner)
        txtPassword.pack()

    lblNumChars = Label(window, text="Number of Characters").pack()
    txtNumChars = Entry(window, width=20)
    txtNumChars.pack()
    az = BooleanVar()
    o1 = Checkbutton(window, text="a-z", variable=az, onvalue=True, offvalue=False).pack()

    AZ = BooleanVar()
    o2 = Checkbutton(window, text="A-Z", variable=AZ, onvalue=True, offvalue=False).pack()

    num = BooleanVar()
    o3 = Checkbutton(window, text="0-9", variable=num, onvalue=True, offvalue=False).pack()

    special = BooleanVar()
    o4 = Checkbutton(window, text="!@#$%%^&*()", variable=special, onvalue=True, offvalue=False).pack()
    btnRandomize = Button(window, text="Randomize Password", command=lambda: randomize(txtNumChars.get()))
    btnRandomize.pack()

def passwordScreen(username):
    for widget in window.winfo_children():  # used to make sure that we delete widgets before making new screen
        widget.destroy()
    window.geometry("850x400")
    window.eval('tk::PlaceWindow . center')
    salt = username.encode('utf-8')
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    global encryptionKey
    encryptionKey = base64.urlsafe_b64encode(kdf.derive(username.encode()))
    scrollFrame = Frame(window)
    scrollFrame.pack(fill=BOTH, expand=1)

    scrollCanvas = Canvas(scrollFrame)
    scrollCanvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollBar = ttk.Scrollbar(scrollFrame, orient=VERTICAL, command=scrollCanvas.yview)
    scrollBar.pack(side=RIGHT, fill=Y)

    scrollCanvas.configure(yscrollcommand=scrollBar.set)
    scrollCanvas.bind('<Configure>', lambda e: scrollCanvas.configure(scrollregion=scrollCanvas.bbox("all")))

    secondScrollFrame = Frame(scrollCanvas)

    scrollCanvas.create_window((0,0), window=secondScrollFrame, anchor="nw")

    getInfo = 'SELECT * FROM ' + username
    cursor.execute(getInfo)
    data = cursor.fetchall()
    rows = len(data)

    lbl = Label(secondScrollFrame, text = "Website")
    lbl.grid(row = 2, column = 0, padx = 80)
    lbl = Label(secondScrollFrame, text="Username")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(secondScrollFrame, text="Password")
    lbl.grid(row=2, column=2, padx=80)
    import LoginScreen
    btnLogout = Button(secondScrollFrame, text = "Logout", command = lambda:LoginScreen.loginScreen())
    btnLogout.grid(row = 2, column = 3, padx = 30)

    def copyPassword(i):
        pyperclip.copy(decrypt(data[i][3].encode('utf-8'), encryptionKey).decode('utf-8'))

    if (cursor.fetchall != None):
        i = -1
        for info in data:
            i += 1
            editAction = partial(editEntry, username, int(info[0]), i, data)
            copyAction = partial(copyPassword,i)
            lbl1 = Label(secondScrollFrame, text = decrypt(info[1].encode('utf-8'), encryptionKey))
            lbl1.grid(column = 0, row = i + 3)
            lbl2 = Label(secondScrollFrame, text= decrypt(info[2].encode('utf-8'), encryptionKey))
            lbl2.grid(column=1, row=i + 3)
            label3 = decrypt(info[3].encode('utf-8'), encryptionKey)
            if len(label3) > 12:
                label3 = label3[0:8].decode('utf-8') + "..."
            lbl3 = Label(secondScrollFrame, text=label3)
            lbl3.grid(column=2, row=i + 3)
            btn = Button(secondScrollFrame, text = "Copy", command = copyAction)
            btn.grid(row = i + 3, column = 4, pady = 10)
            btn = Button(secondScrollFrame, text="Edit", command=editAction)
            btn.grid(row = i + 3, column=3, pady=10)
    btn = Button(secondScrollFrame, text="Add Entry", command=lambda:addEntry(username))
    btn.grid(row=rows + 3, column=0, pady=10)
