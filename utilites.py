import datetime
import os
import re
import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'\nФункция работала {elapsed} секунд(ы)')
        return result

    return surrogate


def write_html(src, filename):
    with open(filename, 'w', encoding='utf8') as write_file:
        write_file.write(src)


def add_data_to_file(src, filename):
    with open(filename, 'a', encoding='utf8') as write_file:
        write_file.write(src)


def get_last_dir():
    pages_dir_from_os = os.listdir('htmls')
    dir_date_template = r'\d{2}-\d{2}-202\d'
    loaded_dirs = []
    for el in pages_dir_from_os:
        check_dir = re.findall(dir_date_template, el)
        if check_dir:
            dir_in_list = datetime.datetime.strptime(el, '%d-%m-%Y')
            loaded_dirs.append(dir_in_list)
    return sorted(loaded_dirs)[-1].strftime('%d-%m-%Y')
