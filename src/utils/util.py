import os
import re
import yaml
import json
import pandas as pd

from pathlib import Path
from datetime import date, datetime

from src.choice_dtc.browser import Browser


def get_config(file_name):
    root = get_file_path(file_name)
    if file_name.endswith('.yaml'):
        with open(root, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    elif file_name.endswith('.json'):
        with open(root, 'r') as f:
            data = json.load(f)
    else:
        raise ValueError('File type not supported')
    return data


def get_file_path(file_name):
    root_dir = Path(__file__).parents[2]
    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            if name == file_name:
                return os.path.join(root, name)
    raise FileNotFoundError('File not found')


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
    if not re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date_of_birth):
        assert False, ValueError('Date of birth must be in the format dd/mm/yyyy')
    today = date.today()
    dob = datetime.strptime(date_of_birth, "%m/%d/%Y")
    return (
            today.year
            - dob.year
            - ((today.month, today.day) < (dob.month, dob.day))
    )


def is_legal_age(date_of_birth: str) -> bool:
    """
    Federal age limit is 21 years old.
    """
    return get_age(date_of_birth.replace('-', '/')) < 21


def parse_str(string):
    string = string.replace("/", "")
    string = string.replace(" ", "_")
    return string.lower()


def lob_clean_state(driver) -> None:
    browser = Browser('lob_clean_state', driver)
    lob_list = [
        "Medicare Insurance",
        "Short Term Health Insurance",
        "ACA Health Insurance",
        "Dental Insurance",
        "Vision Insurance",
        "Supplemental Insurance",
    ]
    for lob in lob_list:
        lob_element = browser.get_web_element(f"//h6[text() = '{lob}']", locator_type='xpath')
        # if lob is already on a checked state, uncheck it.
        if "font-weight: bold" in lob_element.get_attribute('style'):
            lob_element.click()


def title_case(string):
    # accepts a string and returns a title cased string
    return " ".join(s.capitalize() for s in string.split(" "))
