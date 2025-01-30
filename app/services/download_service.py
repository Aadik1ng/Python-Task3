import os
from fastapi.responses import FileResponse

ATTENDANCE_CSV_FILE = "attendance.csv"

def download_attendance_csv():
    """Returns the generated CSV file as a response if it exists."""
    if not os.path.exists(ATTENDANCE_CSV_FILE):
        return {"error": "Attendance CSV file not found"}
    
    return FileResponse(
        path=ATTENDANCE_CSV_FILE,
        filename="attendance.csv",
        media_type="text/csv"
    )
