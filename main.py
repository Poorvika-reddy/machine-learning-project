from tkinter import *
from PIL import Image,ImageTk   
from Recognize import reco
from Mark_attendance import mark
from Train_data import traindata
from Add_face import addface


def attend_button_click():
    mark()



root=Tk()

root.title("FACE RECOGNIZATION")
root.geometry('1900x1000')

#background img------------------------------
bg_img=Image.open("800_390_face-recognition.png")
bg_img=bg_img.resize((1900,1000))
main_img=ImageTk.PhotoImage(bg_img)
main_lbl=Label(root,image=main_img)
main_lbl.place(x=0,y=0)


title_txt=Label(root,text="Face Recognization",font=("times new roman",50,"bold"),)
title_txt.place(x=650,y=10)

#StudentName_txt=Label(root,text="Anish K S \n Seshadripuram Degree College  \n BCA 3rd Year",font=("times new roman",30,"bold"),)
#StudentName_txt.place(x=1300,y=700)

addface_txt=Label(root,text="ADD FACE",font=("times new roman",25,"bold"),)
addface_txt.place(x=165,y=150)
addface_img=Image.open("1_YF4KdQE-RadFtNa6n66wdg.gif")
addface_img=addface_img.resize((300,300))
mainaddface_img=ImageTk.PhotoImage(addface_img)
addface_btn=Button(root,image=mainaddface_img,command=addface)
addface_btn.place(x=100,y=200,height=300,width=300)

title_txt=Label(root,text="TRAIN DATA",font=("times new roman",25,"bold"),)
title_txt.place(x=580,y=150)
train_img=Image.open("trainface.jpg")
train_img=train_img.resize((300,300))
maintrain_img=ImageTk.PhotoImage(train_img)
mainyrain_btn=Button(root,image=maintrain_img,command=traindata)
mainyrain_btn.place(x=550,y=200,height=300,width=300)

title_txt=Label(root,text="RECOGNIZE FACES",font=("times new roman",25,"bold"),)
title_txt.place(x=90,y=550)
recognizeface_img=Image.open("Telpo-TPS980-face-recognition-machine.jpg")
recognizeface_img=recognizeface_img.resize((300,300))
maintrainface_img=ImageTk.PhotoImage(recognizeface_img)
mainrecon_btn=Button(root,image=maintrainface_img,command=reco)
mainrecon_btn.place(x=100,y=600,height=300,width=300)

title_txt=Label(root,text="ATTENDANCE",font=("times new roman",25,"bold"),)
title_txt.place(x=580,y=550)
attendance_img=Image.open("Screenshot 2023-10-01 122705.png")
attendance_img=attendance_img.resize((300,300))
mainatted_img=ImageTk.PhotoImage(attendance_img)
attend_btn=Button(root,image=mainatted_img,command=attend_button_click)
attend_btn.place(x=550,y=600,height=300,width=300)

root.mainloop()