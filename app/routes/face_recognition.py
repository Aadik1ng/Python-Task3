from fastapi import APIRouter, File, UploadFile, HTTPException, Depends,Form
from sqlalchemy.orm import Session
from app.services.auth import verify_token  # Import the JWT verification method
from app.services.utils import save_file, clean_up_file  # Import file handling utility functions
from app.services.database import get_db  # Assuming this is where your DB session comes from
from app.services.face_recognition_service import register_face, recognize_face  # Assuming these are your functions

router = APIRouter()

# Helper function to validate the file (example for image types)
def validate_file(file: UploadFile):
    valid_mime_types = ["image/jpeg", "image/png"]
    if file.content_type not in valid_mime_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG images are allowed.")
    return True
@router.post("/register/")
async def register(
    file: UploadFile = File(...),  # Expecting file as form data
    name: str = Form(...),  # Expecting 'name' as form data
    password: str = Form(...),  # Expecting 'password' as form data
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    try:
        # Validate the file type
        validate_file(file)
        
        # Save the file securely
        file_location = save_file(file)
        
        # Ensure password is provided
        if not password:
            raise HTTPException(status_code=400, detail="Password is required for registration.")
        
        # Register the user with the face data
        user = register_face(file_location, name, password, db)
        
        # Clean up the file after processing
        clean_up_file(file_location)
        
        if user:
            return {"message": "User registered successfully", "user": user.name}
        else:
            raise HTTPException(status_code=400, detail="No face detected in the image")
    
    except HTTPException as http_error:
        raise http_error  # Re-raise HTTPException to maintain proper status codes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
@router.post("/recognize/")
async def recognize(file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(verify_token)):
    try:
        # Validate the file type
        validate_file(file)
        
        # Save the file securely
        file_location = save_file(file)
        
        # Recognize the face and mark attendance
        user, attendance = recognize_face(file_location, db)
        
        # Clean up the file after processing
        clean_up_file(file_location)
        
        if user:
            return {"message": f"User {user.name} recognized, attendance marked", "attendance": attendance.timestamp}
        else:
            raise HTTPException(status_code=400, detail="No match found")
    
    except HTTPException as http_error:
        raise http_error  # Re-raise HTTPException to maintain proper status codes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the file: {str(e)}")
