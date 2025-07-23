# 🎯 Face Recognition Attendance System

A **real-time face recognition attendance system** built using Python, OpenCV, and Firebase. It detects and recognizes students' faces through a webcam and automatically updates their attendance records in Firebase.

---

## 📸 Features

- Real-time face detection and recognition via webcam
- Automatic attendance marking in Firebase Realtime Database
- Face image uploads to Firebase Storage
- Smart time-threshold check to avoid repeated attendance entries
- Displays student details upon successful recognition
- Background UI interface using pre-designed mode images

---

## 🧰 Technologies Used

- Python 3
- OpenCV
- face_recognition
- Firebase Admin SDK
- NumPy
- cvzone

---

## 🗂️ Project Structure

.
├── encoder.py # Script to encode student faces and upload images to Firebase
├── firebase.py # Script to add initial student data to Firebase Realtime Database
├── main.py # Main script to run the face recognition attendance system
├── EncodeFile.p # Pickle file storing encoded face data and student IDs
├── Images/ # Folder containing student face images (named by student ID)
├── Resources/
│ ├── background.png # Background layout for display
│ └── Modes/ # Folder with different mode overlays (loading, verified, etc.)
├── serviceAccountKey.json # Firebase credentials (NOT included in repo for security)



📊 Sample Firebase Data Format


."22ucs090": {
  "name": "Gokulnath.s",
  "major": "'III'-CS('B')",
  "Batch": "2022-25",
  "total_attendance": 40,
  "standing": "G",
  "year": "III",
  "last_attendance_time": "24-08-08 11:50:24"
}



✍️ Author
Gokulnath S
BSc Computer Science, 2025
📧 Email: gokulofficial709@gmail.com


