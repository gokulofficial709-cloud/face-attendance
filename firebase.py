import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://dapper-system-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')
data={

    "22ucs090":
        {
            "name": "Gokulnath.s",
            "major": "'III'-CS('B')",
            "Batch":'2022-25',
            "total_attendance":  40,
            "standing":"G",
            "year":'III',
            "last_attendance_time":"24-08-08 11:50:24",
        },

    "22ucs100":
        {
            "name": "kavin.S",
            "major": "'III'-CS('B')",
            "Batch":'2022-25',
            "total_attendance":  38,
            "standing":"G",
            "year":'III',
            "last_attendance_time":"24-08-08 11:50:24",
        },






}
for key,value in data.items():
    ref.child(key).set(value)