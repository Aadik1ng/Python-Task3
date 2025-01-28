# app/main.py

from fastapi import FastAPI
from app.routes.face_recognition import router as face_recognition_router
from app.database import init_db
from app.services.attendance_csv import CSVHandler

app = FastAPI()

# Initialize database
init_db()
CSVHandler()
app.include_router(face_recognition_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
