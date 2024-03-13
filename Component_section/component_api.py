import requests
import pandas as pd
from requests.exceptions import HTTPError


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

    try:
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        return response.json()
    except HTTPError as http_err:
        # Specific HTTP status code errors can be handled here if needed
        error_message = response.json().get('error_message', 'No error message available')
        # Raise a new exception with a more descriptive error message
        raise Exception(f"HTTP error occurred: {http_err}. Error message: {error_message}") from http_err
    except Exception as err:
        # Handle other possible exceptions (e.g., network issues, JSON decode error)
        raise Exception(f"An error occurred: {err}") from err


def extract_prices(prices_dict):
    # Adjust this function to match your actual data structure
    return ", ".join(
        [f"{currency}: {p['unit_price']} for {p['unit_break']} units" for currency, price_list in prices_dict.items()
         for p in price_list])


if __name__ == "__main__":
    # Example usage
    api_key_path = '../keys/components_api_key.txt'
    api_key = get_api_key(api_key_path)

    data = fetch_part_data(
        part_number='LM324N',
        api_key=api_key,
        country_code='IS',
        currencies=['ILS']  # currencies should be passed as a list
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
