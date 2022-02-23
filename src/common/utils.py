import copy
import json
import os
import re
from contextlib import suppress
from datetime import date, datetime
from enum import Enum
from logging import getLogger
from pathlib import Path

import pandas as pd
import yaml
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class MergeStrategy(Enum):
    DeleteKey = 0


def deep_merge_dict(base: dict, addition: dict) -> dict:
    """
    Recursively merge dictionaries.

    Values in `addition` can be set to a variant of `MergeStrategy`
    to induce special behavior.
    """
    base = copy.deepcopy(base)

    for key, value in addition.items():
        if value == MergeStrategy.DeleteKey:
            base.pop(key, None)
        elif isinstance(value, dict) and key in base and isinstance(base[key], dict):
            base[key] = deep_merge_dict(base.get(key, {}), value)
        else:
            base[key] = addition[key]
    return base


def get_config(file_name):
    if file_name is None or file_name == "config.yaml":
        root_dir = Path(__file__).parents[2]
        data = yaml.safe_load((root_dir / "config.yaml").read_text())
        override = root_dir / "config.override.yaml"
        if override.exists():
            data = deep_merge_dict(data, yaml.safe_load(override.read_text()))
        return data
    # if file_name is not None
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
    """Federal age limit is 21 years old."""
    return get_age(date_of_birth.replace("-", "/")) > 21


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
    """
    Accepts a string and checks if the string is in pascal case.
    pascal case: 'PascalCase'
    """
    return string != string.lower() and string != string.upper() and " " not in string


def rectify_zip_code(zip_code: str) -> str:
    # if zip_code is less than 5 digits, add leading zeros
    if len(zip_code) < 5:
        return "0" * (5 - len(zip_code)) + zip_code
    return zip_code


def compare_values(value, value_2) -> None:
    log = getLogger("compare_values")
    if value != value_2:
        log.error(f"Values do not match: {value} != {value_2}")
        assert False, ValueError(f"Values do not match: {value} != {value_2}")
    log.info(f"Values match: {value} == {value_2}")


def clear_input_fields(driver: webdriver) -> None:
    # clears the remaining data in the text fields if any from previous test
    web_elements = driver.find_elements_by_xpath('//input[@type="text" or @type="email" or @type="tel"]')
    for element in web_elements:
        # As element.clear() does not work, we utilize `Keys` instead
        element.send_keys(f"{Keys.CONTROL}A{Keys.DELETE}")


def reset_non_primary_applicant_demographics(driver: webdriver) -> None:
    with suppress(NoSuchElementException):
        # Checking if Spouse demographics is displayed
        driver.find_element_by_xpath("//div[@aria-label='Spouse ']")
        driver.find_element_by_xpath("//div[@aria-label='Spouse ']//button[@id='remove-button-icon']").click()
        # Checking if Dependent demographics is displayed
        driver.find_element_by_xpath("//div[@aria-label='Dependent ']")
        driver.find_element_by_xpath("//div[@aria-label='Dependent ']//button[@id='remove-button-icon']").click()
