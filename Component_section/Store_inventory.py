import warnings
from copy import deepcopy

import pandas as pd

warnings.filterwarnings('ignore')


class Store:
    def __init__(self, name, inventory_url):
        self.name = name
        self.inventory_url = inventory_url
        # Initialize _inventory as an empty DataFrame
        self._inventory = pd.DataFrame(columns=['Part Number', 'Description', 'Quantity Available', 'Price'])

    def add_component(self, part_number, description, quantity_available, price):
        new_component = pd.DataFrame({
            'Part Number': [part_number],
            'Description': [description],
            'Quantity Available': [quantity_available],
            'Price': [price]
        })
        self._inventory = pd.concat([self._inventory, new_component], ignore_index=True)

    def save_inventory_to_file(self, file_path: str):
        # Save the DataFrame to a CSV file
        self._inventory.to_csv(file_path, index=False)

    def load_inventory_from_file(self, file_path: str):
        # Load _inventory from a CSV file into the DataFrame
        self._inventory = pd.read_csv(file_path)

    @property
    def inventory(self):
        # return copy of inventory
        return deepcopy(self._inventory)

    def __len__(self):
        # return the number of the components
        return self._inventory.shape[0]

    def __iter__(self) -> dict:
        # runs over the components
        for ind in range(self._inventory.shape[0]):
            yield self._inventory.iloc[ind, :].to_dict()

    def __repr__(self):
        return f"store names: {self.name}"


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

    # len function return the number of components
    print(f"the number of components{len(store_example)}")

    # iterator return dict of single component each iteration
    for i in store_example:
        print(i)

    # Print the inventory DataFrame
    # print(store_example.inventory)
    print(store_example.inventory)
