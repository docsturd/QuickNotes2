import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Create the Patient table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patient (
        ID INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        date_of_birth TEXT,
        gender TEXT,
        patient_id TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        warning TEXT,
        special_notes TEXT
    )
''')

# Create the Exam table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Exam (
        ID INTEGER PRIMARY KEY,
        PatientID INTEGER,
        ExamDate DATE,
        Assessment VARCHAR,
        TreatmentPlan VARCHAR,
        FOREIGN KEY (PatientID) REFERENCES Patient(ID)
    )
''')

# Create the History of Present Complaints table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS HistoryOfPresentComplaints (
        ID INTEGER PRIMARY KEY,
        ExamID INTEGER,
        Complaint VARCHAR,
        FOREIGN KEY (ExamID) REFERENCES Exam(ID)
    )
''')

# Create the DailyNotes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS DailyNotes (
        ID INTEGER PRIMARY KEY,
        PatientID INTEGER,
        Date DATE,
        SubjectiveComplaints TEXT,
        ObjectiveFindings TEXT,
        Assessment TEXT,
        TreatmentProvided TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patient(ID)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
