import re
import os
from project_path import ProjectPathConfig
from global_constants import GlobalConstants


class TrackerConfig:

    REAL_DEFAULT_CACHE = True
    REAL_DEFAULT_REFRESH_CACHE = False
    REAL_DEFAULT_MISSING_ONLY = True
    REAL_DEFAULT_ENABLE_PARALLEL = True
    REAL_DEFAULT_API = GlobalConstants.OBA_API

    def __init__(self,
                 cache=REAL_DEFAULT_CACHE,
                 refresh_cache=REAL_DEFAULT_REFRESH_CACHE,
                 enable_parallel=REAL_DEFAULT_ENABLE_PARALLEL,
                 missing_only=REAL_DEFAULT_MISSING_ONLY,
                 api=REAL_DEFAULT_API):
        self.cache = cache
        self.refresh_cache = refresh_cache
        self.enable_parallel = enable_parallel
        self.missing_only = missing_only
        self.api = api
        try:
            with open(os.path.join(ProjectPathConfig.SOURCE_ROOT_PATH, GlobalConstants.CONFIG_FILE_NAME), 'r') as _config:
                self.__read_config(_config.readlines())
        except Exception as e:
            print "cannot load tracker config: %s" % getattr(e, 'strerror', e.message)
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
