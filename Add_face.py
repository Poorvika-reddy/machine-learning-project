from tkinter import *
from tkinter import simpledialog
import cv2



def addface():
        face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        ROOT=Tk()
        ROOT.withdraw()
        id=simpledialog.askinteger(title="USER ID",prompt="Enter Your ID")
        Name=simpledialog.askstring(title="USER Name",prompt="Enter Your Name")
        f=open("name.txt","a")
        f.write(f"{id}st {Name}\n")
        f.close
        img_id=1

        def facecrop(img):
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=face_classifier.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                facecrop=img[y:y+h,x:x+w]
                return facecrop
            
        cap=cv2.VideoCapture(0)
        imgId=0
        while True:
            ret,myFrame=cap.read()
            if facecrop(myFrame) is not None:
                imgId+=1
                face=cv2.resize(facecrop(myFrame),(600,600))
                face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                facedataPath="faceData/user."+str(id)+"."+str(img_id)+".jpg"
                cv2.imwrite(facedataPath,face)
                cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)
                cv2.imshow("live",face)
                img_id+=1
            if cv2.waitKey(1)==13 or int(img_id)==100: #you can set number of image for now 100 images per person is ok
                break
        cap.release()

