import mysql.connector

#connects to mysql local server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)
#Cursor to connect to mysql database
mycursor = mydb.cursor()


#Functions from project source code. Modified to not include parts from tkinter/the GUI.
def signIn(username,password):
   #username = usernameEntry.get()
   #password = passwordEntry.get()
   mycursor.execute("USE projectTest")
   #Checks database if there is an admin with this username and password
   sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
   mycursor.execute(sql, (username,password))
   myresult = mycursor.fetchall()

   #If login info is false, show error and return to login screen
   if not mycursor.rowcount:
       #messagebox.showerror("Error","Username or password is incorrect.")
       #loginMenu()
       return bool(False)
   #If login info is correct, proceed to main menu
   else:
       #mainMenu()
       return bool(True)
   return


def viewInfo(patientName,patientDOB):
       #patientName = testEntry.get()

       #Checks database if this patient is in the system
       sql = "SELECT * FROM patient WHERE name = %s AND dob = %s"
       mycursor.execute(sql, (patientName,patientDOB))
       myresult = mycursor.fetchall()

       #If login info is false, show error and return to login screen
       if not mycursor.rowcount:
           return bool(False)
           #messagebox.showerror("Error","Username or password is incorrect.")
       #If login info is correct, proceed to main menu
       else:
           return bool(True)
           #for x in myresult:
           #  patientLabel = Label(menuFrame, text="ID: " + x[0] + ", Name: " + x[1] + ", Age: " + x[2] + ", Gender: " + x[3] + ", Address: " + x[4],font=('Helvetica',10))
           #  patientLabel.grid(row=5, column=0, pady=10)  
       return
