import csv


def save_to_csv_for_google_sheets(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            # writer.writerow(["Module Name", "Module URL", "Repository URL", "License URL", "License Info"])
            writer.writerow(["Module Name", "Module URL", "License URL", "License Info"])
            writer.writerows(data)
        print(f"Dependencies successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")