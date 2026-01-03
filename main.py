def main():
    import sys
    try:
        print("="*40)
        print(" " * 10 + "SALES ANALYTICS SYSTEM")
        print("="*40 + "\n")

        # ---------- 1. Read sales data ----------
        print("[1/10] Reading sales data...")
        sales_file = "data/sales_data.txt"  # Adjust path if needed
        raw_lines = read_sales_data(sales_file)
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # ---------- 2. Parse and clean ----------
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records\n")

        # ---------- 3. Display filter options ----------
        print("[3/10] Filter Options Available:")
        available_regions = sorted(set(t["Region"] for t in transactions if t.get("Region")))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        min_amount, max_amount = min(amounts), max(amounts)
        print(f"Regions: {', '.join(available_regions)}")
        print(f"Amount Range: ₹{min_amount:,.0f} - ₹{max_amount:,.0f}\n")

        apply_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        filtered_transactions = transactions
        if apply_filter == "y":
            region_input = input(f"Enter region to filter ({', '.join(available_regions)}): ").strip()
            min_input = input(f"Enter minimum transaction amount (default {min_amount}): ").strip()
            max_input = input(f"Enter maximum transaction amount (default {max_amount}): ").strip()

            min_val = float(min_input) if min_input else None
            max_val = float(max_input) if max_input else None

            filtered_transactions, invalid_count, summary = validate_and_filter(
                transactions,
                region=region_input if region_input else None,
                min_amount=min_val,
                max_amount=max_val
            )
            print(f"✓ Filter applied: {len(filtered_transactions)} records remaining\n")

        # ---------- 4. Validate ----------
        print("[4/10] Validating transactions...")
        valid_transactions, invalid_count, validation_summary = validate_and_filter(filtered_transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}\n")

        # ---------- 5. Perform analytics ----------
        print("[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_transactions)
        region_stats = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        customer_stats = customer_analysis(valid_transactions)
        daily_stats = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)
        print("✓ Analysis complete\n")

        # ---------- 6. Fetch product data ----------
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # ---------- 7. Enrich sales data ----------
        print("[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products)
        enriched_txns = enrich_sales_data(valid_transactions, product_map)
        enriched_count = sum(1 for t in enriched_txns if t.get("API_Match"))
        success_rate = (enriched_count / len(enriched_txns) * 100) if enriched_txns else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_txns)} transactions ({success_rate:.1f}%)\n")

        # ---------- 8. Save enriched data ----------
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_txns)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # ---------- 9. Generate report ----------
        print("[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_txns)
        print("✓ Report saved to: output/sales_report.txt\n")

        # ---------- 10. Complete ----------
        print("[10/10] Process Complete!")
        print("="*40)

    except FileNotFoundError as fe:
        print(f"Error: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
