from rubbishy_kcm_vehicle_tracker.common.project_path import ProjectPathConfig
from rubbishy_kcm_vehicle_tracker.common.utils.common_utils import CommonUtils
from rubbishy_kcm_vehicle_tracker.one_bus_away.utils.oba_utils import OBAUtils
import os
import json


class OBARouteCache:

    def __init__(self):
        self.cache_path = os.path.join(
            ProjectPathConfig.DATA_ROOT_PATH,
            'cache',
            'oba_api',
            'routes'
        )
        CommonUtils.make_dir_if_not_exists(self.cache_path)

    def write(self, agency_id, json_obj):
        filename = self.__get_file_name(agency_id)
        with open(os.path.join(self.cache_path, filename), 'w') as _cache:
            json.dump(obj=json_obj, fp=_cache)

    def read(self, agency_id):
        filename = self.__get_file_name(agency_id)
        with open(os.path.join(self.cache_path, filename), 'r') as _cache:
            return json.load(fp=_cache)

    def clear(self):
        for filename in os.listdir(self.cache_path):
            os.remove(os.path.join(self.cache_path, filename))

    def __get_file_name(self, agency_id):
        return OBAUtils.get_agency_name_from_id(agency_id) + '.txt'
