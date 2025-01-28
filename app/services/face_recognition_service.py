# app/services/face_recognition_service.py

import face_recognition
import cv2
import numpy as np
from sqlalchemy.orm import Session
from app.database import User, Attendance
from app.services.attendance_csv import CSVHandler
import json

def register_face(image_path: str, name: str, db: Session):
    # Load the image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face encodings
    face_encodings = face_recognition.face_encodings(rgb_image)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]

        # Save the user details and their face embedding to the database
        user = User(
            name=name,
            facial_embedding=str(face_encoding.tolist())  # Convert the numpy array to a list and store it as a string
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    else:
        # No face detected
        return None


def recognize_face(image_path: str, db: Session):
    # Load image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get face encoding(s) from the input image
    face_encodings = face_recognition.face_encodings(rgb_image)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]  # Consider the first face encoding

        # Fetch all registered users and their embeddings from the database
        users = db.query(User).all()
        recognized_user = None
        min_distance = float("inf")  # Initialize with a large value for comparison

        for user in users:
            # Convert the stored facial embedding string back to a numpy array
            db_encoding = np.array(json.loads(user.facial_embedding))  # Use JSON instead of eval

            # Calculate the Euclidean distance between face encodings
            distance = np.linalg.norm(face_encoding - db_encoding)

            # Check if the distance is below the threshold
            if distance < 0.6:  # 0.6 is the commonly used threshold for face recognition
                if distance < min_distance:  # Find the closest match
                    min_distance = distance
                    recognized_user = user

        if recognized_user:
            # Mark attendance for the recognized user
            CSVHandler.initialize_csv()
            attendance = Attendance(user_id=recognized_user.id)
            db.add(attendance)
            db.commit()
            db.refresh(attendance)

            # Count the user's attendance
            attendance_count = db.query(Attendance).filter(Attendance.user_id == recognized_user.id).count()

            # Save to CSV
            CSVHandler.save_to_csv(
                recognized_user.id,
                recognized_user.name,
                attendance.timestamp,
                attendance_count,
            )

            # Debugging: Confirm recognized user details
            print(f"Recognized User: {recognized_user.name}, Attendance Marked: {attendance.timestamp}")

            return recognized_user, attendance

    # Return None if no match is found
    return None, None


