import pandas as pd
import json

def convert_excel_to_json(excel_file, json_output):
    # Load the excel file
    df = pd.read_excel(excel_file)
    
    # Convert dataframe to a list of dictionaries
    data = df.to_dict(orient='records')
    
    # Save as JSON
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully converted {excel_file} to {json_output}")

# Usage
convert_excel_to_json('metadata.xlsx', 'metadata.json')