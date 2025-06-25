
import csv

def remove_duplicates(input_path, output_path):
    seen = set()
    with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        headers = next(reader)
        writer.writerow(headers)
        for row in reader:
            row_key = tuple(row)
            if row_key not in seen:
                seen.add(row_key)
                writer.writerow(row)
