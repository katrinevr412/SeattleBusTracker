class KCMTrackerConfig:

    REAL_DEFAULT_CACHE = True
    REAL_DEFAULT_REFRESH_CACHE = False
    REAL_DEFAULT_MISSING_ONLY = True
    REAL_DEFAULT_ENABLE_PARALLEL = True

    def __init__(self,
                 cache=REAL_DEFAULT_CACHE,
                 refresh_cache=REAL_DEFAULT_REFRESH_CACHE,
                 enable_parallel=REAL_DEFAULT_ENABLE_PARALLEL,
                 missing_only=REAL_DEFAULT_MISSING_ONLY):
        self.cache = cache
        self.refresh_cache = refresh_cache
        self.enable_parallel = enable_parallel
        self.missing_only = missing_only
