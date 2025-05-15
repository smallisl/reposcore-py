from datetime import datetime
import sys

def parse_semester_start(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Invalid semester_start date format. Expected YYYY-MM-DD.")
        sys.exit(1)
