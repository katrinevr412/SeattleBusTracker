import os
from rubbishy_kcm_vehicle_tracker.common.utils.common_utils import CommonUtils


class DataWriter:

    def __init__(self, dir):
        self.dir = dir
        CommonUtils.make_dir_if_not_exists(dir)

    def write(self, filename, content):
        with open(os.path.join(self.dir, filename), 'a') as _file:
            _file.write(content + '\n')
