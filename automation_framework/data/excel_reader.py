import openpyxl
import os
from typing import List, Dict, Any

class ExcelReader:
    """Reads structured test data from Excel spreadsheets (.xlsx)."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Excel file not found at: {filepath}")

    def read_sheet_as_dicts(self, sheet_name: str) -> List[Dict[str, Any]]:
        """Reads rows from a sheet and returns a list of dictionaries keyed by header."""
        wb = openpyxl.load_workbook(self.filepath, data_only=True)
        if sheet_name not in wb.sheetnames:
            wb.close()
            raise ValueError(f"Sheet '{sheet_name}' does not exist in {self.filepath}")

        sheet = wb[sheet_name]
        rows = list(sheet.iter_rows(values_only=True))
        wb.close()

        if not rows:
            return []

        headers = [str(h).strip() if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
        records = []

        for row in rows[1:]:
            if all(cell is None for cell in row):
                continue
            record = {}
            for header, val in zip(headers, row):
                record[header] = "" if val is None else str(val).strip()
            records.append(record)

        return records

    def get_row_by_key(self, sheet_name: str, key_col: str, key_val: str) -> Dict[str, Any]:
        """Finds first row matching a key column value."""
        records = self.read_sheet_as_dicts(sheet_name)
        for r in records:
            if r.get(key_col) == key_val:
                return r
        return {}
