
# Python Data Manipulation Assignment

This project loads JSON data into a MySQL database, retrieves it using Pandas, and performs different data transformations.

## Requirements

- Python 3
- MySQL
- Pandas
- SQLAlchemy
- PyMySQL

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Database Setup

Create the MySQL database:

```sql
CREATE DATABASE python_assignment;
```

The program uses the following table:

```text
json_to_sql_table
```

Update the MySQL username and password in `config.py`.

## How to Run

Run the main program:

```bash
python main.py
```

The program:

1. Loads data from the JSON file.
2. Stores the data in MySQL.
3. Loads the data from MySQL into a Pandas DataFrame.
4. Converts all email addresses to `gmail.com`.
5. Converts `postalZip` values to integers.
6. Encodes phone numbers into ASCII characters.
7. Renames `phone` to `coded_phone_number`.

## Testing

Run the unit tests:

```bash
python -m pytest
```

