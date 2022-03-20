import cv2 as cv
import numpy as np
import os
import imutils


folder=os.path.dirname(__file__)
width=800
faces  = cv.CascadeClassifier(os.path.join(folder,'./haarcascade_frontalface_default.xml'))
eyes = cv.CascadeClassifier(os.path.join(folder,'./haarcascade_eye.xml'))
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
    cv.imshow('IMG',img)
    if cv.waitKey(1) == ord('q'):
        break
vid.release()
cv.destroyAllWindows()
