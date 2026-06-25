import sqlite3
import re

data_file = open("mock_logs.txt")
for line in data_file:
    if "ERROR" in line or "WARNING" in line:
        print(line)

database_file = sqlite3.connect("log_vault.db")
cursor = database_file.cursor()
cursor.execute(
    "CREATE TABLE log_vault (" \
    " log_id INT AUTO_INCREMENT PRIMARY KEY," \
    " log_timestamp VARCHAR(23)," \
    " log_status VARCHAR(10)," \
    " log_message VARCHAR(100)" \
    ")"
    )

