import json
import logging
import re

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from config import DB_CONFIG


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def create_database_connection():
    """Create a connection to the MySQL database."""

    try:
        connection_url = URL.create(
            "mysql+pymysql",
            username=DB_CONFIG["username"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"]
        )

        engine = create_engine(connection_url)

        logging.info("Connected to MySQL successfully.")
        return engine

    except Exception as error:
        logging.error("Database connection failed: %s", error)
        raise


def load_json_data(file_name):
    """Load JSON data into a pandas DataFrame."""

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            json_data = json.load(file)

        dataframe = pd.DataFrame(
            json_data["data"],
            columns=json_data["cols"]
        )

        logging.info("JSON data loaded successfully.")

        return dataframe

    except Exception as error:
        logging.error("Failed to load JSON file: %s", error)
        raise


def load_data_to_mysql(dataframe, engine):
    """Load DataFrame into MySQL."""

    try:
        dataframe.to_sql(
            "json_to_sql_table",
            con=engine,
            if_exists="replace",
            index=False
        )

        logging.info("Data loaded into MySQL successfully.")

    except Exception as error:
        logging.error("Failed to load data into MySQL: %s", error)
        raise


def read_data_from_mysql(engine):
    """Read data from MySQL into a DataFrame."""

    query = "SELECT * FROM json_to_sql_table"

    try:
        dataframe = pd.read_sql(query, engine)

        logging.info("Data successfully loaded from MySQL.")

        return dataframe

    except Exception as error:
        logging.error("Failed to read data from MySQL: %s", error)
        raise


def fix_email(email):
    """Change the email domain to gmail.com."""

    username = email.split("@")[0]

    return f"{username}@gmail.com"


def fix_postal_zip(value):
    """Keep only numbers and convert the value to integer."""

    numbers = re.sub(r"[^0-9]", "", str(value))

    if numbers == "":
        return None

    return int(numbers)


def encode_phone(phone):
    """
    Remove non-numeric characters and convert
    every two digits into an ASCII character.

    Values below 65 are replaced with O.
    """

    digits = re.sub(r"\D", "", str(phone))

    result = ""

    for index in range(0, len(digits) - 1, 2):
        number = int(digits[index:index + 2])

        if number < 65:
            result += "O"
        else:
            result += chr(number)

    return result


def transform_data(dataframe):
    """Apply all required transformations."""

    dataframe["email"] = dataframe["email"].apply(fix_email)

    dataframe["postalZip"] = dataframe["postalZip"].apply(
        fix_postal_zip
    )

    dataframe["phone"] = dataframe["phone"].apply(
        encode_phone
    )

    dataframe.rename(
        columns={"phone": "coded_phone_number"},
        inplace=True
    )

    return dataframe


def main():
    """Run the complete data manipulation process."""

    engine = create_database_connection()

    # Step 1: Load JSON
    dataframe = load_json_data(
        "sample_data_for_assignment.json"
    )

    # Step 2: Load JSON data into MySQL
    load_data_to_mysql(dataframe, engine)

    # Step 3: Read data from MySQL
    dataframe = read_data_from_mysql(engine)

    # Step 4: Display original data
    print("\nOriginal Data:")
    print(dataframe)

    # Step 5: Transform data
    dataframe = transform_data(dataframe)

    # Step 6: Display final data
    print("\nFinal Data:")
    print(dataframe)


if __name__ == "__main__":
    main()