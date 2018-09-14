import re
import os


class TrackerConfig:

    REAL_DEFAULT_CACHE = True
    REAL_DEFAULT_REFRESH_CACHE = False
    REAL_DEFAULT_CMD_STR = 'ens'  # Only East, North and South bases
    REAL_DEFAULT_MISSING_ONLY = True
    REAL_DEFAULT_ENABLE_PARALLEL = True

    def __init__(self):
        self.__load_real_default()
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'), 'r') as config:
                self.__read_config(config.readlines())
        except:
            # in case the config file is missing, fall back to "real" default values
            pass

    def __read_config(self, config_lines):
        for config_line in config_lines:
            if config_line.strip().startswith('#'):
                continue
            key, value = config_line.strip().split('=')
            if value.lower() == 'false':
                value = False
            elif value.lower() == 'true':
                value = True
            if re.match(r'^[a-zA-Z_]\w*$', key):
                setattr(self, key, value)

    def __load_real_default(self):
        self.cache = self.REAL_DEFAULT_CACHE
        self.cmd_str = self.REAL_DEFAULT_CMD_STR
        self.missing_only = self.REAL_DEFAULT_MISSING_ONLY
        self.refresh_cache = self.REAL_DEFAULT_REFRESH_CACHE
        self.enable_parallel = self.REAL_DEFAULT_ENABLE_PARALLEL
