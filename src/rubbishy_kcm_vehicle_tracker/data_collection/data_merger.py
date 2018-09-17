import os
import pytz
from datetime import datetime
from rubbishy_kcm_vehicle_tracker.utils.utils import Utils


class DataMerger:

    def __init__(self, from_dir, to_dir,
                 date_formatter=lambda: datetime.now(pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %a'),
                 file_formatter=lambda _file: '',
                 clean_source_after_complete=True
                 ):
        self.from_dir = from_dir
        self.to_dir = to_dir
        self.date_formatter = date_formatter
        self.file_formatter = file_formatter
        self.clean_source = clean_source_after_complete
        Utils.make_dir_if_not_exists(from_dir)
        Utils.make_dir_if_not_exists(to_dir)

    def merge(self):
        filenames = filter(lambda path: os.path.isfile(os.path.join(self.from_dir, path)), os.listdir(self.from_dir))
        for filename in filenames:
            self.__merge_single_file(filename)
        if self.clean_source:
            self.__clean_source()

    def __merge_single_file(self, filename):
        from_file_path = os.path.join(self.from_dir, filename)
        to_file_path = os.path.join(self.to_dir, filename)
        with open(from_file_path, 'r') as _from_file,\
                open(to_file_path, 'a') as _to_file:
            formatted_content = self.file_formatter(_from_file)
            formatted_date = self.date_formatter()
            _to_file.write(formatted_date + '\t' + formatted_content + '\n')

    def __clean_source(self):
        for filename in os.listdir(self.from_dir):
            os.remove(os.path.join(self.from_dir, filename))
