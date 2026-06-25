import sqlite3
import re

data_file = open("mock_logs.txt")

database_file = sqlite3.connect("log_vault.db")
cursor = database_file.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_vault (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_timestamp TEXT,
            log_status TEXT,
            log_message TEXT
        )
    """)

for line in data_file:
    if "ERROR" in line or "WARNING" in line:
        clean_line = line.strip()

        cursor.execute(
            "INSERT INTO log_vault(log_timestamp, log_status, log_message) VALUES (?, ?, ?)", (clean_line.split(" - ", 2))
        )

database_file.commit()
database_file.close()
