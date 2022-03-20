from flask import Flask, request,render_template,redirect,Response,flash,url_for
import os
import mysql.connector
from cryptography.fernet import Fernet
import cv2 as cv
import numpy as np
from deepface import DeepFace
from PIL import Image
from io import BytesIO
import model


folder=os.path.dirname(__file__)

#from videocapture import *

#connect to postgreSQL database
def connect_database():
    global db
    db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="sahil121",
    database="strike"
    )
connect_database()

# password encryptor
def encrypter(password):
    fkey=open("file_key.txt",'rb')
    key=fkey.read()
    cipher=Fernet(key)
    print("Value in encrypter function - ",password)
    encrypted_pass=cipher.encrypt(bytes(password,'utf-8'))
    print("Function answer by decrypter - ",encrypted_pass)
    return encrypted_pass

def decrypter(password):
    fkey=open("file_key.txt",'rb')
    key=fkey.read()
    cipher=Fernet(key)
    print("Value in decryptor function - ",password)
    decrypted_pass=cipher.decrypt(password)
    print("Function answer by decryptor - ",decrypted_pass)
    return decrypted_pass.decode()

#Load image to database
def store(pic,name):
    '''def digital_to_binary(image_name):
        # Convert digital data to binary format
        with open(image_name, 'rb') as file:
            binaryData = file.read()
        return binaryData'''

    rect,pict =cv.imencode('.jpg',pic)
    picture=pict.tobytes()
    cursor=db.cursor()   
    if user_type=='admin' :
        sql=("update admins set image=%s where name='{n}'").format(n=name)
    elif user_type=='student':
        sql = ("update users set image=%s where name='{n}'").format(n=name)   
    args = (picture, )       
    cursor.execute(sql,args)
    db.commit()
    
def receive(name_face):
    global data
    cursor=db.cursor()
    if usertype=='admin':
        query1= ("SELECT image from admins where username='{n}' ").format(n=name_face)
    elif usertype=='student':
        query1= ("SELECT image from users where username='{n}' ").format(n=name_face)
    cursor.execute(query1)
    data=cursor.fetchall()
    im = Image.open(BytesIO(data[0][0]))
    #im1=im.convert("RGB")
    #img=np.array(im1.getdata())
    opencvImage = cv.cvtColor(np.array(im), cv.COLOR_RGB2BGR)
    return opencvImage

#Login check
'''def login(train,test):
    global ex
    j= DeepFace.verify(img1_path = train, img2_path =test,enforce_detection=False)
    print(j['verified'])
    ans=j['distance']
    print(ans)
    if ans>0.1:
        ex=0
    elif ans<=0.1:
        print("Exam de")
        ex=1
    return ex'''

def login(train,test,name):
    y=model.face(train,test,name)
    print(y)
#load Image from database

#video function
global capture,verification
capture=0
verification=0

'''def generate_frames(video):
    width=600
    faces  = cv.CascadeClassifier(os.path.join(folder,'haarcascade_frontalface_default.xml'))
    eyes = cv.CascadeClassifier(os.path.join(folder,'haarcascade_eye.xml'))
    vid = cv.VideoCapture(0)
    counter = 0
    count =10
    timer = 0
    attempts = 3
    counter_eyes = 0
    count_eyes =10
    timer_eyes = 0
    attempts = 3
    while True:
        status,img = vid.read()
        img=imutils.resize(img,width)
        gray_face = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        face = faces.detectMultiScale(gray_face,1.9,5)
        if len(face) > 0:
            for (x,y,w,h) in face:
                cv.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
                eyes_gray = gray_face[y:y+h,x:x+w]
                eyes_img = img[y:y+h,x:x+w]
                eye = eyes.detectMultiScale(eyes_gray,1.8,5)
                if len(eye) > 1:
                    for (ex,ey,ew,eh) in eye:  
                        
                        cv.rectangle(eyes_img,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
                        eye=True
                        counter_eyes = 0
                        count_eyes = 10
                else:
                    cv.putText(img,f'look at the screen',(313,255),cv.FONT_HERSHEY_SIMPLEX, .5,(255,255,255),2,cv.LINE_AA)
                    counter_eyes += 1
                    if counter > 500:
                        cv.putText(img,f'look at the screen or else you will be disqualified {count_eyes} sec',(60,420),cv.FONT_HERSHEY_TRIPLEX, .5,(0,0,255),2,cv.LINE_AA)
                    timer_eyes +=1
                    if timer_eyes == 50:
                        timer_eyes = 0
                        count-=1
                    if count_eyes == 0:
                        break
                    if count_eyes == 5 and timer_eyes == 50:
                        attempts -=1
                    if attempts == 0:
                        break

            counter = 0
            count = 10            
        else:
            cv.rectangle(img,(350,290),(470,310),(0,0,255),-1)
            cv.putText(img,f'Not detected',(363,305),cv.FONT_HERSHEY_SIMPLEX, .5,(255,255,255),2,cv.LINE_AA)
            counter +=1
            if counter > 500:
                cv.rectangle(img,(55,400),(600,440),(0,0,255),1)
                cv.putText(img,f'You will be disqualified if you dont return to exam in {count} sec',(60,420),cv.FONT_HERSHEY_TRIPLEX, .5,(0,0,255),2,cv.LINE_AA)
                timer +=1
                if timer == 50:
                    timer = 0
                    count-=1
                if count == 0:
                    break
                
                if count == 5 and timer == 50:
                    attempts -=1
                if attempts == 0:
                    break
        #cv.imshow('IMG',img)
        #if cv.waitKey(30) == ord('q') & 0xff:
            #break
    #vid.release()
    #cv.destroyAllWindows()
        ret,jpeg=cv.imencode('.jpg',img)
        frame=jpeg.tobytes()
        yield(b'--frame2\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')'''
        
