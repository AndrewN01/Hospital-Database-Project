#Imports tkinter for GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#Connects python with MySql
import mysql.connector
#Import datetime
from datetime import date 
#Imports files from project
import createDatabases
import fillDatabases


#Server information for connection
setHost = "localhost"
setUser="root"
setPasswd="password"

#connects to mysql local server
mydb = mysql.connector.connect(
  host=setHost,
  user=setUser,
  passwd=setPasswd
)
#Cursor to connect to mysql database
mycursor = mydb.cursor()

#Set position for all GUI frames
position = "+100+100"

#Initializes aspects for starting GUI window
root = Tk()
root.title('Hospital Database')
root.iconbitmap('logo.ico')
root.geometry("500x650" + position)

#Hospital logo
img = PhotoImage(file='logo.png')

#GLOBAL FUNCTIONS used in multiple menus
#Function to check if patient exists in the patient table of the hospital database
def checkForPatient(username,dob):
    mydb = mysql.connector.connect(
        host=setHost,
        user=setUser,
        passwd=setPasswd
    )
    mycursor = mydb.cursor()
    mycursor.execute("USE hospital")
    #print(username + dob)
    sql = "SELECT * FROM patient WHERE name = %s AND dob = %s"
    mycursor.execute(sql, (username,dob))
    myresult = mycursor.fetchall()
    #Patient is not in database
    if not mycursor.rowcount:
        return bool(False)
    #Patient is in database
    else:
        return bool(True)
    return

#Checks if both fields in search are not empty and if selected patient exists in the database.
def checkExists(name,dob):
    mydb = mysql.connector.connect(
        host=setHost,
        user=setUser,
        passwd=setPasswd
    ) 
    mycursor = mydb.cursor()    
    mycursor.execute("USE hospital")
    #Displays error if any field is empty
    if name == '' or dob == '':
        messagebox.showerror("Error","One or more fields are empty.")
    else:
        #Displays an error if patient does not exist in the database
        if not checkForPatient(name,dob):
            messagebox.showerror("Error","Patient does not exist in the database.")
        else:
            return bool(True)

#Gets and returns a patient's ID using their name and date of birth
def getPatientID(name,dob):
    mydb = mysql.connector.connect(
        host=setHost,
        user=setUser,
        passwd=setPasswd
    ) 
    mycursor = mydb.cursor()
    mycursor.execute("USE hospital")
    sql = "SELECT patient_id FROM patient WHERE name = %s AND dob = %s" 
    mycursor.execute(sql, (name,dob))
    myresult = mycursor.fetchall()
    for x in myresult:
        patientID = x[0]
    return patientID

#GUI FUNCTIONS to create the different frames and widgets in the GUI
#Function for login menu GUI
def loginMenu():
    root.title('Hospital Database - Login')
    root.geometry("500x650" + position)
    #reconnects to server
    mydb = mysql.connector.connect(
       host=setHost,
       user=setUser,
       passwd=setPasswd
    )
    mycursor = mydb.cursor()
    mycursor.execute("USE administrators")
    #Frame for login menu
    loginFrame = LabelFrame(root, padx=100, pady=100,borderwidth=0,highlightthickness=0)
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

    passwordEntry = Entry(loginFrame, font=('Helvetica',12), show="*")
    passwordEntry.grid(row=4, column=1)

    #Triggers sign in button if enter key is pressed
    def enterSignIn(event):
        signIn()
    
    #Checks to see if login information is correct from the administrator database
    def signIn():
       username = usernameEntry.get()
       password = passwordEntry.get()

       mydb = mysql.connector.connect(
           host=setHost,
           user=setUser,
           passwd=setPasswd
       )
       mycursor = mydb.cursor()
       mycursor.execute("USE administrators")
       
       #Checks database if there is an admin with this username and password. Decrypts password with key.
       #The user's unique password is the aes encryption/decryption key in this table where the actual password is set string: "password"
       sql = "SELECT admin_id, username, CAST(AES_DECRYPT(password,'" + password + "') AS CHAR(255)) FROM admin WHERE username = %s AND CAST(AES_DECRYPT(password,'" + password + "') AS CHAR(255)) = 'password'"
       mycursor.execute(sql, (username,))
       myresult = mycursor.fetchall()
       
       #If login info is false, display error
       if not mycursor.rowcount:
           messagebox.showerror("Error","Username or password is incorrect.")
           #Delete info from entry boxes
           usernameEntry.delete(0,"end")
           passwordEntry.delete(0,"end")
       #If login info is correct, proceed to main menu
       else:
           loginFrame.destroy()
           mainMenu()
       return

    #Sign In button to trigger sign in function
    loginButton = Button(loginFrame, text="Sign In", font=('Helvetica',12), command=signIn)
    loginButton.grid(row=5, column=0, columnspan=2, pady=20)

    #Binds entries to trigger the sign in function
    usernameEntry.bind('<Return>',enterSignIn)
    passwordEntry.bind('<Return>',enterSignIn)


