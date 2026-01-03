Task 3.1 
A)
import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    url = "https://dummyjson.com/products"
    params = {"limit": 100}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f"Successfully fetched {len(products)} products.")
        return products

    except requests.exceptions.RequestException as e:
        print("Failed to fetch products from DummyJSON API.")
        print(f"Error: {e}")
        return []

B)
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters:
    - api_products: list of product dictionaries from fetch_all_products()

    Returns: dictionary mapping product IDs to product info
    """

    product_mapping = {}

    for product in api_products:
        try:
            product_id = product.get("id")

            if product_id is None:
                continue

            product_mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

        except AttributeError:
            # Skip malformed product entries
            continue

    return product_mapping

Task 3.2

import os

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns: list of enriched transaction dictionaries
    """

    enriched_transactions = []

    # Ensure output directory exists
    os.makedirs("data", exist_ok=True)
    output_file = "data/enriched_sales_data.txt"

    # Define new header including API fields
    header_fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    # ---------- Enrich each transaction ----------
    for t in transactions:
        enriched = t.copy()

        try:
            # Extract numeric ID from ProductID (P101 → 101)
            product_id_str = t.get("ProductID", "")
            numeric_id = int("".join(filter(str.isdigit, product_id_str)))

            api_info = product_mapping.get(numeric_id)

            if api_info:
                enriched["API_Category"] = api_info.get("category")
                enriched["API_Brand"] = api_info.get("brand")
                enriched["API_Rating"] = api_info.get("rating")
                enriched["API_Match"] = True
            else:
                # No match
                enriched["API_Category"] = None
                enriched["API_Brand"] = None
                enriched["API_Rating"] = None
                enriched["API_Match"] = False

        except Exception:
            # On any error, mark as no match
            enriched["API_Category"] = None
            enriched["API_Brand"] = None
            enriched["API_Rating"] = None
            enriched["API_Match"] = False

        enriched_transactions.append(enriched)

    # ---------- Save to pipe-delimited file ----------
    with open(output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write("|".join(header_fields) + "\n")

        # Write records
        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")),
                str(t.get("Quantity", "")),
                str(t.get("UnitPrice", "")),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category", "")),
                str(t.get("API_Brand", "")),
                str(t.get("API_Rating", "")),
                str(t.get("API_Match", ""))
            ]
            f.write("|".join(row) + "\n")

    print(f"Enriched sales data saved to '{output_file}'")
    return enriched_transactions

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Define full header including new API fields
    header_fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    try:
        with open(filename, "w", encoding="utf-8") as f:
            # Write header
            f.write("|".join(header_fields) + "\n")

            # Write each enriched transaction
            for t in enriched_transactions:
                row = []
                for field in header_fields:
                    value = t.get(field, "")
                    if value is None:
                        value = ""
                    row.append(str(value))
                f.write("|".join(row) + "\n")

        print(f"Enriched transactions successfully saved to '{filename}'.")

    except Exception as e:
        print(f"Error saving enriched data: {e}")
