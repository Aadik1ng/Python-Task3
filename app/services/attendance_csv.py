import csv
import os

# Path to the CSV file
ATTENDANCE_CSV_FILE = "attendance.csv"

class CSVHandler:
    @staticmethod
    def initialize_csv():
        """
        Ensures the CSV file exists and has the correct headers.
        If the file exists but lacks headers, headers are added.
        """
        if not os.path.exists(ATTENDANCE_CSV_FILE):
            print("CSV file not found. Creating file with headers.")
            # Create the file with headers if it doesn't exist
            with open(ATTENDANCE_CSV_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["User ID", "Name", "Timestamp", "Attendance Count"])
        else:
            print("CSV file found. Checking headers...")
            # Check if headers exist in the file
            with open(ATTENDANCE_CSV_FILE, mode="r", newline="") as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # Read the first row
                if headers != ["User ID", "Name", "Timestamp", "Attendance Count"]:
                    print("Headers are missing or incorrect. Rewriting headers.")
                    # Rewrite headers if missing or incorrect
                    with open(ATTENDANCE_CSV_FILE, mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(["User ID", "Name", "Timestamp", "Attendance Count"])
                else:
                    print("Headers are correct.")

    @staticmethod
    def save_to_csv(user_id: int, name: str, timestamp: str, attendance_count: int = 1):
        """
        Updates an existing attendance record by incrementing the count,
        or appends a new record if the user does not exist.
        """
        records = []
        user_found = False

        # Read existing data from the CSV
        if os.path.exists(ATTENDANCE_CSV_FILE):
            with open(ATTENDANCE_CSV_FILE, mode="r", newline="") as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # Skip the headers
                for row in reader:
                    if int(row[0]) == user_id:  # If the User ID matches
                        user_found = True
                        row[2] = timestamp  # Update the timestamp
                        row[3] = str(int(row[3]) + 1)  # Increment the attendance count
                    records.append(row)

        # If the user was not found, add a new record
        if not user_found:
            print(f"User ID {user_id} not found. Adding new record.")
            records.append([user_id, name, timestamp, attendance_count])

        # Write all records back to the CSV
        with open(ATTENDANCE_CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User ID", "Name", "Timestamp", "Attendance Count"])  # Write headers
            writer.writerows(records)  # Write the updated records

        if user_found:
            print(f"User ID {user_id} found. Attendance count updated.")
        else:
            print(f"New record added for User ID {user_id}.")
