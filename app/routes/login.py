from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.database import get_db  # Database dependency
from app.services.auth import create_access_token, verify_password, get_user, hash_password  # Your JWT utilities
from app.models.user import User, LoginRequest, RegisterRequest  # Assuming User is your User model
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = get_user(db, request.name)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password
    hashed_password = hash_password(request.password)
    
    # Create a new user
    new_user = User(name=request.name, password=hashed_password)
    
    # Save the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user": new_user.name}

@router.post("/token")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Handle user login
    user = get_user(db, request.name)
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
