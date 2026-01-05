import pandas as pd

def convert_csv_to_json_pandas(csv_file_path, json_file_path):
    """
    Converts a CSV file to a JSON file using the pandas library.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Convert the DataFrame to JSON format and save to a file
        # orient='records' creates a list of JSON objects (one per row)
        df.to_json(json_file_path, orient='records', indent=4)
        
        print(f"Successfully converted {csv_file_path} to {json_file_path} using pandas")
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


