import os
import yaml
import json
from pathlib import Path

import pandas as pd
import datetime
import time

from pandas._libs.tslibs.parsing import relativedelta


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

    if parse:
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
    return df


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

    if parse:
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
    else:
        return df


#create a function that will take the input age and return the date of birth
def get_date_of_birth(age):
    return datetime.date.today() - relativedelta(years=age)


#create a list comprehension that will read the parameter from the input file and return the equivalent value from choice_dtc.yaml
def get_dtc_value(parameter):
    return get_config('choice_dtc.yaml')[parameter]

