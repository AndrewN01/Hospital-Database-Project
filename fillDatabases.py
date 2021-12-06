import mysql.connector


def fill():

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password"
    )
    mycursor = mydb.cursor()

    #Fills admin database with test login information
    mycursor.execute("USE administrators")
    mycursor.execute("insert into admin values ('1','Admin','Password')")
    mycursor.execute("insert into admin values ('2','Andrew','1234')")
    mycursor.execute("insert into admin values ('3','User','Birthday')")
    mycursor.execute("insert into admin values ('4','1','2')")


    mycursor.execute("USE hospital")
    #patient
    mycursor.execute("insert into patient values ('1','Patient1','06-13-2000','Male','My Address','My disease','My insurance company','YDSID2042')")
    #doctor
    mycursor.execute("insert into doctor values ('1','Doctor1','7-29-1992','Male','DoctorAddress','300')")
    mycursor.execute("insert into doctor values ('2','Doctor2','4-12-1987','Male','DoctorAddress','350')")
    #room
    mycursor.execute("insert into room values ('1','Normal','200',NULL,NULL,NULL)")
    mycursor.execute("insert into room values ('2','Normal','200',NULL,NULL,NULL)")
    mycursor.execute("insert into room values ('3','Normal','200',NULL,NULL,NULL)")
    mycursor.execute("insert into room values ('4','Emergency','400',NULL,NULL,NULL)")
    mycursor.execute("insert into room values ('5','Emergency','400',NULL,NULL,NULL)")
    #record
    mycursor.execute("insert into record values ('1','1','12-02-2021','12-05-2021','1200')")
    
    mydb.commit()
    mycursor.close()
    return
