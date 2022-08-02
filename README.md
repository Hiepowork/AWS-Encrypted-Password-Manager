# AWS-Encrypted-Password-Manager
This project utilizes Amazon Web Services databases, SQL and Python to store user passwords encrypted with SHA-256 hashing. To use with source code, all that needs to be done is to create an AWS account and a new Relational Database Service through AWS.

There will be 2 files that need to be edited, one called Admin.py, and the other being Main.py. At the top of the files, there needs to be a host name, user, and password that are put into the quotation marks for everything to work. Other than that everything else should work fine.

To run the program, there are 2 applications that can be used. Firstly, admin.py is the administrative portion of the database. As this is only a project not meant to  be used by real consumers, admin gives the administrator access to the entire database without needing to enter a password or anything. However, everything in the program is still encrypted as well. Secondly, Main.py is the main file that the entire program runs on and is used to launch the actual applicaiton.

When starting for the first time, the program first creates a database, and a table called usernamesAndPasswords within the database that stores all usernames and password login information. There are 4 columns called recovery, username, password, and count. Everything is encrypted with SHA-256 aside from count, as it poses no security risk. Everything else is encrypted on the User side, so that once it is in the database, even the administrator cannot decrypt it. This is known as Zero-Knowledge technology in which the information is first encrypted by the User, and then stored into the database.

From there, when a user logs in and adds various login information to the program, it is encrypted with Fernet, a library in python. This is done, so that the passwords can be decrypted. The key that is used for Fernet, is based on the username of the user, meaning everyone has a unique Fernet Key that they are able to use. 

AWS is the service used to store the database information so that it can be accessed from any computer runnning the application.
The database technologyu used in this applicaiton are SQL in order to store the various user data and their passwords. 
The encryption and hashing technologies used in this program are the hashlib library used for sha256 encryption, as well as the cryptography library that is used for its Fernet encryption and decryption.
The general user interface of this program are run with TKinter, a common GUI library in python.
