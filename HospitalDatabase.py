#Imports tkinter for GUI
from tkinter import *
from tkinter import messagebox
#Connects python with MySql
import mysql.connector
#Imports files from project
import createDatabases
import fillDatabases

#connects to mysql local server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)
#Cursor to connect to mysql database
mycursor = mydb.cursor()

#Initializes aspects for starting GUI window
root = Tk()
root.title('Hospital Database')
root.iconbitmap('logo.ico')
root.geometry("500x650+1050+500")

#Hospital logo
img = PhotoImage(file='logo.png')

#Class for login menu GUI
def loginMenu():
    root.title('Hospital Database - Login')
    root.geometry("500x650+1050+500")
    mycursor.execute("USE administrators")
    #Frame for login menu
    loginFrame = LabelFrame(root, padx=100, pady=100)#,borderwidth=0,highlightthickness=0)
    loginFrame.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky=N+E+S+W)

    #Add hospital logo to Login window
    logoLabel = Label(loginFrame, image=img)
    logoLabel.grid(row=0, column=0, columnspan=2)

    #Title label for Login Window
    titleLabel = Label(loginFrame, text="Hospital Database",font=('Helvetica',25))
    titleLabel.grid(row=1, column=0, columnspan=2, pady=10)

    #Username and password Labels and Entries
    loginLabel = Label(loginFrame, text="Login",font=('Helvetica',20))
    loginLabel.grid(row=2, column=0, columnspan=2, pady=(80,20))

    usernameLabel = Label(loginFrame, text="Username: ",font=('Helvetica',12))
    usernameLabel.grid(row=3, column=0, padx=20)

    usernameEntry = Entry(loginFrame, font=('Helvetica',12))
    usernameEntry.grid(row=3, column=1)

    passwordLabel = Label(loginFrame, text="Password: ",font=('Helvetica',12))
    passwordLabel.grid(row=4, column=0, padx=20, pady=5)

    passwordEntry = Entry(loginFrame, font=('Helvetica',12))
    passwordEntry.grid(row=4, column=1)


    #Checks to see if login information is correct from the administrator database
    def signIn():
       username = usernameEntry.get()
       password = passwordEntry.get()

       #Checks database if there is an admin with this username and password
       sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
       mycursor.execute(sql, (username,password))
       myresult = mycursor.fetchall()

       #If login info is false, show error and return to login screen
       if not mycursor.rowcount:
           messagebox.showerror("Error","Username or password is incorrect.")
           loginMenu()
       #If login info is correct, proceed to main menu
       else:
           mainMenu()
       return

    #Sign In button
    loginButton = Button(loginFrame, text="Sign In", font=('Helvetica',12), command=signIn)
    loginButton.grid(row=5, column=0, columnspan=2, pady=20)

    #TEMP skip to main menu
    #mainMenu()


#Class for main menu GUI
def mainMenu():

   root.title('Hospital Database - Main Menu')
   root.geometry("580x650+0+0")
   menuFrame = LabelFrame(root, padx=60, pady=25)
   menuFrame.grid(row = 0, column = 0, rowspan = 4, columnspan = 2, sticky=N+E+S+W)
   mycursor.execute("USE hospital")

   testLabel = Label(menuFrame, text="Main Menu",font=('Helvetica',25))
   testLabel.grid(row=0, column=0, columnspan=2)

   def register():
       registerPatient()
    



   def logOut():
       response = messagebox.askquestion("Log Out","Are you sure that you want to log out?")
       if response == "yes":
           loginMenu()


   #All buttons for main menu
   registerButton = Button(menuFrame, text="Register New Patient", width=20,height=3, font=('Helvetica',12), command=register)
   registerButton.grid(row=1, column=0, padx=(0,80),pady=(100,0))

   viewButton = Button(menuFrame, text="View/Edit Patient Info", width=20,height=3, font=('Helvetica',12))#, command=clear_frame2)
   viewButton.grid(row=1, column=1, padx=(0,0), pady=(100,0))

   admitButton = Button(menuFrame, text="Admit a Patient", width=20,height=3, font=('Helvetica',12))#, command=clear_frame2)
   admitButton.grid(row=2, column=0, padx=(0,80),pady=(100,0))

   dischargeButton = Button(menuFrame, text="Discharge a Patient", width=20,height=3, font=('Helvetica',12))#, command=clear_frame2)
   dischargeButton.grid(row=2, column=1, padx=(0,0), pady=(100,0))

   recordsButton = Button(menuFrame, text="View Records/Billing", width=20,height=3, font=('Helvetica',12))#, command=clear_frame2)
   recordsButton.grid(row=3, column=0, padx=(0,80),pady=(100,0))

   logoutButton = Button(menuFrame, text="Log Out", width=20,height=3, font=('Helvetica',12), command=logOut)
   logoutButton.grid(row=3, column=1, padx=(0,0), pady=(100,0))


   #registerPatient()


   
   #testEntry = Entry(menuFrame, font=('Helvetica',12))
   #testEntry.grid(row=2, column=0, columnspan=2,pady=20)

   #def viewInfo():
    #   patientName = testEntry.get()
