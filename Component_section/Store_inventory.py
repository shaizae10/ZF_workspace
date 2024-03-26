import pandas as pd


class Store:
    def __init__(self, name, inventory_url):
        self.name = name
        self.inventory_url = inventory_url
        # Initialize inventory as an empty DataFrame
        self.inventory = pd.DataFrame(columns=['Part Number', 'Description', 'Quantity Available', 'Price'])

    def add_component(self, part_number, description, quantity_available, price):
        # Ensure self.inventory is a DataFrame
        if not isinstance(self.inventory, pd.DataFrame):
            raise TypeError("self.inventory is not a pandas DataFrame.")

        new_component = pd.DataFrame({
            'Part Number': [part_number],
            'Description': [description],
            'Quantity Available': [quantity_available],
            'Price': [price]
        })
        self.inventory = pd.concat([self.inventory, new_component], ignore_index=True)

    def save_inventory_to_file(self, file_path):
        # Save the DataFrame to a CSV file
        self.inventory.to_csv(file_path, index=False)

    def load_inventory_from_file(self, file_path):
        # Load inventory from a CSV file into the DataFrame
        self.inventory = pd.read_csv(file_path)


# Example usage
if __name__ == '__main__':
    store_example = Store("Example Store", "https://example.com/inventory")

    # Adding some components for demonstration
    store_example.add_component('123-456', 'Resistor 10k Ohm', 100, 0.10)
    store_example.add_component('789-012', 'Capacitor 100uF', 50, 0.20)

    # Save to CSV file
    store_example.save_inventory_to_file('example_store_inventory.csv')

    # Load from CSV file
    store_example.load_inventory_from_file('example_store_inventory.csv')

    # Print the inventory DataFrame
    print(store_example.inventory)
