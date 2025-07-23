import cv2
import os
import pickle
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://dapper-system-default-rtdb.firebaseio.com/",
    "storageBucket":"dapper-system.appspot.com"
})
#importing student images
folderpath= 'Images'
pathlist=os.listdir(folderpath)
print(pathlist)
imglist=[]
studentId=[]
for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    studentId.append(os.path.splitext(path)[0])

    filename = f'{folderpath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)
print(studentId)

def findencodings(imagelist):
    encodelist=[]
    for img in imagelist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)
        if len(encode)>0:
            encode=encode[0]
        encodelist.append(encode)
    return encodelist
print("encoding started")
encodelistknown=findencodings(imglist)
encodelistknownwithIds=[encodelistknown,studentId]
print(len(encodelistknown))
print("encoding ended")
file=open("EncodeFile.p",'wb')
pickle.dump(encodelistknownwithIds,file)
file.close()