import sqlite3
from datetime import datetime

# SQLite Database connection
def create_connection():
    conn = sqlite3.connect('attendance.db')
    return conn

def mark_attendance(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    return f"Attendance marked for User ID {user_id}"

def get_attendance_report():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT users.name, attendance.timestamp
        FROM attendance
        JOIN users ON attendance.user_id = users.id
    ''')
    records = cursor.fetchall()
    conn.close()
    return records
