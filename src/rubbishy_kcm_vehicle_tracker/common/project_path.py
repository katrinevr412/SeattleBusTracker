import os


class ProjectPathConfig:

    SOURCE_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(SOURCE_ROOT_PATH)), 'data')
