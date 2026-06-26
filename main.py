import sqlite3


def process_and_analyze_logs(log_file_path, db_file_path):
    """Streams logs into a SQLite database and prints hourly analytics."""

    # 1. Initialize Database Connection and Schema
    database_file = sqlite3.connect(db_file_path)
    cursor = database_file.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS log_vault (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_timestamp TEXT,
            log_status TEXT,
            log_message TEXT
        )
    """
    )

    # 2. Parse and Insert Log Streams Safely
    with open(log_file_path, "r") as data_file:
        for line in data_file:
            if "ERROR" in line or "WARNING" in line:
                clean_line = line.strip()

                cursor.execute(
                    "INSERT INTO log_vault(log_timestamp, log_status, log_message) VALUES (?, ?, ?)",
                    clean_line.split(" - ", 2),
                )

    # Commit insertions before querying
    database_file.commit()

    # 3. Aggregate Metrics Using SQL Analytics
    cursor.execute(
        """
        SELECT 
            SUBSTR(log_timestamp, 12, 2) AS hour_of_day,
            log_status,
            COUNT(*) AS total_incidents
        FROM log_vault
        GROUP BY hour_of_day, log_status
        ORDER BY hour_of_day ASC;
    """
    )

    results = cursor.fetchall()

    # 4. Format and Display Reports
    print(f"{'Hour':<8} | {'Status':<10} | {'Total Incidents'}")
    print("-" * 35)

    for row in results:
        raw_hour = int(row[0])  # Convert string hours (e.g., '08') to integers

        # Map 24-hour integers to AM/PM human-readable formats
        if raw_hour == 0:
            display_hour = "12 AM"
        elif raw_hour == 12:
            display_hour = "12 PM"
        elif raw_hour > 12:
            display_hour = f"{raw_hour - 12} PM"
        else:
            display_hour = f"{raw_hour} AM"

        print(f"{display_hour:<8} | {row[1]:<10} | {row[2]}")

    # Clean up connections
    database_file.close()


if __name__ == "__main__":
    # Define file configurations and execute the pipeline
    LOG_FILE = "mock_logs.txt"
    DB_FILE = "log_vault.db"

    process_and_analyze_logs(LOG_FILE, DB_FILE)
