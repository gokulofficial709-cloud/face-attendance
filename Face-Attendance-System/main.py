import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://dapper-system-default-rtdb.firebaseio.com/",
    "storageBucket":"dapper-system.appspot.com"
})
bucket=storage.bucket()

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)
imgBackground = cv2.imread('Resources/background.png')
modepath = 'Resources/Modes'
modepathlist=os.listdir(modepath)
imgmodelist=[]
for path in modepathlist:
    imgmodelist.append(cv2.imread(os.path.join(modepath,path)))
print("Loading encoded file")
file=open('EncodeFile.p','rb')
encodelistknownwithIds=pickle.load(file)
file.close()
encodelistknown,studentId=encodelistknownwithIds
#print(studentId)
print("Encoded file loaded")
ModeType=0
counter=0
id=-1
imgstudent=[]

while True:
    success, img=cap.read()
    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs= cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    facecurframe=face_recognition.face_locations(imgs)
    encodecurframe=face_recognition.face_encodings(imgs,facecurframe)


    imgBackground[162:162+480,55:55+640]= img
    imgBackground[44:44+633,808:808+414]=imgmodelist[ModeType]
    if facecurframe:
        for encodeface,faceloc in zip(encodecurframe,facecurframe):
            matches = face_recognition.compare_faces(encodeface,encodelistknown)
            faceDis=face_recognition.face_distance(encodeface,encodelistknown)
            #print("Matches", matches)
            #print("faceDis", faceDis)

            matchIndex=np.argmin(faceDis)
            #print("MatchIndex",matchIndex)
            if matches[matchIndex]:
                print("know face detected")
                print(studentId[matchIndex])
                y1,x2,y2,x1=faceloc
                y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
                bbox=55 + x1, 162 + y1,x2 - x1,y2 -y1
                imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
                id=studentId[matchIndex]
                if counter==0:
                    cvzone.putTextRect(imgBackground,'loading',(275,400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter=1
                    ModeType=1


        if counter!=0:
            #get the data
            if counter==1:
                studentinfo=db.reference(f'Students/{id}').get()
                print(studentinfo)
                #get the image
                blob=bucket.get_blob(f'Images/{id}.png')
                array=np.frombuffer(blob.download_as_string(), np.uint8)
                imgstudent=cv2.imdecode(array,cv2.COLOR_BGRA2RGB)
                #update data of attendance
                datetimeobject=datetime.strptime(studentinfo['last_attendance_time'],"%y-%m-%d %H:%M:%S")
                secondsElapsed=(datetime.now()-datetimeobject).total_seconds()
                #print(secondsElapsed)
                if secondsElapsed>30:

                    ref=db.reference(f'Students/{id}')
                    studentinfo['total_attendance']+=1
                    ref.child('total_attendance').set(studentinfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
                else:
                    ModeType=3
                    counter=0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[ModeType]

            if ModeType!=3:

                if 10<counter<30:
                    ModeType=2
                imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[ModeType]
                if counter<=10:
                    cv2.putText(imgBackground,str(studentinfo['total_attendance']),(861,125),
                          cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground, str(studentinfo['major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentinfo['standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(imgBackground, str(studentinfo['year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(imgBackground, str(studentinfo['Batch']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)

                    (w,h),_=cv2.getTextSize(studentinfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2
                    cv2.putText(imgBackground, str(studentinfo['name']), (808+offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    imgBackground[175:175+216,909:909+216]=imgstudent
                counter+=1

                if counter>=20:
                    counter=0
                    ModeType=0
                    studentinfo=[]
                    imgstudent=[]
                    imgBackground[44:44 + 633, 808:808 + 414] = imgmodelist[ModeType]
    else:
        ModeType=0
        counter=0
    #cv2.imshow("webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)