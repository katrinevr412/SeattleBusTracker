import os


class CommonUtils:

    @staticmethod
    def make_dir_if_not_exists(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
