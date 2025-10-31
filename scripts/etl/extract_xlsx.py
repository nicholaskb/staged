#!/usr/bin/env python3
"""
Extract tabular data from all .xlsx files in a directory (all sheets), optionally ingest
existing .csv files in the same folder, and write per-sheet CSVs plus an optional
combined CSV.

Usage:
  python extract_xlsx.py --input-dir /Users/nicholasbaro/Python/staged/data --combine

Notes:
- Requires pandas and openpyxl: pip install pandas openpyxl
- Default input directory is "./data" relative to this script's location.
"""

from __future__ import annotations

import argparse
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract .xlsx sheets to CSV and optionally combine with CSV files.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "data",
        help="Directory containing .xlsx/.csv files (default: ./data)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write outputs (default: <input-dir>/extracted)",
    )
    parser.add_argument(
        "--combine",
        action="store_true",
        help="Also create a combined CSV with all rows and source metadata.",
    )
    parser.add_argument(
        "--combined-filename",
        type=str,
        default="combined_all.csv",
        help="Filename for the combined CSV (when --combine is set).",
    )
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="CSV encoding for outputs (default: utf-8)",
    )
    return parser.parse_args(argv)


def ensure_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)


def sanitize_for_filename(name: str) -> str:
    # Replace unsafe filename characters
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return sanitized or "sheet"


def read_excel_all_sheets(xlsx_path: Path) -> Dict[str, "pandas.DataFrame"]:
    import pandas as pd  # Local import to avoid hard dependency for other uses

    # Read all sheets as strings to preserve data fidelity without dtype surprises
    sheets: Dict[str, pd.DataFrame] = pd.read_excel(
        xlsx_path,
        sheet_name=None,
        dtype=str,
        engine="openpyxl",
    )
    return sheets


def normalize_columns(df: "pandas.DataFrame") -> "pandas.DataFrame":
    # Strip whitespace and unify column names
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def write_sheet_csv(df: "pandas.DataFrame", output_path: Path, encoding: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding=encoding)


def extract_xlsx_to_csv(input_dir: Path, output_dir: Path, encoding: str) -> List[Path]:
    written_paths: List[Path] = []
    for xlsx_path in sorted(input_dir.glob("*.xlsx")):
        sheets = read_excel_all_sheets(xlsx_path)
        workbook_stem = sanitize_for_filename(xlsx_path.stem)
        for sheet_name, df in sheets.items():
            df = normalize_columns(df)
            safe_sheet = sanitize_for_filename(str(sheet_name))
            output_path = output_dir / f"{workbook_stem}__{safe_sheet}.csv"
            write_sheet_csv(df, output_path, encoding)
            print(f"Wrote: {output_path}")
            written_paths.append(output_path)
    return written_paths


def read_csv_files(input_dir: Path, encoding: str) -> Dict[str, "pandas.DataFrame"]:
    import pandas as pd

    csv_map: Dict[str, pd.DataFrame] = {}
    for csv_path in sorted(input_dir.glob("*.csv")):
        try:
            df = pd.read_csv(csv_path, dtype=str, encoding=encoding)
        except UnicodeDecodeError:
            # Fallback for BOM or other encodings commonly seen in Excel exports
            df = pd.read_csv(csv_path, dtype=str, encoding="utf-8-sig")
        df = normalize_columns(df)
        csv_map[csv_path.name] = df
    return csv_map


def build_combined_dataframe(
    per_sheet_paths: List[Path],
    input_dir: Path,
    encoding: str,
) -> "pandas.DataFrame":
    import pandas as pd

    frames: List[pd.DataFrame] = []

    # Include per-sheet CSVs we just wrote (authoritative from .xlsx)
    for path in per_sheet_paths:
        try:
            df = pd.read_csv(path, dtype=str, encoding=encoding)
        except UnicodeDecodeError:
            df = pd.read_csv(path, dtype=str, encoding="utf-8-sig")
        df["source_file"] = path.name
        # Infer workbook and sheet from naming convention
        if "__" in path.stem:
            workbook, sheet = path.stem.split("__", 1)
        else:
            workbook, sheet = path.stem, ""
        df["workbook"] = workbook
        df["sheet"] = sheet
        frames.append(df)

    # Also include any standalone CSVs present in the input dir
    standalone_csvs = read_csv_files(input_dir, encoding)
    for csv_name, df in standalone_csvs.items():
        df = df.copy()
        df["source_file"] = csv_name
        df["workbook"] = Path(csv_name).stem
        df["sheet"] = "(csv)"
        frames.append(df)

    if not frames:
        import pandas as pd

        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True, sort=False)
    # Normalize column order to surface metadata first
    meta_cols = [c for c in ["source_file", "workbook", "sheet"] if c in combined.columns]
    other_cols = [c for c in combined.columns if c not in meta_cols]
    combined = combined[meta_cols + other_cols]
    return combined


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    input_dir: Path = args.input_dir.resolve()
    output_dir: Path = (args.output_dir or (input_dir / "extracted")).resolve()
    encoding: str = args.encoding

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: input directory does not exist or is not a directory: {input_dir}", file=sys.stderr)
        return 2

    ensure_output_dir(output_dir)

    print(f"Scanning: {input_dir}")
    per_sheet_paths = extract_xlsx_to_csv(input_dir, output_dir, encoding)

    if args.combine:
        print("Building combined CSV...")
        try:
            combined_df = build_combined_dataframe(per_sheet_paths, input_dir, encoding)
        except Exception as exc:  # Defensive: ensure we still return per-sheet outputs if combine fails
            print(f"Warning: failed to build combined CSV: {exc}", file=sys.stderr)
            return 1

        if combined_df.empty:
            print("No data found to combine.")
        else:
            combined_path = output_dir / args.combined_filename
            combined_df.to_csv(combined_path, index=False, encoding=encoding)
            print(f"Wrote combined CSV: {combined_path}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


