#!/usr/bin/env python3
"""Build the interactive HTML preview from the beverages CSV.

The preview is a single self-contained HTML file. This script reads the CSV,
cleans the column names and values, and embeds the result as JSON in
Scripts/preview_template.html.

Usage (run from anywhere):
    python Scripts/build_preview.py              # Data/beverages_data.csv, or the synthetic sample if it is missing
    python Scripts/build_preview.py --csv Data/beverages_data.csv --out Previews/preview.html
    python Scripts/build_preview.py --csv Data/sample/beverages_data_synthetic.csv --synthetic

Use --synthetic when the CSV is the random sample from dummy_data_generator.py.
It adds a "Sample data" notice to the page.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# Normalised CSV header -> key used by the page
COLUMNS = {
    "beveragecategory": "category",
    "beverage": "beverage",
    "beverageprep": "prep",
    "calories": "calories",
    "totalfatg": "totalFat",
    "transfatg": "transFat",
    "saturatedfatg": "satFat",
    "sodiummg": "sodium",
    "totalcarbohydratesg": "carbs",
    "cholesterolmg": "cholesterol",
    "dietaryfibreg": "fibre",
    "dietaryfiberg": "fibre",
    "sugarsg": "sugars",
    "proteing": "protein",
    "vitaminadv": "vitA",
    "vitamincdv": "vitC",
    "calciumdv": "calcium",
    "irondv": "iron",
    "caffeinemg": "caffeine",
}
TEXT = ["category", "beverage", "prep"]
PERCENT = ["vitA", "vitC", "calcium", "iron"]
REQUIRED = ["category", "beverage", "calories"]


def normalise(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def load(csv_path: Path) -> pd.DataFrame:
    raw = pd.read_csv(csv_path)
    renamed = {}
    for col in raw.columns:
        key = COLUMNS.get(normalise(col))
        if key and key not in renamed.values():
            renamed[col] = key
    df = raw.rename(columns=renamed)[list(renamed.values())].copy()

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        sys.exit(f"Missing required columns: {', '.join(missing)}. Found: {', '.join(raw.columns)}")

    for col in df.columns:
        if col in TEXT:
            df[col] = df[col].astype(str).str.strip().replace({"nan": None, "": None})
        else:
            cleaned = df[col].astype(str).str.replace("%", "", regex=False).str.strip()
            df[col] = pd.to_numeric(cleaned, errors="coerce")

    # Daily-value columns stored as fractions (0 to 1) become percentages (0 to 100)
    for col in PERCENT:
        if col in df.columns and df[col].max() <= 1.0:
            df[col] = df[col] * 100
    return df


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=None, help="CSV to embed (default: Data/beverages_data.csv)")
    ap.add_argument("--template", default=str(ROOT / "Scripts" / "preview_template.html"))
    ap.add_argument("--out", default=str(ROOT / "Previews" / "preview.html"))
    ap.add_argument("--synthetic", action="store_true", help="mark the data as random sample data")
    args = ap.parse_args()

    template_path, out_path = Path(args.template), Path(args.out)
    synthetic = args.synthetic
    if args.csv:
        csv_path = Path(args.csv)
    else:
        real = ROOT / "Data" / "beverages_data.csv"
        sample = ROOT / "Data" / "sample" / "beverages_data_synthetic.csv"
        if real.exists():
            csv_path = real
        elif sample.exists():
            csv_path, synthetic = sample, True
            print("Data/beverages_data.csv not found, using the synthetic sample instead.")
        else:
            sys.exit("No data found. Put the dataset at Data/beverages_data.csv or pass --csv.")
    df = load(csv_path)

    cols = list(df.columns)
    rows = []
    for rec in df.itertuples(index=False):
        row = []
        for col, val in zip(cols, rec):
            if val is None or (isinstance(val, float) and pd.isna(val)):
                row.append(None)
            elif isinstance(val, float):
                row.append(round(val, 2))
            else:
                row.append(val)
        rows.append(row)

    payload = {
        "meta": {"source": csv_path.name, "rows": len(rows), "synthetic": bool(synthetic)},
        "cols": cols,
        "rows": rows,
    }
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

    html = template_path.read_text(encoding="utf-8")
    if "__PAYLOAD__" not in html:
        sys.exit("Template is missing the __PAYLOAD__ placeholder.")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html.replace("__PAYLOAD__", data), encoding="utf-8")
    print(f"Wrote {out_path} ({len(rows)} rows, {out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
