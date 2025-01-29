from fastapi import FastAPI
from app.routes.face_recognition import router as face_recognition_router
from app.routes.login import router as login_router  # Import the login router
from app.services.database import init_db
from app.services.attendance_csv import CSVHandler

app = FastAPI()

# Initialize database
init_db()
CSVHandler()

# Include the login router for the /api/Login endpoint
app.include_router(login_router, prefix="/api")

# Include the face recognition router for the /api/v1 endpoint
app.include_router(face_recognition_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
