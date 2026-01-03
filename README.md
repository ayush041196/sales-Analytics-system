Overview
This project processes sales transactions, cleans and validates the data, enriches it with product information from an API, performs detailed sales analysis, and generates a comprehensive report.
Key Features:
•	Read and clean raw sales data (handling encoding issues)
•	Parse, validate, and optionally filter transactions
•	Calculate revenue, top products, customer stats, region-wise performance, and daily trends
•	Fetch product data from DummyJSON API and enrich transactions
•	Save enriched data to a file
•	Generate a detailed text report summarizing all analytics

Project Structure

project_root/
│
├── data/
│   └── sales_data.txt               # Raw sales data file (pipe-delimited)
│
├── output/
│   └── sales_report.txt             # Generated analytics report
│
├── main.py                          # Main execution script
├── sales_functions.py               # All helper functions:
│   - read_sales_data
│   - parse_transactions
│   - validate_and_filter
│   - calculate_total_revenue
│   - region_wise_sales
│   - top_selling_products
│   - customer_analysis
│   - daily_sales_trend
│   - find_peak_sales_day
│   - low_performing_products
│   - fetch_all_products
│   - create_product_mapping
│   - enrich_sales_data
│   - save_enriched_data
│   - generate_sales_report
│
└── README.md                        # This file


Dependencies
•	Python 3.8 or above
•	Required libraries:
o	requests (for API access)
o	datetime
o	collections
o	os
•	Install dependencies using:
pip install requests


Input Data
•	Raw sales transactions file: data/sales_data.txt
•	Format: Pipe-delimited (|) with columns:
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
T001|2024-12-01|P101|Laptop|2|45000|C001|North
...
•	Ensure this file is present in the data/ directory.

How to Run
1.	Clone or download the repository into your local machine.
2.	Place your raw sales data file in the data/ folder (sales_data.txt).
3.	Run the main script:
python main.py
4.	Follow prompts (optional filtering):
o	You will see available regions and transaction amount ranges.
o	You can choose to filter transactions by region or amount, or skip filtering.
5.	Wait for pipeline to complete:
The console will display step-by-step progress:
[1/10] Reading sales data...
[2/10] Parsing and cleaning data...
[3/10] Filter Options Available...
[4/10] Validating transactions...
[5/10] Analyzing sales data...
[6/10] Fetching product data from API...
[7/10] Enriching sales data...
[8/10] Saving enriched data...
[9/10] Generating report...
[10/10] Process Complete!


Output Files
1.	Enriched sales data:
data/enriched_sales_data.txt
•	Pipe-delimited file containing original transaction fields + API enrichment fields:
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
...
2.	Comprehensive sales report:
output/sales_report.txt
•	Human-readable text report including:
o	Overall revenue summary
o	Region-wise performance
o	Top products and customers
o	Daily sales trends
o	Product performance analysis
o	API enrichment summary