#Function for main menu GUI
def mainMenu():

   #reconnects to server
   mydb = mysql.connector.connect(
       host=setHost,
       user=setUser,
       passwd=setPasswd
   )
   mycursor = mydb.cursor()

   root.title('Hospital Database - Main Menu')
   root.geometry("580x650" + position)
   menuFrame = LabelFrame(root, padx=60, pady=50,borderwidth=0,highlightthickness=0)
   menuFrame.grid(row = 0, column = 0, rowspan = 4, columnspan = 2, sticky=N+E+S+W)
   mycursor.execute("USE hospital")

   menuLabel = Label(menuFrame, text="Main Menu",font=('Helvetica',25))
   menuLabel.grid(row=0, column=0, columnspan=2)

   def register():
       menuFrame.destroy()
       registerPatient()
    
   def view():
       menuFrame.destroy()
       viewInfo()

   def admit():
       menuFrame.destroy()
       admitPatient()

   def discharge():
       menuFrame.destroy()
       dischargePatient()
       
   def records():
       menuFrame.destroy()
       viewRecords()

   def logOut():
       response = messagebox.askquestion("Log Out","Are you sure that you want to log out?")
       if response == "yes":
           menuFrame.destroy()
           loginMenu()


   #All buttons for main menu
   registerButton = Button(menuFrame, text="Register New Patient", width=20,height=3, font=('Helvetica',12), command=register)
   registerButton.grid(row=1, column=0, padx=(0,80),pady=(100,0))

   viewButton = Button(menuFrame, text="View/Edit Patient Info", width=20,height=3, font=('Helvetica',12), command=view)
   viewButton.grid(row=1, column=1, padx=(0,0), pady=(100,0))

   admitButton = Button(menuFrame, text="Admit a Patient", width=20,height=3, font=('Helvetica',12), command=admit)
   admitButton.grid(row=2, column=0, padx=(0,80),pady=(100,0))

   dischargeButton = Button(menuFrame, text="Discharge a Patient", width=20,height=3, font=('Helvetica',12), command=discharge)
   dischargeButton.grid(row=2, column=1, padx=(0,0), pady=(100,0))

   recordsButton = Button(menuFrame, text="View Records/Billing", width=20,height=3, font=('Helvetica',12), command=records)
   recordsButton.grid(row=3, column=0, padx=(0,80),pady=(100,0))

   logoutButton = Button(menuFrame, text="Log Out", width=20,height=3, font=('Helvetica',12), command=logOut)
   logoutButton.grid(row=3, column=1, padx=(0,0), pady=(100,0))

