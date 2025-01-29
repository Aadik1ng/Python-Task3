import os
import uuid
from fastapi import UploadFile, HTTPException
from mimetypes import guess_type

# Function to validate image files
def validate_image(file: UploadFile) -> bool:
    mime_type, _ = guess_type(file.filename)
    return mime_type and mime_type.startswith('image')

# Function to save the file securely with a unique filename
def save_file(file: UploadFile, destination_folder: str = 'static') -> str:
    if not validate_image(file):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    
    # Create a unique filename to avoid overwriting
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
    file_location = os.path.join(destination_folder, unique_filename)
    
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_location

# Function to clean up uploaded files after processing
def clean_up_file(file_location: str):
    """Function to delete files after processing"""
    if os.path.exists(file_location):
        os.remove(file_location)
