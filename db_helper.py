import mysql.connector
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(r"D:\emotion_detection\my_env.env")
import sys

class dbHelper:
    """dbHelper class is used to store and update the data in the database
    """
    def __init__(self):
        try:
            self.conn=mysql.connector.connect(host=os.getenv("host_name"), user=os.getenv("db_user_name"), password=os.getenv("db_password"),database=os.getenv("db_name"))

            self.mycursor=self.conn.cursor(buffered=True)
        except Exception as e:
            print("some erorr occure in  connected to Database",e)
            sys.exit(0)
        else:
            print("Coonected to database")
    def store(self,mood):
        """store methos is used to store the facial expression into the database
        Args : 
            mood : mood is facial expressionon
        Retirns :
            none
        """
        try:
            print("In store method---",mood)
            self.mood=mood
            print(111)
            if self.mycursor.execute("select * from emotion_detection;") is None:
                print(222)
                self.mycursor.execute("INSERT INTO emotion_detection (Mood) VALUES('"+self.mood+"');")
                self.conn.commit()
            else:
                print(333)
                self.mycursor.execute("INSERT INTO emotion_detection (Mood) VALUES('"+self.mood+"');")
                self.conn.commit()
        except Exception as e:
            print("ERROR :  db store method failed  ",e)