def camera(video,name):
    url=cv.VideoCapture(0)
    global capture,verification,verified
    while True:
    
        img,frame=url.read()
        if img:
            if(capture):
                capture=0
                '''p=os.path.sep.join(['./code/shots',"{name}.jpg"]).format(name=name)
                cv.imwrite(p,frame)
                path='C:\SEM-5\Strike\code\shots\{na}.jpg'.format(na=name)'''
                store(frame,name)
            
            elif(verification):
                verification=0
                verified=login(receive(name),frame,name)
                print(verified)
                if verified:
                    return redirect('/exam')
                
                

            else:
                ret,jpeg=cv.imencode('.jpg',frame)
                frms=jpeg.tobytes()
                yield(b'--frame2\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n'+frms+b'\r\n')
            #except Exception as e:
                #pass
        else:
            pass
    
 

signup=Flask(__name__,template_folder='templates')
signup.secret_key='strike'
@signup.route("/")
def homepage():
    return render_template('homepage.html')


@signup.route("/home",methods=["POST","GET"])
def checklogin():
    global data,temp_name,usertype,verified
    if request.method=="POST":
        usertype=request.form['user_type']
        username=request.form["username"]
        pswd=request.form["password"]
        cursor=db.cursor()
        query1= ("SELECT username, password from users WHERE username='{id}'").format(id=username)
        query2=("SELECT username, password from admins WHERE username='{id}'").format(id=username)
        if usertype=='admin':
            cursor.execute(query2)
        elif usertype=='student':
            cursor.execute(query1)
        data=cursor.fetchall()
        if len(data)==1:
            decrypt_password=decrypter(data[0][1])
            if decrypt_password==pswd:
                temp_name=username
                verified=0
                return render_template("face_reg.html")
            else:
                return render_template('homepage.html')
        else:
            return render_template('homepage.html')
    
            
@signup.route("/register",methods=["GET","POST"])
def registerpage():
    global get_name,temp_name,user_type
    if request.method=="POST":
        user_type=request.form['user_type']
        get_name=request.form["name"]
        get_username=request.form["username"]
        get_pswd=request.form["password"]
        get_email=request.form["email"]
        get_contact=request.form["phone"]
        get_sapid=request.form["SapID"]
        encrypt_password=encrypter(get_pswd)
        cursor=db.cursor()
        query4=("INSERT INTO admins(name,username,password,email,phone,sapid) VALUES('{n}','{un}','{p}','{e}','{s}','{ph}')").format(n=get_name,un=get_username,p=encrypt_password.decode(),e=get_email,ph=get_contact,s=get_sapid)
        query3=("INSERT INTO users(name,username,password,email,phone,sapid) VALUES('{n}','{un}','{p}','{e}','{s}','{ph}')").format(n=get_name,un=get_username,p=encrypt_password.decode(),e=get_email,ph=get_contact,s=get_sapid)
        
        if user_type=='admin':
            admin_key=request.form['key']
            
            if admin_key=='notstudent':
                cursor.execute(query4)
                db.commit()
                temp_name=get_name
                return render_template('reg_photo.html')  
            else:
                print('Not admin')
                return render_template('Register.html')
        elif user_type=='student':
            cursor.execute(query3)
            db.commit()
            temp_name=get_name
            return render_template('reg_photo.html')
        else:
            return render_template('Register.html')
        
        
        
    return render_template('Register.html')



@signup.route("/video",methods=["GET","POST"])
def video():
    global video
    return Response(camera(video,temp_name),mimetype='multipart/x-mixed-replace; boundary=frame')

@signup.route("/requests",methods=['POST','GET'])
def cap():
    global camera
    if request.method=="POST":
        if request.form.get('click')=='Capture':
            global capture
            capture=1
        elif request.method=='GET':
            return render_template('reg_photo.html')
    return render_template('homepage.html')

@signup.route("/verif",methods=['POST','GET'])
def verif():
    global camera,verification
    if request.method=="POST":
        if request.form.get('click')=='Verify':
    
            verification=1
        elif request.method=='GET':
            return render_template('face_reg.html')
    return render_template("face_reg.html")
    
    
@signup.route("/exam",methods=['POST','GET'])
def exam():
    return render_template('exam.html')



if __name__ == "__main__":
    signup.run()