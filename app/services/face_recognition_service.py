# app/services/face_recognition_service.py

import face_recognition
import cv2
import numpy as np
from sqlalchemy.orm import Session
from app.services.database import User, Attendance
from app.services.attendance_csv import CSVHandler
import json
import redis
import hashlib
import cv2
import face_recognition
import redis
import json
import os


REDIS_URL = os.getenv("REDIS_URL")  # Fetch Redis URL from env variable

def register_face(image_path: str, name: str, password: str, db: Session):
    """
    Registers a new face with a given name and password, and stores its encoding in Redis and User data in the DB.
    """
    # Validate input fields
    if not name or not password:
        raise ValueError("Name and password cannot be empty.")

    # Hash the password before storing it for security
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Load the image and convert it to RGB
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face encodings
    face_encodings = face_recognition.face_encodings(rgb_image)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]

        # Save user details in the database with hashed password
        user = User(name=name, password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)

        # Store the face encoding in Redis (as a JSON array)
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)



        # redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.set(user.name, json.dumps(face_encoding.tolist()))

        print(f"User {name} registered successfully.")
        return user
    else:
        print("No face detected.")
        return None

def recognize_face(image_path: str,db: Session): 
    # Load image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    # Get face encoding(s) from the input image
    face_encodings = face_recognition.face_encodings(rgb_image)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[0]  # Consider the first face encoding

        # Fetch all registered users and their embeddings from Redis
        recognized_user_name = None
        min_distance = float("inf")  # Initialize with a large value for comparison

        for key in redis_client.keys():
            user_name = key
            db_encoding = np.array(json.loads(redis_client.get(key)))

            # Calculate the Euclidean distance between face encodings
            distance = np.linalg.norm(face_encoding - db_encoding)

            # Check if the distance is below the threshold
            if distance < 0.6:  # 0.6 is the commonly used threshold for face recognition
                if distance < min_distance:  # Find the closest match
                    min_distance = distance
                    recognized_user_name = user_name

        if recognized_user_name:
            # Fetch user details from the traditional database
            recognized_user = db.query(User).filter(User.name == recognized_user_name).first()
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