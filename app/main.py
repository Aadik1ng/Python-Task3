from fastapi import FastAPI,Request
from app.routes.face_recognition import router as face_recognition_router
from app.routes.login import router as login_router  # Import the login router
from app.services.database import init_db
from app.services.attendance_csv import CSVHandler
from app.routes import download_routes
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://python-task3-frontend.vercel.app"],  # You can specify ["http://localhost:3000"] to limit to your React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def redirect_to_https(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url)
    return await call_next(request)


# Initialize database
init_db()
CSVHandler()

# Include the login router for the /api/Login endpoint
app.include_router(login_router, prefix="/api")
app.include_router(download_routes.router, prefix="/attendance")

# Include the face recognition router for the /api/v1 endpoint
app.include_router(face_recognition_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
