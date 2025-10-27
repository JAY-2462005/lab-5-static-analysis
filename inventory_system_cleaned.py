"""
A simple inventory management system.

This module allows for adding, removing, and querying items
in a simple in-memory inventory, with options to load from
and save to a JSON file.
"""

import json
import logging
from datetime import datetime

# Module-level variable for inventory.
# pylint: disable=invalid-name
stock_data = {}


def add_item(item, quantity, logs=None):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        item (str): The name of the item to add.
        quantity (int): The number of items to add.
        logs (list, optional): A list to append log messages to.
                              Defaults to None.
    """
    # Fix: Dangerous default value []
    if logs is None:
        logs = []

    # Fix: Implement input validation
    if not isinstance(item, str) or not item:
        logging.warning(
            "Invalid item name provided: %s. Must be a non-empty string.",
            item
        )
        return
    if not isinstance(quantity, int):
        logging.warning(
            "Invalid quantity for %s: %s. Must be an integer.",
            item,
            quantity
        )
        return

    stock_data[item] = stock_data.get(item, 0) + quantity
    # Fix: Use f-string for cleaner formatting
    logs.append(f"{datetime.now()}: Added {quantity} of {item}")
    logging.info("Added %d of %s", quantity, item)
    # Fix: Make all return statements implicit 'None' (R1710)
    return


def remove_item(item, quantity):
    """
    Removes a specified quantity of an item from the stock.

    Args:
        item (str): The name of the item to remove.
        quantity (int): The number of items to remove.
    """
    # Fix: Implement input validation
    if not isinstance(item, str) or not item:
        logging.warning(
            "Invalid item name provided: %s. Must be a non-empty string.",
            item
        )
        return
    if not isinstance(quantity, int):
        logging.warning(
            "Invalid quantity for %s: %s. Must be an integer.",
            item,
            quantity
        )
        return

    try:
        if stock_data[item] - quantity <= 0:
            logging.info(
                "Stock for %s is %d, removing from inventory.",
                item,
                stock_data[item]
            )
            del stock_data[item]
        else:
            stock_data[item] -= quantity
    # Fix: Replace bare 'except:' with specific exception
    except KeyError:
        logging.warning("Attempted to remove item not in stock: %s", item)
    # Fix: Catch a more specific exception than 'Exception' (W0718)
    except TypeError as e:
        logging.error(
            "An unexpected error (TypeError) occurred while removing %s: %s",
            item,
            e
        )


def get_qty(item):
    """
    Gets the current quantity of a specific item.

    Args:
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item in stock, or 0 if not found.
    """
    # Fix: Implement safe dictionary access to prevent KeyError
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads inventory data from a JSON file.

    Args:
        file (str, optional): The filename to load from.
                              Defaults to "inventory.json".
    """
    global stock_data  # pylint: disable=global-statement
    try:
        # Fix: Use 'with' for file handling and add 'encoding'
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Successfully loaded data from %s", file)
    except FileNotFoundError:
        # Fix: Break long line (E501)
        logging.warning(
            "Inventory file %s not found. Starting with empty inventory.",
            file
        )
        stock_data = {}
    except json.JSONDecodeError:
        logging.error(
            "Failed to decode JSON from %s. Starting with empty inventory.",
            file
        )
        stock_data = {}


def save_data(file="inventory.json"):
    """
    Saves the current inventory data to a JSON file.

    Args:
        file (str, optional): The filename to save to.
                              Defaults to "inventory.json".
    """
    try:
        # Fix: Use 'with' for file handling and add 'encoding'
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Successfully saved data to %s", file)
    except IOError as e:
        logging.error("Error saving data to %s: %s", file, e)


def print_data():
    """Prints a report of all items and their quantities."""
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        # Fix: Rename loop variable 'i' to 'item' and use f-string
        for item, quantity in stock_data.items():
            print(f"{item} -> {quantity}")
    print("--------------------\n")


def check_low_items(threshold=5):
    """
    Returns a list of items with stock below the threshold.

    Args:
        threshold (int, optional): The stock level to check against.
                                   Defaults to 5.

    Returns:
        list: A list of item names below the threshold.
    """
    # Fix: Rename 'i' and use a more Pythonic list comprehension
    low_items = [
        item for item, quantity in stock_data.items()
        if quantity < threshold
    ]
    return low_items


def main():
    """Main function to run the inventory system operations."""
    # Fix: Properly configure logging & break long line (E501)
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    logging.info("Starting inventory system...")
    load_data()

    # Fix: Update function calls to snake_case
    add_item("apple", 10)
    add_item("banana", 5)
    # This invalid call will now be handled by validation in add_item
    add_item(123, "ten")
    add_item("banana", -2)  # This will correctly adjust the total

    remove_item("apple", 3)
    # This invalid call will now be handled by the KeyError in remove_item
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    print_data()
    save_data()

    # Fix: Removed dangerous 'eval()' call
    print("System check complete. 'eval' call removed.")
    logging.info("Inventory system operations complete.")


# Fix: Use __name__ == "__main__" block for executable code
if __name__ == "__main__":
    main()
