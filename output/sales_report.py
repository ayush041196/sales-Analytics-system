import os
from datetime import datetime

def generate_sales_report(
    transactions,
    enriched_transactions,
    output_file='output/sales_report.txt'
):
    """
    Generates a comprehensive formatted text report summarizing sales analytics.

    Parameters:
    - transactions: list of validated transaction dicts
    - enriched_transactions: list of enriched transactions with API fields
    - output_file: path to save the report
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # ---------- Overall Summary ----------
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0.0

    dates = [t['Date'] for t in transactions if t.get('Date')]
    date_range = (min(dates), max(dates)) if dates else ("N/A", "N/A")

    # ---------- Region-wise Performance ----------
    from collections import defaultdict
    region_stats = defaultdict(lambda: {"sales":0.0, "count":0})
    for t in transactions:
        r = t.get("Region")
        if not r: continue
        region_stats[r]["sales"] += t["Quantity"] * t["UnitPrice"]
        region_stats[r]["count"] += 1
    total_sales_all_regions = sum(s["sales"] for s in region_stats.values())
    # Sort descending by sales
    sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]["sales"], reverse=True)

    # ---------- Top 5 Products ----------
    from collections import Counter
    product_counter = defaultdict(lambda: {"quantity":0, "revenue":0.0})
    for t in transactions:
        pname = t.get("ProductName")
        if not pname: continue
        product_counter[pname]["quantity"] += t["Quantity"]
        product_counter[pname]["revenue"] += t["Quantity"] * t["UnitPrice"]
    top_products = sorted(product_counter.items(), key=lambda x: x[1]["quantity"], reverse=True)[:5]

    # ---------- Top 5 Customers ----------
    customer_counter = defaultdict(lambda: {"spent":0.0, "orders":0})
    for t in transactions:
        cid = t.get("CustomerID")
        if not cid: continue
        customer_counter[cid]["spent"] += t["Quantity"] * t["UnitPrice"]
        customer_counter[cid]["orders"] += 1
    top_customers = sorted(customer_counter.items(), key=lambda x: x[1]["spent"], reverse=True)[:5]

    # ---------- Daily Sales Trend ----------
    daily_stats = defaultdict(lambda: {"revenue":0.0, "transactions":0, "unique_customers":set()})
    for t in transactions:
        d = t.get("Date")
        if not d: continue
        daily_stats[d]["revenue"] += t["Quantity"] * t["UnitPrice"]
        daily_stats[d]["transactions"] += 1
        daily_stats[d]["unique_customers"].add(t.get("CustomerID"))
    sorted_daily = sorted(daily_stats.items())

    # ---------- Product Performance ----------
    # Peak day
    peak_day = max(daily_stats.items(), key=lambda x: x[1]["revenue"], default=(None, None))
    # Low-performing products (<10 units)
    low_products = [(p, v["quantity"], v["revenue"]) for p,v in product_counter.items() if v["quantity"]<10]
    low_products_sorted = sorted(low_products, key=lambda x: x[1])

    # Average transaction value per region
    avg_txn_region = {r: round(v["sales"]/v["count"],2) if v["count"] else 0.0 for r,v in region_stats.items()}

    # ---------- API Enrichment Summary ----------
    total_enriched = sum(1 for t in enriched_transactions if t.get("API_Match"))
    success_rate = (total_enriched / len(enriched_transactions) * 100) if enriched_transactions else 0
    not_enriched = [t.get("ProductName") for t in enriched_transactions if not t.get("API_Match")]

    # ---------- Write Report ----------
    with open(output_file, "w", encoding="utf-8") as f:
        # HEADER
        f.write("="*50 + "\n")
        f.write(" "*10 + "SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n")
        f.write("="*50 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range[0]} to {date_range[1]}\n\n")

        # REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>12}{'Transactions':>15}\n")
        for r, stats in sorted_regions:
            percent = (stats["sales"]/total_sales_all_regions*100) if total_sales_all_regions else 0
            f.write(f"{r:<10}₹{stats['sales']:>14,.2f}{percent:>11.2f}%{stats['count']:>15}\n")
        f.write("\n")

        # TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Rank':<5}{'Product Name':<25}{'Quantity':>10}{'Revenue':>15}\n")
        for i,(p,v) in enumerate(top_products,1):
            f.write(f"{i:<5}{p:<25}{v['quantity']:>10}₹{v['revenue']:>14,.2f}\n")
        f.write("\n")

        # TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Rank':<5}{'CustomerID':<15}{'Total Spent':>15}{'Orders':>10}\n")
        for i,(c,v) in enumerate(top_customers,1):
            f.write(f"{i:<5}{c:<15}₹{v['spent']:>14,.2f}{v['orders']:>10}\n")
        f.write("\n")

        # DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Transactions':>15}{'Unique Customers':>20}\n")
        for date, stats in sorted_daily:
            f.write(f"{date:<12}₹{stats['revenue']:>14,.2f}{stats['transactions']:>15}{len(stats['unique_customers']):>20}\n")
        f.write("\n")

        # PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-"*50 + "\n")
        peak_date, peak_info = peak_day
        peak_revenue = peak_info["revenue"] if peak_info else 0
        peak_txns = peak_info["transactions"] if peak_info else 0
        f.write(f"Best Selling Day: {peak_date} - Revenue: ₹{peak_revenue:,.2f} ({peak_txns} transactions)\n")

        if low_products_sorted:
            f.write("Low Performing Products:\n")
            for p, q, r in low_products_sorted:
                f.write(f"  {p:<20} Quantity: {q:<5} Revenue: ₹{r:,.2f}\n")
        else:
            f.write("No low performing products.\n")

        f.write("Average Transaction Value per Region:\n")
        for r, avg in avg_txn_region.items():
            f.write(f"  {r}: ₹{avg:,.2f}\n")
        f.write("\n")

        # API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Products Enriched: {total_enriched}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        if not_enriched:
            f.write("Products Not Enriched: " + ", ".join(not_enriched) + "\n")
        else:
            f.write("All products enriched successfully.\n")

    print(f"Sales report generated: '{output_file}'")