#
 #      #Checks database if this patient is in the system
  #     sql = "SELECT * FROM patient WHERE name = %s"
   #   myresult = mycursor.fetchall()

       #If login info is false, show error and return to login screen
    #   if not mycursor.rowcount:
     #      messagebox.showerror("Error","Username or password is incorrect.")
      # #If login info is correct, proceed to main menu
       #else:
        #   print("Yes")
         #  for x in myresult:
          #   patientLabel = Label(menuFrame, text="ID: " + x[0] + ", Name: " + x[1] + ", Age: " + x[2] + ", Gender: " + x[3] + ", Address: " + x[4],font=('Helvetica',10))
           #  patientLabel.grid(row=5, column=0, pady=10)  
       #return

   #viewButton = Button(menuFrame, text="Search", font=('Helvetica',12))#, command=viewInfo)
   #viewButton.grid(row=4, column=0, columnspan=2,pady=20)

#First runs Login Menu to start the GUI
#loginMenu()


def registerPatient():

    root.title('Hospital Database - Register New Patient')
    root.geometry("580x650+0+0")
    registerFrame = LabelFrame(root, padx=60, pady=50)
    registerFrame.grid(row = 0, column = 0, rowspan = 12, columnspan = 2, sticky=N+E+S+W)
    mycursor.execute("USE hospital")

    #Text Labels:
    nameLabel = Label(registerFrame, text="Name",font=('Helvetica',20))
    nameLabel.grid(row=1, column=0, padx=(0,160),pady=5, sticky=W)

    dobLabel = Label(registerFrame, text="Date of Birth",font=('Helvetica',20))
    dobLabel.grid(row=2, column=0, pady=5, sticky=W)

    genderLabel = Label(registerFrame, text="Gender",font=('Helvetica',20))
    genderLabel.grid(row=3, column=0, pady=5, sticky=W)

    addressLabel = Label(registerFrame, text="Address",font=('Helvetica',20))
    addressLabel.grid(row=4, column=0, pady=5, sticky=W)

    diseaseLabel = Label(registerFrame, text="Disease/Reason",font=('Helvetica',20))
    diseaseLabel.grid(row=5, column=0, pady=5, sticky=W)

    insuranceLabel = Label(registerFrame, text="Insurance Name",font=('Helvetica',20))
    insuranceLabel.grid(row=6, column=0, pady=5, sticky=W)

    insuranceIDLabel = Label(registerFrame, text="Insurance ID",font=('Helvetica',20))
    insuranceIDLabel.grid(row=7, column=0, pady=5, sticky=W)

    #Text Boxes
    name = Entry(registerFrame, font=('Helvetica',16))
    name.grid(row=1, column=1, pady=5, sticky=E)

    dob = Entry(registerFrame, font=('Helvetica',16))
    dob.grid(row=2, column=1, pady=5, sticky=E)

    gender = Entry(registerFrame, font=('Helvetica',16))
    gender.grid(row=3, column=1, pady=5, sticky=E)

    address = Entry(registerFrame, font=('Helvetica',16))
    address.grid(row=4, column=1, pady=5, sticky=E)

    disease = Entry(registerFrame, font=('Helvetica',16))
    disease.grid(row=5, column=1, pady=5, sticky=E)

    insurance = Entry(registerFrame, font=('Helvetica',16))
    insurance.grid(row=6, column=1, pady=5, sticky=E)

    insuranceID = Entry(registerFrame, font=('Helvetica',16))
    insuranceID.grid(row=7, column=1, pady=5, sticky=E)

    submitButton = Button(registerFrame, text="Submit", width=30,height=2, font=('Helvetica',18))
    submitButton.grid(row=8, column=0, columnspan = 2, pady=(50,0))
    #Submit Button

"""

    # Create Text Boxes
    f_name = Entry(root, width=30)
    f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name = Entry(root, width=30)
    l_name.grid(row=1, column=1)
    address = Entry(root, width=30)
    address.grid(row=2, column=1)
    city = Entry(root, width=30)
    city.grid(row=3, column=1)
    state = Entry(root, width=30)
    state.grid(row=4, column=1)
    zipcode = Entry(root, width=30)
    zipcode.grid(row=5, column=1)
"""





#TEMP remove all databases
mycursor.execute("DROP DATABASE administrators")
mycursor.execute("DROP DATABASE hospital")

sql = "SHOW DATABASES LIKE 'administrators'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(mycursor.rowcount)


#Checks if database exists
#If it does not exist it runs a file to create the database and classes
if not mycursor.rowcount:
    print("Database doesn't exist")
    createDatabases.create()
    #Fills databases with test data
    fillDatabases.fill()

    #reconnects to server to get newly created databases and info
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password"
    )
    mycursor = mydb.cursor()

    
#Else, the database exists
else:
    print("Database exists")


loginMenu()
#Ends GUI
root.mainloop()




