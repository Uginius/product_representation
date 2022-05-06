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
