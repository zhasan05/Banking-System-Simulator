import json
import os
from bank import Bank

# default path where account data is saved between executions
DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "accounts.json")

# creates data/ folder if missing, converts bank to dict, writes to JSON file
def save_accounts(bank: Bank, filepath: str = DEFAULT_DATA_PATH) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    data = bank.to_dict() # convert Bank object to plain dictionary
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

# returns fresh Bank if no save file exists, otherwise reads JSON and rebuilds Bank
def load_accounts(filepath: str = DEFAULT_DATA_PATH) -> Bank:
    if not os.path.exists(filepath):
        return Bank()
    else:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return Bank.from_dict(data) # convert plain dictionary to Bank object