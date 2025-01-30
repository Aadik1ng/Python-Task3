from fastapi import APIRouter
from services.download_service import download_attendance_csv

router = APIRouter()

@router.get("/download-csv")
def download_csv():
    return download_attendance_csv()
