'''
A module to save user generated data in xlsx file
'''

import datetime
import os

def get_file_name_with_path():
    '''
    Returns the file name with path of the xlsx file
    '''
    year = datetime.datetime.now().year
    month = datetime.datetime.now().strftime("%B")
    day_name = datetime.datetime.now().strftime("%A")
    day = datetime.datetime.now().strftime("%D").replace("/","-")
    file_name = f"{year}/{month}/{day_name}-{day}.xlsx"
    return file_name

def load_file():
    filename = get_file_name_with_path()
    try:
        f= open(filename, 'ab')
    except FileNotFoundError:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        f= open(filename, 'ab')
    return f

def save_data(data):
    pass

save_data({"hello":123})