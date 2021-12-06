import mysql.connector


def create():

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password"
    )
    mycursor = mydb.cursor()

    #Database to store administrator login information
    mycursor.execute("CREATE DATABASE administrators")
    mycursor.execute("USE administrators")
    #admin table
    mycursor.execute("""CREATE TABLE admin (
                        admin_id VARCHAR(255),
                        username VARCHAR(255),
                        password VARCHAR(255),
                        primary key (admin_id))""")

    #Database to store everything for a hospital
    mycursor.execute("CREATE DATABASE hospital")
    mycursor.execute("USE hospital")
    #patient table
    mycursor.execute("""CREATE TABLE patient (
                        patient_id VARCHAR(255),
                        name VARCHAR(255),
                        dob VARCHAR(255),
                        gender VARCHAR(255),
                        address VARCHAR(255),
                        disease VARCHAR(255),
                        insurancename VARCHAR(255),
                        insuranceID VARCHAR(255),
                        primary key (patient_id))""")
    #doctor table
    mycursor.execute("""CREATE TABLE doctor (
                        doctor_id VARCHAR(255),
                        name VARCHAR(255),
                        dob VARCHAR(255),
                        gender VARCHAR(255),
                        address VARCHAR(255),
                        charge VARCHAR(255),
                        primary key (doctor_id))""")
    #room table
    mycursor.execute("""CREATE TABLE room (
                        room_number VARCHAR(255),
                        room_type VARCHAR(255),
                        room_charge VARCHAR(255),
                        patient_id VARCHAR(255),
                        date_admitted VARCHAR(255),
                        doctor_id VARCHAR(255),
                        primary key (room_number),
                        foreign key (patient_id) references patient(patient_id),
                        foreign key (doctor_id) references doctor(doctor_id))""")
    #record table
    mycursor.execute("""CREATE TABLE record (
                        patient_id VARCHAR(255),
                        record_number VARCHAR(255),
                        date_admitted VARCHAR(255),
                        date_discharged VARCHAR(255),
                        bill VARCHAR(255),
                        primary key (patient_id,record_number),
                        foreign key (patient_id) references patient(patient_id) on delete cascade)""")


    
    mydb.commit()

    
    """
    THIS IS FOR TESTING
    mycursor.execute("insert into admins values ('1','Efren','Password')")
    mycursor.execute("insert into admins values ('2','Efren2','Password')")
    mycursor.execute("insert into admins values ('3','Efren3','Password')")
    mycursor.execute("insert into admins values ('4','Efren4','Password')")

    mydb.commit()
    sql = "SELECT * FROM admins"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    #print(mycursor.rowcount)
    for x in myresult:
        print(x[1])
    """

    mycursor.close()
    return
