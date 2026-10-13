"""Generate a synthetic beverage dataset with the same columns as the real one.

The values are random and independent of each other (a smoothie can contain
cola), so the output is only useful for testing the Power BI report and the
HTML preview. Do not use it for analysis.

Usage:  python Scripts/dummy_data_generator.py
Output: Data/sample/beverages_data_synthetic.csv
Requires: pandas
"""
import random
from pathlib import Path

import pandas as pd

ROWS = 1000
random.seed(42)  # same output on every run

OUT = Path(__file__).resolve().parent.parent / "Data" / "sample" / "beverages_data_synthetic.csv"

# Beverage categories, beverages, and preparations to randomize
beverage_categories = ['Tea', 'Smoothie', 'Soda', 'Coffee', 'Juice']
beverages = ['Orange Juice', 'Mango Smoothie', 'Espresso', 'Green Tea', 'Cola', 'Latte', 'Lemonade', 'Iced Tea']
beverage_preps = ['Hot', 'Iced', 'Blended']

# Generate the dummy data
data = {
    "Beverage_category": [random.choice(beverage_categories) for _ in range(ROWS)],
    "Beverage": [random.choice(beverages) for _ in range(ROWS)],
    "Beverage_prep": [random.choice(beverage_preps) for _ in range(ROWS)],
    "Calories": [random.randint(50, 500) for _ in range(ROWS)],
    "Total Fat (g)": [round(random.uniform(0, 20), 1) for _ in range(ROWS)],
    "Trans Fat (g)": [round(random.uniform(0, 5), 1) for _ in range(ROWS)],
    "Saturated Fat (g)": [round(random.uniform(0, 10), 1) for _ in range(ROWS)],
    "Sodium (mg)": [random.randint(0, 500) for _ in range(ROWS)],
    "Total Carbohydrates (g)": [round(random.uniform(0, 100), 1) for _ in range(ROWS)],
    "Cholesterol (mg)": [random.randint(0, 100) for _ in range(ROWS)],
    "Dietary Fibre (g)": [round(random.uniform(0, 10), 1) for _ in range(ROWS)],
    "Sugars (g)": [round(random.uniform(0, 50), 1) for _ in range(ROWS)],
    "Protein (g)": [round(random.uniform(0, 30), 1) for _ in range(ROWS)],
    "Vitamin A (% DV)": [random.randint(0, 100) for _ in range(ROWS)],
    "Vitamin C (% DV)": [random.randint(0, 100) for _ in range(ROWS)],
    "Calcium (% DV)": [random.randint(0, 100) for _ in range(ROWS)],
    "Iron (% DV)": [random.randint(0, 100) for _ in range(ROWS)],
    "Caffeine (mg)": [random.randint(0, 300) for _ in range(ROWS)],
}

# Create a DataFrame and save it to a CSV file
df = pd.DataFrame(data)
OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