#Function for register menu GUI
def registerPatient():

    root.title('Hospital Database - Register New Patient')
    root.geometry("600x600" + position)
    registerFrame = LabelFrame(root, padx=60, pady=50,borderwidth=0,highlightthickness=0)
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

    #Entry Boxes
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

    def submit():
        #reconnects to server
        mydb = mysql.connector.connect(
        host=setHost,
        user=setUser,
        passwd=setPasswd
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE hospital")
        
        #Displays error if any field is empty
        if name.get() == '' or dob.get() == '' or gender.get() == '' or address.get() == '' or disease.get() == '' or insurance.get() == '' or insuranceID.get() == '':
            messagebox.showerror("Error","One or more fields are empty.")
        else:
            #Displays an error if user tries to add a patient that already exists
            if checkForPatient(name.get(),dob.get()):
                messagebox.showerror("Error","Patient already exists in the database.")
            
            else:
                #Finds next unused patientID number
                sql = "SELECT * FROM patient ORDER BY CAST(patient_id AS unsigned)"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                patientID = 1
                #Increments through the taken ID numbers until an unused one is found
                for x in myresult:
                    if str(patientID) == x[0]:
                        patientID +=1
                    else:
                        break
                #Adds new patient's information into patient table
                sql = "INSERT INTO patient (patient_id, name, dob, gender, address, disease, insurancename, insuranceID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = [(patientID,name.get(),dob.get(),gender.get(),address.get(),disease.get(),insurance.get(),insuranceID.get())]
                mycursor.executemany(sql,val)
                mydb.commit()
                messagebox.showinfo("Success","New patient has been added to the database.")
                registerFrame.destroy()
                mainMenu()

    def back():
        registerFrame.destroy()
        mainMenu()
        
    #Submit Button
    submitButton = Button(registerFrame, text="Submit", width=35,height=2, font=('Helvetica',18), command=submit)
    submitButton.grid(row=8, column=0, columnspan = 2, pady=(50,0))

    backButton = Button(registerFrame, text="Back", width=15,height=1, font=('Helvetica',18), command=back)
    backButton.grid(row=9, column=1, pady=(20,0), sticky=E)

#Function for view/edit menu GUI
def viewInfo():
    root.title('Hospital Database - View or Edit Patient Information')
    root.geometry("580x813" + position)
    mycursor.execute("USE hospital")


    #Search Frame contains name and dob entries to search for a patient
    searchFrame = LabelFrame(root, padx=42, pady=20, text="Search")
    searchFrame.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky=N+E+S+W, padx = 5)

    selectLabel = Label(searchFrame, text="Select Patient",font=('Helvetica',25))
    selectLabel.grid(row=0, column=0, pady = (0,15),columnspan=2)

    #Search Labels
    nameSearchLabel = Label(searchFrame, text="Name",font=('Helvetica',20))
    nameSearchLabel.grid(row=1, column=0, padx=(0,160),pady=5, sticky=W)

    dobSearchLabel = Label(searchFrame, text="Date of Birth",font=('Helvetica',20))
    dobSearchLabel.grid(row=2, column=0, pady=5, sticky=W)

    #Search Entries
    nameSearch = Entry(searchFrame, font=('Helvetica',16))
    nameSearch.grid(row=1, column=1, pady=5, sticky=E)

    dobSearch = Entry(searchFrame, font=('Helvetica',16))
    dobSearch.grid(row=2, column=1, pady=5, sticky=E)


    #Information Frame contains information of selected patient

    infoFrame = LabelFrame(root, padx=42, pady=20, text="Information")
    infoFrame.grid(row = 4, column = 0, rowspan = 12, columnspan = 2, sticky=N+E+S+W, padx = 5)

    #Information Labels
    nameLabel = Label(infoFrame, text="Name",font=('Helvetica',20))
    nameLabel.grid(row=4, column=0, padx=(0,160),pady=5, sticky=W)

    dobSearchLabel = Label(infoFrame, text="Date of Birth",font=('Helvetica',20))
    dobSearchLabel.grid(row=5, column=0, pady=5, sticky=W)

    genderLabel = Label(infoFrame, text="Gender",font=('Helvetica',20))
    genderLabel.grid(row=6, column=0, pady=5, sticky=W)

    addressLabel = Label(infoFrame, text="Address",font=('Helvetica',20))
    addressLabel.grid(row=7, column=0, pady=5, sticky=W)

    diseaseLabel = Label(infoFrame, text="Disease/Reason",font=('Helvetica',20))
    diseaseLabel.grid(row=8, column=0, pady=5, sticky=W)

    insuranceLabel = Label(infoFrame, text="Insurance Name",font=('Helvetica',20))
    insuranceLabel.grid(row=9, column=0, pady=5, sticky=W)

    insuranceIDLabel = Label(infoFrame, text="Insurance ID",font=('Helvetica',20))
    insuranceIDLabel.grid(row=10, column=0, pady=5, sticky=W)

    #Information Entries
    nameEntry = Entry(infoFrame, font=('Helvetica',16))
    nameEntry.grid(row=4, column=1, pady=5, sticky=E)

    dobEntry = Entry(infoFrame, font=('Helvetica',16))
    dobEntry.grid(row=5, column=1, pady=5, sticky=E)

    genderEntry = Entry(infoFrame, font=('Helvetica',16))
    genderEntry.grid(row=6, column=1, pady=5, sticky=E)

    addressEntry = Entry(infoFrame, font=('Helvetica',16))
    addressEntry.grid(row=7, column=1, pady=5, sticky=E)

    diseaseEntry = Entry(infoFrame, font=('Helvetica',16))
    diseaseEntry.grid(row=8, column=1, pady=5, sticky=E)

    insuranceEntry = Entry(infoFrame, font=('Helvetica',16))
    insuranceEntry.grid(row=9, column=1, pady=5, sticky=E)

    insuranceIDEntry = Entry(infoFrame, font=('Helvetica',16))
    insuranceIDEntry.grid(row=10, column=1, pady=5, sticky=E)


    #Function to get information of selected patient
    def search():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE hospital")
        if checkExists(nameSearch.get(), dobSearch.get()):
                sql = "SELECT * FROM patient WHERE name = %s AND dob = %s"
                mycursor.execute(sql, (nameSearch.get(),dobSearch.get()))
                myresult = mycursor.fetchall()
                #Replaces all entry boxes in information frame with details of selected patient
                for x in myresult:
                    nameEntry.delete(0,"end"),nameEntry.insert(0,x[1])
                    dobEntry.delete(0,"end"),dobEntry.insert(0,x[2])
                    genderEntry.delete(0,"end"),genderEntry.insert(0,x[3])
                    addressEntry.delete(0,"end"),addressEntry.insert(0,x[4])
                    diseaseEntry.delete(0,"end"),diseaseEntry.insert(0,x[5])
                    insuranceEntry.delete(0,"end"),insuranceEntry.insert(0,x[6])
                    insuranceIDEntry.delete(0,"end"),insuranceIDEntry.insert(0,x[7])

    #Function to update information of selected patient   
    def save():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE hospital")
        if checkExists(nameSearch.get(), dobSearch.get()):
            #Displays error if any field from information frame is empty
            if nameEntry.get() == '' or dobEntry.get() == '' or genderEntry.get() == '' or addressEntry.get() == '' or diseaseEntry.get() == '' or insuranceEntry.get() == '' or insuranceIDEntry.get() == '':
                messagebox.showerror("Error","One or more fields are empty.")
            else:
                #Gets id of selected patient
                patientID = getPatientID(nameSearch.get(),dobSearch.get())
                #Updates patient's information with information from information frame
                sql = "UPDATE patient SET name = %s, dob = %s, gender = %s, address = %s, disease = %s, insurancename = %s, insuranceID = %s WHERE patient_id = %s"
                val = [(nameEntry.get(),dobEntry.get(),genderEntry.get(),addressEntry.get(),diseaseEntry.get(),insuranceEntry.get(),insuranceIDEntry.get(),patientID)]
                mycursor.executemany(sql,val)
                mydb.commit()
                messagebox.showinfo("Success","The patient's information has been updated.")

    def delete():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE hospital")
        if checkExists(nameSearch.get(), dobSearch.get()):        
            response = messagebox.askquestion("Delete Patient","Are you sure that you want to delete this patient from the database?")
            if response == "yes":
                #Gets id of selected patient
                patientID = getPatientID(nameSearch.get(),dobSearch.get())

                #Checks if patient is currently in a room. If so, deletes information referencing patient from the room.
                sql = "SELECT room_number FROM room WHERE patient_id = %s"
                mycursor.execute(sql,(patientID,))
                myresult = mycursor.fetchall()
                for x in myresult:
                    roomNumber = x[0]
                #If patient had a room, remove date_admitted and doctor_id values from the room
                if mycursor.rowcount:
                    sql = "UPDATE room SET date_admitted = NULL,doctor_id = NULL WHERE room_number = %s"
                    mycursor.execute(sql,(roomNumber,))
                    mydb.commit()
                #Deletes patient from the database
                sql = "DELETE FROM patient WHERE patient_id = %s"
                mycursor.execute(sql,(patientID,))
                mydb.commit()
                #Delete info from entry boxes
                nameSearch.delete(0,"end")
                dobSearch.delete(0,"end")
                nameEntry.delete(0,"end")
                dobEntry.delete(0,"end")
                genderEntry.delete(0,"end")
                addressEntry.delete(0,"end")
                diseaseEntry.delete(0,"end")
                insuranceEntry.delete(0,"end")
                insuranceIDEntry.delete(0,"end")
                messagebox.showinfo("Success","The patient was successfully deleted from the database.")

    #Function opens a window that displays the information for all patients
    def viewall():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE hospital")

        #Creates new window to display information of all patients
        viewRoot = Tk()
        viewRoot.title('Hospital Database - All Patients')
        viewRoot.iconbitmap('logo.ico')
        viewRoot.geometry("950x320" + position)

        #Frame for new window
        viewallFrame = LabelFrame(viewRoot, padx=100, pady=20,borderwidth=0,highlightthickness=0)
        viewallFrame.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, sticky=N+E+S+W)


        #Columns displayed in table
        columns = ('patient_id','name','dob','gender','address','disease','insurancename','insuranceID')

        #Creates a treeview to display tabular data
        tree = ttk.Treeview(viewallFrame, columns=columns, show='headings', height=12)

        tree.column('patient_id',width = 70,anchor=W)
        tree.heading('patient_id', text='Patient ID',anchor=W)

        tree.column('name',width = 90,anchor=W)
        tree.heading('name', text='Name',anchor=W)

        tree.column('dob',width = 90,anchor=W)
        tree.heading('dob', text='Date of Birth',anchor=W)
        
        tree.column('gender',width = 70,anchor=W)
        tree.heading('gender', text='Gender',anchor=W)

        tree.column('address',width = 90,anchor=W)
        tree.heading('address', text='Address',anchor=W)

        tree.column('disease',width = 110,anchor=W)
        tree.heading('disease', text='Disease/Reason',anchor=W)

        tree.column('insurancename',width = 130,anchor=W)
        tree.heading('insurancename', text='Insurance Company',anchor=W)

        tree.column('insuranceID',width = 110,anchor=W)
        tree.heading('insuranceID', text='Insurance ID',anchor=W)

        tree.grid(row=0, column=0, columnspan = 2, sticky=N+E+S+W)

        #Adds a scrollbar 
        scrollbar = Scrollbar(viewallFrame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=N+S+E)

        #Gets all patients from database
        sql = "SELECT * FROM patient"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        #If no patients are found, display error.
        if not mycursor.rowcount:
            messagebox.showerror("Error","No patients were found in the database.")
        #Replace tablular data with information of all patients in database
        else:
            for x in myresult:
                tree.insert('', END, values=(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))        




        
        
    #Function to return to main menu            
    def back():
        searchFrame.destroy()
        infoFrame.destroy()
        mainMenu()

    #Search, Save, Delete, and Back buttons
    searchButton = Button(searchFrame, text="Search", width=15,height=1, font=('Helvetica',18), command=search)
    searchButton.grid(row=3, column=0, columnspan = 2, pady=(20,0))

    saveButton = Button(infoFrame, text="Save", width=15,height=1, font=('Helvetica',18), command=save)
    saveButton.grid(row=11, column=0, columnspan = 1, pady=(20,0))

    deleteButton = Button(infoFrame, text="Delete", width=15,height=1, font=('Helvetica',18), command=delete)
    deleteButton.grid(row=11, column=1, columnspan = 1, pady=(20,0))

    viewallButton = Button(infoFrame, text="View All", width=15,height=1, font=('Helvetica',18), command=viewall)
    viewallButton.grid(row=12, column=0, columnspan = 1, pady=(20,0))

    backButton = Button(infoFrame, text="Back", width=15,height=1, font=('Helvetica',18), command=back)
    backButton.grid(row=12, column=1, columnspan = 1, pady=(20,0))

