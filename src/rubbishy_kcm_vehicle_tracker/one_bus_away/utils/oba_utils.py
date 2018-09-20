from rubbishy_kcm_vehicle_tracker.one_bus_away.oba_constants import OBAConstants
import re


class OBAUtils:

    @staticmethod
    def get_agency_name_from_id(agency_id):
        if str(agency_id) in OBAConstants.OBA_VEHICLE_ID_PREFIX:
            return OBAConstants.OBA_VEHICLE_ID_PREFIX[str(agency_id)]
        return OBAConstants.UNKNOWN

    @staticmethod
    def get_route_number_from_short_name(short_name):
        if short_name.strip() in OBAConstants.SHORT_NAME_EXCEPTIONS:
            return OBAConstants.SHORT_NAME_EXCEPTIONS.get(short_name.strip())
        elif re.match('^[0-9]+$', short_name.strip()):
            return short_name.strip()
        return OBAConstants.UNKNOWN

    @staticmethod
    def get_agency_id_from_name(agency_name):
        for key in OBAConstants.OBA_VEHICLE_ID_PREFIX:
            if agency_name == OBAConstants.OBA_VEHICLE_ID_PREFIX.get(key):
                return key
        return OBAConstants.UNKNOWN

    @staticmethod
    def get_raw_vehicle_id_from_oba_style_vehicle_id(vehicle_id):
        if '_' in str(vehicle_id):
            agency, id = str(vehicle_id).split('_')
        else:
            agency = OBAConstants.KCM
            id = str(vehicle_id)
        if agency in [OBAConstants.KCM, OBAConstants.ST]:
            return id
        elif agency == OBAConstants.CT:
            return OBAConstants.CT_LINE_INDICATOR + id
        elif agency == OBAConstants.PT:
            return OBAConstants.PT_LINE_INDICATOR + id
        else:
            return str(vehicle_id)

    @staticmethod
    def get_agency_name_from_vehicle_id(vehicle_id):
        return OBAUtils.get_agency_name_from_id(
            vehicle_id.split('_')[0]
        )
