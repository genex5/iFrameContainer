import csv
import re

def validate_employee_id(employee_id, existing_ids):
    errors = []
    if not employee_id.isdigit():
        errors.append(f"Invalid employee ID: '{employee_id}' is not numeric.")
    elif employee_id in existing_ids:
        errors.append(f"Duplicate employee ID: '{employee_id}'.")
    return errors

def validate_currency(currency_string):
    errors = []
    # Regex to check for an optional currency symbol at the beginning and a valid number.
    if not re.match(r'^\$?\d+(\.\d+)?$', currency_string):
        errors.append(f"Invalid currency format: '{currency_string}'.")
    return errors

def validate_csv(file_path):
    errors = []
    existing_ids = set()

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row

        for row_num, row in enumerate(reader, start=2):
            if len(row) != 3:
                errors.append(f"Row {row_num}: Incorrect number of columns.")
                continue

            employee_id, name, salary = row

            # Validate Employee ID
            id_errors = validate_employee_id(employee_id, existing_ids)
            if id_errors:
                errors.extend([f"Row {row_num}: {error}" for error in id_errors])
            else:
                existing_ids.add(employee_id)

            # Validate Salary (currency format)
            salary_errors = validate_currency(salary)
            if salary_errors:
                errors.extend([f"Row {row_num}: {error}" for error in salary_errors])

    return errors

def generate_report(errors, report_file):
    with open(report_file, 'w') as f:
        if errors:
            f.write("Payroll Validation Error Report:\n")
            f.write("=" * 30 + "\n")
            for error in errors:
                f.write(f"- {error}\n")
        else:
            f.write("No errors found in the payroll CSV file.\n")

if __name__ == "__main__":
    errors = validate_csv('payroll.csv')
    generate_report(errors, 'error_report.txt')
    print("Validation complete. Report generated in 'error_report.txt'.")
