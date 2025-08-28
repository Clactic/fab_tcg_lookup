import csv

def convert_csv_to_dict(file_path):
    """
    Converts a CSV file to a list of dictionaries.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        list: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
            "tcgplayerId": row["TCGPlayerId"],
            "condition": row["Condition"],
            "printing": row["Printing"]
        })
    return data