#Function for admit menu GUI
def admitPatient():
    root.title('Hospital Database - Admit a Patient')
    root.geometry("580x360" + position)
    mycursor.execute("USE hospital")

    admitFrame = LabelFrame(root, padx=42, pady=20,borderwidth=0,highlightthickness=0)
    admitFrame.grid(row = 0, column = 0, rowspan = 4, columnspan = 2, sticky=N+E+S+W)    

    selectLabel = Label(admitFrame, text="Select Patient",font=('Helvetica',25))
    selectLabel.grid(row=0, column=0, pady = (0,15),columnspan=2)
    #Admit Labels
    nameLabel = Label(admitFrame, text="Name",font=('Helvetica',20))
    nameLabel.grid(row=1, column=0, padx=(0,160),pady=5, sticky=W)

    dobLabel = Label(admitFrame, text="Date of Birth",font=('Helvetica',20))
    dobLabel.grid(row=2, column=0, pady=5, sticky=W)

    #Admit Entries
    nameAdmit = Entry(admitFrame, font=('Helvetica',16))
    nameAdmit.grid(row=1, column=1, pady=5, sticky=E)

    dobAdmit = Entry(admitFrame, font=('Helvetica',16))
    dobAdmit.grid(row=2, column=1, pady=5, sticky=E)


    def admit():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        
        mycursor.execute("USE hospital")
        name = nameAdmit.get()
        dob = dobAdmit.get()
        #First check if patient exists in the patient table of the hospital database.
        if checkExists(name,dob):
            #Get patient id
            patientID = getPatientID(name,dob)
            #Check if patient is already admitted to the hospital
            sql = "SELECT * FROM room WHERE patient_id = %s"
            mycursor.execute(sql,(patientID,))
            myresult = mycursor.fetchall()
            #If not, admit assign patient a room and an available doctor
            #If patient already has a room, display an error.
            if mycursor.rowcount:
                for x in myresult:
                    messagebox.showerror("Error","Patient already has a room.\nRoom: " + x[0] + "\nDoctor: " + x[5] + "\nDate Admitted: " + x[4])
            #Assign patient an available room and an available doctor
            else:
                #Ask user if an emergency room is needed
                response = messagebox.askquestion("Emergency?","Does patient need an emergency room?")
                if response == "yes":
                    desiredRoom = "Emergency"
                elif response == "no":
                    desiredRoom = "Normal"

                
                #Finds next room that is not being used
                sql = "SELECT * FROM room  WHERE room_type = %s AND patient_id IS NULL ORDER BY CAST(room_number AS unsigned)"
                mycursor.execute(sql,(desiredRoom,))
                myresult = mycursor.fetchall()
                #If there are no more rooms avialable, display error.
                if not mycursor.rowcount:
                    messagebox.showerror("Error - Out of rooms","There are no more available rooms of this type.")
                else:
                    #Gets next available room of desired type.
                    for x in myresult:
                        availableRoom = x[0]
                        break

                    #Counts amount of doctors
                    sql = "SELECT * FROM doctor"
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()

                    availableDoctor = 0
                    lowestAmount = 10000

                    #Finds doctor that currently has the least amount of patients
                    for x in myresult:
                        sql = "SELECT DISTINCT * FROM doctor NATURAL JOIN room WHERE doctor_id = %s"
                        mycursor.execute(sql,(x[0],))
                        myresult2 = mycursor.fetchall()
                        patientCount = 0
                        doctorID = x[0]
                        for y in myresult2:
                            doctorID = y[0]
                            patientCount += 1
                        if patientCount < lowestAmount:
                            availableDoctor = doctorID
                            lowestAmount = patientCount
                            doctorName = x[1]

                    #Gets today's date as a string
                    currentDate = str(date.today().month) + "-" + str(date.today().day) + "-" + str(date.today().year)
                
                    sql = "UPDATE room SET patient_id = %s, date_admitted = %s, doctor_id = %s WHERE room_number = %s"
                    val = [(patientID,currentDate,availableDoctor,availableRoom)]
                    mycursor.executemany(sql,val)
                    mydb.commit()
                    messagebox.showinfo("Success","The patient has been admitted.\nRoom: " + availableRoom + "\nDoctor: " + doctorName + "\nDate Admitted: " + currentDate)

                    #Returns to main menu
                    back()

    #Function to return to main menu            
    def back():
        admitFrame.destroy()
        mainMenu()

    #Button to admit a patient
    admitButton = Button(admitFrame, text="Admit Patient", width=35,height=2, font=('Helvetica',18), command=admit)
    admitButton.grid(row=3, column=0, columnspan = 2, pady=(20,0))

    #Button to return to main menu
    backButton = Button(admitFrame, text="Back", width=15,height=1, font=('Helvetica',18), command=back)
    backButton.grid(row=4, column=1, columnspan = 1, pady=(20,0), sticky=E)


