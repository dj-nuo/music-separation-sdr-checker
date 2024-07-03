import csv


def persist_result(result, csv_file):
    # Check if CSV file exists and create header if necessary
    try:
        with open(csv_file, 'r') as file:
            header_exists = csv.Sniffer().has_header(file.readline())
    except FileNotFoundError:
        header_exists = False

    # Write data to CSV file
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=result.keys(), delimiter='\t')

        if not header_exists:
            writer.writeheader()

        writer.writerow(result)

    # print(f"Data has been written to {csv_file}")
