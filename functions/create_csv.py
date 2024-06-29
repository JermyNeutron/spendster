# Create CSV
import csv

import pyperclip


def create_csv(test: bool, hints_enabled: bool, export_text: list) -> None:
    path = 'temp/temp.csv' if not test else 'temp/test_temp.csv'
    with open(path, mode='w', newline='') as file: # writes CSV.
        writer = csv.writer(file)
        writer.writerows(export_text)
        hints_enabled and print('\nHINT: CSV created.')
    with open(path, 'r', newline='') as file:
        csv_data = list(csv.reader(file))
        formatted_data = '\n'.join('\t'.join(row) for row in csv_data)
        pyperclip.copy(formatted_data)
        print("CSV content has been copied to clipboard. You can now paste it using CTRL+V.")
    if test: # converts type list into string to write into .txt.
        csv_view = 'temp/test_csv_view.txt'
        with open(csv_view, 'w') as file:
            for item in export_text:
                file.write(f"{str(item)}\n")
        hints_enabled and print('HINT: CSV view created...')


if __name__ == '__main__':
    create_csv(True, True, None)