#Function for discharge menu GUI
def dischargePatient():
    root.title('Hospital Database - Discharge a Patient')
    root.geometry("580x360" + position)
    mycursor.execute("USE hospital")

    dischargeFrame = LabelFrame(root, padx=42, pady=20,borderwidth=0,highlightthickness=0)
    dischargeFrame.grid(row = 0, column = 0, rowspan = 4, columnspan = 2, sticky=N+E+S+W)    

    selectLabel = Label(dischargeFrame, text="Select Patient",font=('Helvetica',25))
    selectLabel.grid(row=0, column=0, pady = (0,15),columnspan=2)
    #Discharge Labels
    nameLabel = Label(dischargeFrame, text="Name",font=('Helvetica',20))
    nameLabel.grid(row=1, column=0, padx=(0,160),pady=5, sticky=W)

    dobLabel = Label(dischargeFrame, text="Date of Birth",font=('Helvetica',20))
    dobLabel.grid(row=2, column=0, pady=5, sticky=W)

    #Discharge Entries
    nameDischarge = Entry(dischargeFrame, font=('Helvetica',16))
    nameDischarge.grid(row=1, column=1, pady=5, sticky=E)

    dobDischarge = Entry(dischargeFrame, font=('Helvetica',16))
    dobDischarge.grid(row=2, column=1, pady=5, sticky=E)

    
    def discharge():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        
        mycursor.execute("USE hospital")
        name = nameDischarge.get()
        dob = dobDischarge.get()

        #First check if patient exists in the patient table of the hospital database.
        if checkExists(name,dob):
            #Get patient id
            patientID = getPatientID(name,dob)
            #Check if patient is currently admitted to the hospital
            sql = "SELECT * FROM room WHERE patient_id = %s"
            mycursor.execute(sql,(patientID,))
            myresult = mycursor.fetchall()
            #If patient is not currently admitted, display an error.
            if not mycursor.rowcount:
                messagebox.showerror("Error","Patient is not currently admitted.")
            #Remove patient from room and add to patient's record
            else:
                #Get room number, date of admittance, room charge, and doctorID
                for x in myresult:
                    roomNumber = x[0]
                    roomCharge = x[2]
                    admittedDate = x[4]
                    doctorID = x[5]

                #Get doctor's name and charge from doctor table
                sql = "SELECT * FROM room NATURAL JOIN doctor WHERE patient_id = %s"
                mycursor.execute(sql,(patientID,))
                myresult = mycursor.fetchall()
                for x in myresult:
                    doctorName = x[6]
                    doctorCharge = x[10]

                #Remove patient from room
                sql = "UPDATE room SET patient_id = NULL,date_admitted = NULL,doctor_id = NULL WHERE room_number = %s"
                mycursor.execute(sql,(roomNumber,))
                mydb.commit()

                #Count how how many records patient has to get next record number
                sql = "SELECT * FROM record WHERE patient_id = %s"
                mycursor.execute(sql,(patientID,))
                myresult = mycursor.fetchall()
                numRecords = 0
                if not mycursor.rowcount:
                    numRecords = 0
                else:
                    for x in myresult:
                        numRecords += 1
                #Adds one to get the next record number
                numRecords += 1

                #Gets current date admitted and date discharged in string format and date format
                admittedDate1 = admittedDate.split("-")
                d1 = date(int(admittedDate1[2]),int(admittedDate1[0]),int(admittedDate1[1]))

                dischargedDate = str(date.today().month) + "-" + str(date.today().day) + "-" + str(date.today().year)
                d2 = date.today()                
                #Find difference between date admitted and date discharged
                dateDiff = abs(d2-d1).days

                #Calculates patient's bill = doctor_charge + number of days * room_charge

                bill = int(doctorCharge) + int(dateDiff) * int(roomCharge)

                #By default, the bill is not paid immediately
                paid = "No"
                
                #Add new record
                sql =  "INSERT INTO record (patient_id, doctor_name, record_number, date_admitted, date_discharged, bill, paid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = [(patientID,doctorName,numRecords,admittedDate,dischargedDate,bill,paid)]
                mycursor.executemany(sql,val)
                mydb.commit()
                messagebox.showinfo("Success","The patient has been discharged.\nBill: $" + str(bill))

                #Return to main menu
                dischargeFrame.destroy()
                mainMenu()
                
    #Function to return to main menu            
    def back():
        dischargeFrame.destroy()
        mainMenu()

    #Button to discharge a patient
    dischargeButton = Button(dischargeFrame, text="Discharge Patient", width=35,height=2, font=('Helvetica',18), command=discharge)
    dischargeButton.grid(row=3, column=0, columnspan = 2, pady=(20,0))

    #Button to return to main menu
    backButton = Button(dischargeFrame, text="Back", width=15,height=1, font=('Helvetica',18), command=back)
    backButton.grid(row=4, column=1, columnspan = 1, pady=(20,0), sticky=E)

