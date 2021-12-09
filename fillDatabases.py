import mysql.connector

def fill():

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="password"
    )
    mycursor = mydb.cursor()

    #Fills admin database with test login information. Passwords are encrypted with a key
    mycursor.execute("USE administrators")
    mycursor.execute("insert into admin values ('1','Admin',aes_encrypt('password','Password'))")
    mycursor.execute("insert into admin values ('2','Andrew',aes_encrypt('password','1234'))")
    mycursor.execute("insert into admin values ('3','User',aes_encrypt('password','Birthday'))")
    mycursor.execute("insert into admin values ('4','1',aes_encrypt('password','2'))")


    mycursor.execute("USE hospital")
    #patient
    mycursor.execute("insert into patient values ('1','Patient1','01-01-2000','Male','My Address','My disease','My insurance company','YDSID2042')")
    mycursor.execute("insert into patient values ('2','Patient2','04-18-2005','Male','My Address','My disease','My insurance company','YDHRf042')")
    mycursor.execute("insert into patient values ('3','P','D','Male','My Address','My disease','My insurance company','YDHRf042')")


    #doctor
    mycursor.execute("insert into doctor values ('1','Doctor1','7-29-1992','Male','DoctorAddress','300')")
    mycursor.execute("insert into doctor values ('2','Doctor2','4-12-1987','Male','DoctorAddress','350')")
    #room
    mycursor.execute("insert into room values ('1','Normal','200','1','12-5-2021','1')")
    mycursor.execute("insert into room values ('2','Normal','200','2','12-6-2021','1')")
    mycursor.execute("insert into room values ('3','Normal','200',NULL,NULL,NULL)")
    mycursor.execute("insert into room values ('4','Emergency','400',NULL,NULL,NULL)")
    mycursor.execute("insert into room values ('5','Emergency','400',NULL,NULL,NULL)")
    #record
    mycursor.execute("insert into record values ('1','Doctor1','1','12-02-2021','12-05-2021','1200','No')")
    
    mydb.commit()
    mycursor.close()
    return
