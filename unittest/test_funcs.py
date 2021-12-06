import unittest
import funcs
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password"
)
mycursor = mydb.cursor()

#Creates and Uses test database, tables, and values to test functions
#smycursor.execute("DROP DATABASE projectTest")

sql = "SHOW DATABASES LIKE 'projectTest'"
mycursor.execute(sql)
myresult = mycursor.fetchall()

if not mycursor.rowcount:

    mycursor.execute("CREATE DATABASE projectTest")
    mycursor.execute("USE projectTest")

    mycursor.execute("""CREATE TABLE admin (
                        admin_id VARCHAR(255),
                        username VARCHAR(255),
                        password VARCHAR(255),
                        primary key (admin_id))""")

    mycursor.execute("insert into admin values ('1','Admin','Password')")

    mycursor.execute("""CREATE TABLE patient (
                        patient_id VARCHAR(255),
                        name VARCHAR(255),
                        dob VARCHAR(255),
                        gender VARCHAR(255),
                        address VARCHAR(255),
                        disease VARCHAR(255),
                        insurance VARCHAR(255),
                        primary key (patient_id))""")

    mycursor.execute("insert into patient values ('1','Patient1','06-13-2000','Male','My Address','My disease','My insurance company')")

    mydb.commit()
else:
    mycursor.execute("USE administratorsTest")


#Class where test functions are defined
class TestFuncs(unittest.TestCase):

    def test_login(self):
        #Test when a sign in username and password is correct
        result = funcs.signIn("Admin","Password")
        self.assertTrue(result)
        #Test when a sign in username and password is incorrect
        result = funcs.signIn("WrongName","WrongPassword")
        self.assertFalse(result)

    def test_viewinfo(self):
        #Test when user enters a valid name and d.o.b in the patient database
        result = funcs.viewInfo("Patient1","06-13-2000")
        self.assertTrue(result)
        #Test when user enters an invalid name and d.o.b in the patient database
        result = funcs.viewInfo("NameOfPatient2000","02-23-1834")
        self.assertFalse(result)        


#Runs all tests
if __name__ == '__main__':
    unittest.main()
