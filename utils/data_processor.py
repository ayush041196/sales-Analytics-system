Task 2.1
a.
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """

    total_revenue = 0.0

    for t in transactions:
        try:
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if quantity > 0 and unit_price > 0:
                total_revenue += quantity * unit_price

        except (TypeError, ValueError):
            # Skip malformed records safely
            continue

    return total_revenue

b. 
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """

    region_stats = {}
    total_sales_all_regions = 0.0

    # ---------- Aggregate sales and counts ----------
    for t in transactions:
        try:
            region = t.get("Region")
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if not region or quantity <= 0 or unit_price <= 0:
                continue

            sale_amount = quantity * unit_price
            total_sales_all_regions += sale_amount

            if region not in region_stats:
                region_stats[region] = {
                    "total_sales": 0.0,
                    "transaction_count": 0
                }

            region_stats[region]["total_sales"] += sale_amount
            region_stats[region]["transaction_count"] += 1

        except (TypeError, ValueError):
            continue

    # ---------- Calculate percentage contribution ----------
    for region, stats in region_stats.items():
        if total_sales_all_regions > 0:
            stats["percentage"] = round(
                (stats["total_sales"] / total_sales_all_regions) * 100, 2
            )
        else:
            stats["percentage"] = 0.0

    # ---------- Sort by total_sales (descending) ----------
    sorted_region_stats = dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_stats

c. 
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples:
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_stats = {}

    # ---------- Aggregate quantity and revenue by product ----------
    for t in transactions:
        try:
            product = t.get("ProductName")
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if not product or quantity <= 0 or unit_price <= 0:
                continue

            revenue = quantity * unit_price

            if product not in product_stats:
                product_stats[product] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_stats[product]["total_quantity"] += quantity
            product_stats[product]["total_revenue"] += revenue

        except (TypeError, ValueError):
            continue

    # ---------- Sort by total quantity (descending) ----------
    sorted_products = sorted(
        product_stats.items(),
        key=lambda item: item[1]["total_quantity"],
        reverse=True
    )

    # ---------- Return top n ----------
    top_n = [
        (
            product,
            stats["total_quantity"],
            round(stats["total_revenue"], 2)
        )
        for product, stats in sorted_products[:n]
    ]

    return top_n

d. 
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics sorted by total_spent descending
    """

    customer_stats = {}

    # ---------- Aggregate per customer ----------
    for t in transactions:
        try:
            customer_id = t.get("CustomerID")
            product = t.get("ProductName")
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if not customer_id or quantity <= 0 or unit_price <= 0:
                continue

            amount = quantity * unit_price

            if customer_id not in customer_stats:
                customer_stats[customer_id] = {
                    "total_spent": 0.0,
                    "purchase_count": 0,
                    "products_bought": set()
                }

            customer_stats[customer_id]["total_spent"] += amount
            customer_stats[customer_id]["purchase_count"] += 1
            customer_stats[customer_id]["products_bought"].add(product)

        except (TypeError, ValueError):
            continue

    # ---------- Final calculations ----------
    for customer_id, stats in customer_stats.items():
        if stats["purchase_count"] > 0:
            stats["avg_order_value"] = round(
                stats["total_spent"] / stats["purchase_count"], 2
            )
        else:
            stats["avg_order_value"] = 0.0

        # Convert set to sorted list
        stats["products_bought"] = sorted(stats["products_bought"])

        # Round total_spent
        stats["total_spent"] = round(stats["total_spent"], 2)

    # ---------- Sort by total_spent (descending) ----------
    sorted_customers = dict(
        sorted(
            customer_stats.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers

Task 2.2
a.
from collections import defaultdict

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    daily_stats = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0,
        "unique_customers": set()
    })

    # ---------- Aggregate per day ----------
    for t in transactions:
        try:
            date = t.get("Date")
            customer_id = t.get("CustomerID")
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if not date or not customer_id or quantity <= 0 or unit_price <= 0:
                continue

            amount = quantity * unit_price

            daily_stats[date]["revenue"] += amount
            daily_stats[date]["transaction_count"] += 1
            daily_stats[date]["unique_customers"].add(customer_id)

        except (TypeError, ValueError):
            continue

    # ---------- Finalize unique customer counts ----------
    for date, stats in daily_stats.items():
        stats["revenue"] = round(stats["revenue"], 2)
        stats["unique_customers"] = len(stats["unique_customers"])

    # ---------- Sort chronologically ----------
    sorted_daily_stats = dict(
        sorted(daily_stats.items(), key=lambda item: item[0])
    )

    return sorted_daily_stats

b.
from collections import defaultdict

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    daily_totals = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0
    })

    # ---------- Aggregate revenue per day ----------
    for t in transactions:
        try:
            date = t.get("Date")
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if not date or quantity <= 0 or unit_price <= 0:
                continue

            daily_totals[date]["revenue"] += quantity * unit_price
            daily_totals[date]["transaction_count"] += 1

        except (TypeError, ValueError):
            continue

    # ---------- Find peak day ----------
    peak_date = None
    peak_revenue = 0.0
    peak_txn_count = 0

    for date, stats in daily_totals.items():
        if stats["revenue"] > peak_revenue:
            peak_revenue = stats["revenue"]
            peak_date = date
            peak_txn_count = stats["transaction_count"]

    return (
        peak_date,
        round(peak_revenue, 2),
        peak_txn_count
    )

Task 2.3
a.
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples:
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_stats = {}

    # ---------- Aggregate quantity and revenue by product ----------
    for t in transactions:
        try:
            product = t.get("ProductName")
            quantity = t.get("Quantity", 0)
            unit_price = t.get("UnitPrice", 0.0)

            if not product or quantity <= 0 or unit_price <= 0:
                continue

            revenue = quantity * unit_price

            if product not in product_stats:
                product_stats[product] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            product_stats[product]["total_quantity"] += quantity
            product_stats[product]["total_revenue"] += revenue

        except (TypeError, ValueError):
            continue

    # ---------- Filter low-performing products ----------
    low_products = [
        (
            product,
            stats["total_quantity"],
            round(stats["total_revenue"], 2)
        )
        for product, stats in product_stats.items()
        if stats["total_quantity"] < threshold
    ]

    # ---------- Sort by TotalQuantity ascending ----------
    low_products_sorted = sorted(
        low_products,
        key=lambda item: item[1]
    )

    return low_products_sorted



