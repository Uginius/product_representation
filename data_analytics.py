import os


class DataAnalytics:
    def __init__(self):
        self.oz_json_filename, self.wb_json_filename = None, None

    def run(self):
        self.get_last_filenames()
        self.get_json()

    def get_json(self):
        pass

    def get_last_filenames(self):
        result_files = os.listdir('result')
        oz_lst, wb_lst = [], []
        for file in result_files:
            if 'wb' in file:
                wb_lst.append(file)
            elif 'oz' in file:
                oz_lst.append(file)
        self.oz_json_filename = sorted(oz_lst)[-1]
        self.wb_json_filename = sorted(wb_lst)[-1]

    def set_result_filenames(self):
        date_template = ''
        pass
