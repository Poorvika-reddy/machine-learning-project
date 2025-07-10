import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import cv2
import threading

def detect_ears(name):
    # Load the left ear and right ear classifiers
    left_ear_classifier = cv2.CascadeClassifier("haarcascade_mcs_leftear.xml")
    right_ear_classifier = cv2.CascadeClassifier("haarcascade_mcs_rightear.xml")
    
    if left_ear_classifier.empty() or right_ear_classifier.empty():
        print("Error loading ear cascade classifiers. Please ensure the files 'haarcascade_mcs_leftear.xml' and 'haarcascade_mcs_rightear.xml' are present in the working directory.")
        return
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error initializing webcam. Please check your camera connection.")
        return
    
    print("Starting ear detection. Press 'q' to exit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from webcam.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect left ears
        left_ears = left_ear_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Detect right ears
        right_ears = right_ear_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        print(f"Detected {len(left_ears)} left ears, {len(right_ears)} right ears")
        
        # Combine detected ears
        ears = []
        if len(left_ears) > 0:
            ears.extend(left_ears)
        if len(right_ears) > 0:
            ears.extend(right_ears)
        
        for (x, y, w, h) in ears:
            print(f"Drawing rectangle for ear at x:{x}, y:{y}, w:{w}, h:{h}")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(frame, "Ear Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            
            # Mark attendance
            attendance_data = {name: "Present"}
            root = ET.Element("attendance")
            for name, status in attendance_data.items():
                student = ET.SubElement(root, "student")
                student.set("name", name)
                student.set("status", status)
            tree = ET.ElementTree(root)
            tree.write("attendance.xml")
            messagebox.showinfo("Attendance Marked", f"Attendance marked for {name}")
            cap.release()
            cv2.destroyAllWindows()
            return
        
        cv2.imshow("Ear Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def mark_attendance():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("classifier.xml")
    attendance_data = {}
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error initializing webcam. Please check your camera connection.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            id_, confidence = recognizer.predict(face_roi)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if confidence < 50:
                with open("name.txt", "r") as f:
                    content = f.readlines()
                    if id_ <= len(content):
                        n = content[id_ - 1]
                        name = n.strip()[4:]
                        confidence_text = f"Confidence: {round(100 - confidence)}%"
                        if name not in attendance_data:
                            attendance_data[name] = "Present"
                            cap.release()
                            cv2.destroyAllWindows()
                            messagebox.showinfo("Face Recognized", f"{name}, now show your ear to mark attendance.")
                            threading.Thread(target=detect_ears, args=(name,)).start()
                            return
                    else:
                        name = "Unknown"
                        confidence_text = f"Confidence: {round(100 - confidence)}%"
            else:
                name = "Unknown"
                confidence_text = f"Confidence: {round(100 - confidence)}%"

            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, confidence_text, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def mark():
    root = tk.Tk()
    root.title("Attendance System")
    root.geometry("300x200")

    btn_mark_attendance = tk.Button(root, text="Mark Attendance", command=mark_attendance)
    btn_mark_attendance.pack(pady=50)

    root.mainloop()
