import csv
import argparse
from pathlib import Path

import logging

# Configure once at the top of your script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting...")

    parser = argparse.ArgumentParser(description="Split CSV by a grouping column")
    parser.add_argument("input_file", help="Path to input CSV")
    parser.add_argument("--output-dir", default="output", help="Directory for output files")
    parser.add_argument("--group-by", default="meter_id", help="Column to split on")
    args = parser.parse_args()

    input_file = Path(args.input_file)
    output_dir = Path(args.output_dir)
    group_by_col = args.group_by

    output_dir.mkdir(parents=True, exist_ok=True)

    meter_data = {}

    try:
        with open(input_file, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row[group_by_col]
                if key not in meter_data:
                    meter_data[key] = []
                meter_data[key].append(row)
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
        raise          # re-raise if you want the script to exit with a non-zero code
    
    
    files_written = 0    
    for meter_id, rows in meter_data.items():
        output_file = output_dir / f"{meter_id}.csv"
        try:
            with open(output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["meter_id", "date", "value"])
                writer.writeheader()
                writer.writerows(rows)
            logger.info(f"Written {output_file} - {len(rows)} rows")
            files_written += 1
        except Exception as e:
            logger.error(f"Failed to write {output_file}: {e}")
            continue
            
    logger.info(f"Done. {len(rows)} files written.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
