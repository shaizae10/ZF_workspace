import requests
from pprint import pprint
import pandas as pd

def get_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

def fetch_part_data(part_number, api_key, country_code=None, currencies=None):
    base_url = "https://oemsecretsapi.com/partsearch"
    params = {
        'searchTerm': part_number,
        'apiKey': api_key,
    }
    if country_code:
        params['countryCode'] = country_code
    if currencies:
        params['currency[]'] = ','.join(currencies)

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    elif response.status_code in [400, 401, 404]:
        error_message = f"Error {response.status_code}: {response.json().get('error_message', 'No error message')}"
        pprint(error_message)
        return None
    else:
        error_message = f"Error {response.status_code}: Unexpected error."
        pprint(error_message)
        return None

def extract_prices(prices_dict):
    # Adjust this function to match your actual data structure
    return ", ".join([f"{currency}: {p['unit_price']} for {p['unit_break']} units" for currency, price_list in prices_dict.items() for p in price_list])

# Example usage
api_key_path = 'keys/components_api_key.txt'
api_key = get_api_key(api_key_path)

data = fetch_part_data(
    part_number='LM324N',
    api_key=api_key,
    country_code='IS',
    currencies='ILS'
)

if data:
    parts_data = data.get('stock', [])
    df = pd.DataFrame(parts_data)
    
    # Apply the extraction function to your prices column
    if 'prices' in df.columns:
        df['prices_extracted'] = df['prices'].apply(lambda x: extract_prices(x) if isinstance(x, dict) else None)
        df.drop('prices', axis=1, inplace=True)  # Drop the original prices column if no longer needed

    # Select and reorder main columns
        main_columns = ['manufacturer', 'quantity_in_stock', 'moq', 'prices_extracted', 'distributor']
        df_main = df[main_columns]

        # Save to CSV, keeping only the main columns
        df_main.to_csv('parts_data_main_columns.csv', index=False)
        print("Data with main columns saved to 'parts_data_main_columns.csv'")
