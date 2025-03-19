import csv
import os
import datetime

def ensure_file_exists(filename, headers):
    """Create the file with headers if it doesn't exist"""
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def save_data(candidate_data):
    """Save candidate data to a CSV file."""
    # Define headers
    headers = ["full_name", "email", "phone", "experience", "position", "location", "tech_stack", "timestamp"]
    
    # Ensure the file exists
    filename = 'candidates.csv'
    ensure_file_exists(filename, headers)
    
    # Add timestamp
    candidate_data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write data
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(candidate_data)

def save_report(report):
    """Save the report to a CSV file."""
    # Generate a unique filename with candidate info if available
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'report_{timestamp}.csv'
    
    # Headers for the report
    headers = ["question", "answer", "correct"]
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in report:
            writer.writerow(row)
            
    return filename   