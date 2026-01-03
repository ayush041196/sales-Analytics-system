#Task 1.1

def read_sales_data (filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """

    encodings_to_try = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings_to_try:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

            # Skip header and remove empty lines
            cleaned_lines = [
                line.strip()
                for line in lines[1:]
                if line.strip()
            ]

            return cleaned_lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    # If no encoding worked
    print("Error: Unable to read file due to encoding issues.")
    return []

#Task 1.2  
def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    parsed_records = []

    for line in raw_lines:
        # Split by pipe delimiter
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()

            # Clean ProductName (remove commas)
            product_name = parts[3].replace(",", "").strip()

            # Clean and convert Quantity
            quantity_str = parts[4].replace(",", "").strip()
            quantity = int(quantity_str)

            # Clean and convert UnitPrice
            unit_price_str = parts[5].replace(",", "").strip()
            unit_price = float(unit_price_str)

            customer_id = parts[6].strip()
            region = parts[7].strip()

            record = {
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            }

            parsed_records.append(record)

        except (ValueError, IndexError):
            # Skip records with conversion or parsing issues
            continue

    return parsed_records

#Task 1.3: 
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Returns:
    (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    # ---------- Pre-validation info ----------
    available_regions = sorted(
        {t.get("Region") for t in transactions if t.get("Region")}
    )

    amounts = [
        t["Quantity"] * t["UnitPrice"]
        for t in transactions
        if isinstance(t.get("Quantity"), int)
        and isinstance(t.get("UnitPrice"), (int, float))
        and t["Quantity"] > 0
        and t["UnitPrice"] > 0
    ]

    if amounts:
        print(f"Available Regions: {available_regions}")
        print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    # ---------- Validation ----------
    for t in transactions:
        try:
            # Required fields
            required_fields = [
                "TransactionID", "Date", "ProductID", "ProductName",
                "Quantity", "UnitPrice", "CustomerID", "Region"
            ]

            if not all(field in t and t[field] for field in required_fields):
                raise ValueError

            if not t["TransactionID"].startswith("T"):
                raise ValueError

            if not t["ProductID"].startswith("P"):
                raise ValueError

            if not t["CustomerID"].startswith("C"):
                raise ValueError

            if t["Quantity"] <= 0 or t["UnitPrice"] <= 0:
                raise ValueError

            valid_transactions.append(t)

        except Exception:
            invalid_count += 1

    # ---------- Filtering ----------
    filtered_by_region = 0
    filtered_by_amount = 0

    filtered_transactions = valid_transactions

    if region:
        before = len(filtered_transactions)
        filtered_transactions = [
            t for t in filtered_transactions if t["Region"] == region
        ]
        filtered_by_region = before - len(filtered_transactions)
        print(f"Records after region filter ({region}): {len(filtered_transactions)}")

    if min_amount is not None or max_amount is not None:
        before = len(filtered_transactions)

        def amount_in_range(t):
            amount = t["Quantity"] * t["UnitPrice"]
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True

        filtered_transactions = [
            t for t in filtered_transactions if amount_in_range(t)
        ]
        filtered_by_amount = before - len(filtered_transactions)
        print(f"Records after amount filter: {len(filtered_transactions)}")

    # ---------- Summary ----------
    filter_summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered_transactions)
    }

    return filtered_transactions, invalid_count, filter_summary
