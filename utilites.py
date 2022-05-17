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


def clear_file(filename):
    with open(filename, 'w', encoding='utf8'):
        pass


def add_data_to_file(src, filename):
    with open(filename, 'a', encoding='utf8') as write_file:
        write_file.write(src)


def get_last_dir():
    pages_dir_from_os = os.listdir('htmls')
    dir_date_template = r'\d{2}-\d{2}-202\d'
    loaded_dirs = []
    for el in pages_dir_from_os:
        check_dir = re.findall(dir_date_template, el)
        try:
            if check_dir:
                dir_in_list = datetime.datetime.strptime(el, '%d-%m-%Y')
                loaded_dirs.append(dir_in_list)
        except ValueError as ex:
            print(ex)
    final_dir = sorted(loaded_dirs)[-1].strftime('%d-%m-%Y')
    print('last date is', final_dir)
    return final_dir


def get_last_filename(platform):
    result_files = os.listdir('result')
    platform_lst = []
    for file in result_files:
        if platform in file:
            platform_lst.append(file)
    return sorted(platform_lst)[-1]
