data_file = open("mock_logs.txt")
for line in data_file:
    if "ERROR" in line or "WARNING" in line:
        print(line)