import os
import re
import yaml
import json
import pandas as pd

from pathlib import Path
from datetime import date, datetime
from logging import getLogger


def get_config(file_name):
    root = get_file_path(file_name)
    if file_name.endswith(".yaml"):
        with open(root, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    elif file_name.endswith(".json"):
        with open(root, "r") as f:
            data = json.load(f)
    else:
        raise ValueError("File type not supported")
    return data


def get_file_path(file_name):
    root_dir = Path(__file__).parents[2]
    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            if name == file_name:
                return os.path.join(root, name)
    raise FileNotFoundError("File not found")


def read_xls(file_name, parse=True):
    """
    Get excel data
    :param file_name:
    :param parse:
    :return parsed excel:
    """
    fp = get_file_path(file_name)
    xl = pd.read_excel(fp)
    df = pd.DataFrame(xl)

    if not parse:
        return df
    values = []
    for row in df.iterrows():
        row = list(row)
        row[1] = [str(item).strip() for item in row[1]]
        row[1] = [str(item).replace("/", "-") for item in row[1]]
        row[1] = [str(item).replace("\t", "") for item in row[1]]
        row[1] = [str(item).replace(":", "") for item in row[1]]
        items = [n for n in row[1]]
        values.append(tuple(items))
    return values


def read_csv(file_name, parse=True):
    """
    Get csv data
    :param file_name:
    :param parse:
    :return parsed csv:
    """
    fp = get_file_path(file_name)
    csv = pd.read_csv(fp)
    df = pd.DataFrame(csv)

    if not parse:
        return df
    values = []
    for row in df.iterrows():
        row = list(row)
        row[1] = [str(item).strip() for item in row[1]]
        row[1] = [str(item).replace("/", "-") for item in row[1]]
        row[1] = [str(item).replace("\t", "") for item in row[1]]
        row[1] = [str(item).replace(":", "") for item in row[1]]
        items = [n for n in row[1]]
        values.append(tuple(items))
    return values


def get_age(date_of_birth: str) -> int:
    if not re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", date_of_birth):
        assert False, ValueError("Date of birth must be in the format dd/mm/yyyy")
    today = date.today()
    dob = datetime.strptime(date_of_birth, "%m/%d/%Y")
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def is_legal_age(date_of_birth: str) -> bool:
    """
    Federal age limit is 21 years old.
    """
    return get_age(date_of_birth.replace("-", "/")) < 21


def parse_str(string):
    string = string.replace("/", "")
    string = string.replace(" ", "_")
    return string.lower()


def title_case(string):
    # accepts a string and returns a title cased string
    if _is_pascal_case(string):
        return string
    return " ".join(s.capitalize() for s in string.split(" "))


def _is_pascal_case(string) -> bool:
    # accepts a string and checks if the string is in pascal case
    # pascal case: 'PascalCase'
    return string != string.lower() and string != string.upper() and " " not in string


def rectify_zip_code(zip_code: str) -> str:
    # if zip_code is less than 5 digits, add zeros to the front
    if len(zip_code) < 5:
        return "0" * (5 - len(zip_code)) + zip_code
    return zip_code


def compare_values(value, value_2) -> None:
    log = getLogger("compare_values")
    if value != value_2:
        log.error(f"Values do not match: {value} != {value_2}")
        assert False, ValueError(f"Values do not match: {value} != {value_2}")
    log.info(f"Values match: {value} == {value_2}")
