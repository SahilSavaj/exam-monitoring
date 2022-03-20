
import cv2 
import numpy as np
import os
import base64
import mysql.connector
from PIL import Image
from io import StringIO,BytesIO
from deepface import DeepFace

folder=os.path.dirname(__file__)
 
def connect_database():
    global db
    db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="sahil121",
    database="strike"
    )
connect_database()

def store(pic):
    def digital_to_binary(image_name):
            # Convert digital data to binary format
            with open(image_name, 'rb') as file:
                binaryData = file.read()
            return binaryData

    Picture =digital_to_binary(pic)
    sql = 'INSERT INTO image VALUES(%s)'    
    args = (Picture, )
    cursor=db.cursor()
    cursor.execute(sql,args)
    db.commit()

#store('C:\SEM-5\Strike\code\shots/test.jpg')

def receive():
    global data
    cursor=db.cursor()
    query1= ("SELECT image from users where name='sahil savaj' ")
    cursor.execute(query1)
    data=cursor.fetchall()
    def write_file(data, filename):
        with open(filename, 'wb') as file:
            file.write(data)
    write_file(data[0][0],'test.jpg')
    print(data[0][0])

receive()

'''a=verification=DeepFace.verify(img1_path="C:\SEM-5\Strike\code\shots/1111.jpg",img2_path="C:\SEM-5\Strike/test.jpg")
print(a)'''


