import LoginScreen
import RegisterScreen
import PasswordScreen
from tkinter import *
import pymysql

hostt = ""
userr = ""
passwordd = ""
db = pymysql.connect(host=hostt,user=userr,password=passwordd)
cursor = db.cursor()

window = Tk()
window.resizable(False,False)
cmd = """ 
    use tester
    """
cursor.execute(cmd)

reg = RegisterScreen
reg.importData(window, db)
pas = PasswordScreen
pas.importData(window, db)
log = LoginScreen
log.importData(window, db)

log.loginScreen()
window.mainloop()



