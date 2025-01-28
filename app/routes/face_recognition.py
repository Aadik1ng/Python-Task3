# app/routes/face_recognition.py

from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.face_recognition_service import register_face, recognize_face
import os

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register/")
async def register(file: UploadFile = File(...), name: str = "", db: Session = Depends(get_db)):
    file_location = f"static/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    user = register_face(file_location, name, db)
    if user:
        return {"message": "User registered successfully", "user": user.name}
    else:
        return {"message": "No face detected in the image"}

@router.post("/recognize/")
async def recognize(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"static/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    user, attendance = recognize_face(file_location, db)
    if user:
        return {"message": f"User {user.name} recognized, attendance marked", "attendance": attendance.timestamp}
    else:
        return {"message": "No match found"}
