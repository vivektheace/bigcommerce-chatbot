import json
import os

CUSTOMER_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/mock_customers/customers.json"))

def load_customers():
    with open(CUSTOMER_DB_PATH, "r") as f:
        return json.load(f)

# Load customers immediately when this module is imported
customers = load_customers()