#Function for records menu GUI
def viewRecords():
    root.title('Hospital Database - View Records')
    root.geometry("590x680" + position)
    mycursor.execute("USE hospital")


    #Search Frame contains name and dob entries to search for a patient
    searchFrame = LabelFrame(root, padx=42, pady=20, text="Search")
    searchFrame.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky=N+E+S+W, padx = 5)

    selectLabel = Label(searchFrame, text="Select Patient",font=('Helvetica',25))
    selectLabel.grid(row=0, column=0, pady = (0,15),columnspan=2)

    #Search Labels
    nameSearchLabel = Label(searchFrame, text="Name",font=('Helvetica',20))
    nameSearchLabel.grid(row=1, column=0, padx=(0,160),pady=5, sticky=W)

    dobSearchLabel = Label(searchFrame, text="Date of Birth",font=('Helvetica',20))
    dobSearchLabel.grid(row=2, column=0, pady=5, sticky=W)

    #Search Entries
    nameSearch = Entry(searchFrame, font=('Helvetica',16))
    nameSearch.grid(row=1, column=1, pady=5, sticky=E)

    dobSearch = Entry(searchFrame, font=('Helvetica',16))
    dobSearch.grid(row=2, column=1, pady=5, sticky=E)


    #Information Frame contains information of selected patient
    recordFrame = LabelFrame(root, padx=42, pady=20, text="Records")
    recordFrame.grid(row = 4, column = 0, rowspan = 2, columnspan = 2, sticky=N+E+S+W, padx = 5)


    #Columns displayed in table
    columns = ('record','admitted','discharged','doctor','bill','paid')

    #Creates a treeview to display tabular data
    tree = ttk.Treeview(recordFrame, columns=columns, show='headings', height=12)

    tree.column('record',width = 70,anchor=W)
    tree.heading('record', text='Record #',anchor=W)

    tree.column('admitted',width = 90,anchor=W)
    tree.heading('admitted', text='Admitted',anchor=W)

    tree.column('discharged',width = 90,anchor=W)
    tree.heading('discharged', text='Discharged',anchor=W)
    
    tree.column('doctor',width = 100,anchor=W)
    tree.heading('doctor', text='Doctor',anchor=W)

    tree.column('bill',width = 70,anchor=W)
    tree.heading('bill', text='Bill',anchor=W)

    tree.column('paid',width = 70,anchor=W)
    tree.heading('paid', text='Paid',anchor=W)

    tree.grid(row=4, column=0, columnspan = 2, sticky=N+E+S+W)

    #Adds a scrollbar 
    scrollbar = Scrollbar(recordFrame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=4, column=1, sticky=N+S+E)


    def getRecords():
        #reconnects to server
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        
        mycursor.execute("USE hospital")
        name = nameSearch.get()
        dob = dobSearch.get()

        #First check if patient exists in the patient table of the hospital database.
        if checkExists(name,dob):
            #Get patient id
            patientID = getPatientID(name,dob)
            sql = "SELECT * FROM record WHERE patient_id = %s"
            mycursor.execute(sql,(patientID,))
            myresult = mycursor.fetchall()

            #If no records are found, display error.
            if not mycursor.rowcount:
                messagebox.showerror("Error","No records were found for this patient.")
            #Replace tablular data with records from selected patient 
            else:
                #Clear the treeview list items
                for item in tree.get_children():
                   tree.delete(item)
                for x in myresult:
                    tree.insert('', END, values=(x[2],x[3],x[4],x[1],x[5],x[6]))
    



    def paid():
        mydb = mysql.connector.connect(
            host=setHost,
            user=setUser,
            passwd=setPasswd
        )
        mycursor = mydb.cursor()
        
        mycursor.execute("USE hospital")
        name = nameSearch.get()
        dob = dobSearch.get()
        if checkExists(name,dob):
            #Get patient id
            patientID = getPatientID(name,dob)

            #If no row is selected, display error
            if not tree.focus():
                messagebox.showerror("Error","No record is selected.")
            else:
                #Gets record number of selected row
                selected_item = tree.focus()
                values = tree.item(selected_item, 'values')
                recordNum = (values[0])

                sql = "SELECT * FROM record WHERE patient_id = %s AND record_number = %s"
                mycursor.execute(sql, (patientID,recordNum))
                myresult = mycursor.fetchall()
                for x in myresult:
                    tree.item(selected_item, text="", values=(x[2],x[3],x[4],x[1],x[5],"Yes"))
                sql = "UPDATE record SET paid = 'Yes' WHERE patient_id = %s AND record_number = %s"
                mycursor.execute(sql, (patientID,recordNum))
                mydb.commit()

    #Function to return to main menu            
    def back():
        searchFrame.destroy()
        recordFrame.destroy()
        mainMenu()

    #Search and Back buttons
    searchButton = Button(searchFrame, text="Get Records", width=15,height=1, font=('Helvetica',18), command=getRecords)
    searchButton.grid(row=3, column=0, columnspan = 2, pady=(20,0))

    paidButton = Button(recordFrame, text="Paid", width=15,height=1, font=('Helvetica',18), command=paid)
    paidButton.grid(row=5, column=0, pady=(20,0), sticky=W)

    backButton = Button(recordFrame, text="Back", width=15,height=1, font=('Helvetica',18), command=back)
    backButton.grid(row=5, column=1, pady=(20,0), sticky=E)
    


response = messagebox.askquestion("Reset","Reset databases?")
if response == "yes":
    mycursor.execute("DROP DATABASE administrators")
    mycursor.execute("DROP DATABASE hospital")

#Checks if administrators database exists
sql = "SHOW DATABASES LIKE 'administrators'"
mycursor.execute(sql)
myresult = mycursor.fetchall()

#If it does not exist it runs a file to create the databases and classes
if not mycursor.rowcount:
    createDatabases.create()
    #Fills databases with values for testing
    fillDatabases.fill()

    #reconnects to server to get newly created databases and info
    mydb = mysql.connector.connect(
        host=setHost,
        user=setUser,
        passwd=setPasswd
    )
    mycursor = mydb.cursor()

#Opens login menu
loginMenu()

#Ends GUI
root.mainloop()
