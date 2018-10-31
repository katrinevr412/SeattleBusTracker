from oba_constants import OBAConstants
import re


class OBAVehicleIDParser:

    def __init__(self):
        pass

    def parse(self, raw_vehicle_id):
        """
            Parse the raw vehicle id and generate a list of all possible vehicle ids
            in OBA form.
        :param raw_vehicle_id:
        :return:
        """
        raw_vehicle_id = str(raw_vehicle_id)
        if '_' in raw_vehicle_id:
            # raw vehicle ids shouldn't contain underscores.
            return [raw_vehicle_id]
        # if an indicator is given, we use that
        if raw_vehicle_id.startswith(OBAConstants.CT_LINE_INDICATOR):
            return [OBAConstants.CT + '_' + raw_vehicle_id[1:]]
        elif raw_vehicle_id.startswith(OBAConstants.PT_LINE_INDICATOR):
            return [OBAConstants.PT + '_' + raw_vehicle_id[1:]]
        elif not re.match(r'^[0-9]+$', raw_vehicle_id):
            return []
        elif len(raw_vehicle_id) == 3:
            # 3-digit vehicle ids can be DARTs and Community Shuttles in KCM,
            # or PT buses.
            return [
                OBAConstants.KCM + '_' + raw_vehicle_id,
                OBAConstants.PT + '_' + raw_vehicle_id
            ]
        elif len(raw_vehicle_id) == 4:
            # for 4-digit vehicles:
            # if it starts with 9, it's a ST vehicle, otherwise it's a KCM vehicle.
            if raw_vehicle_id.startswith('9'):
                return [OBAConstants.ST + '_' + raw_vehicle_id]
            elif raw_vehicle_id.startswith('80'):
                return [OBAConstants.KCM + '_' + raw_vehicle_id, OBAConstants.PT + '_' + raw_vehicle_id]
            elif raw_vehicle_id.startswith('58'):
                return [OBAConstants.PT + '_' + raw_vehicle_id]
            else:
                return [OBAConstants.KCM + '_' + raw_vehicle_id]
        elif len(raw_vehicle_id) == 5:
            # for 5-digit vehicles:
            # if it begins with 4, 5, 6 it's a ST vehicle
            # if it begins with 1 or 2, it's a CT vehicle
            # otherwise, it doesn't exist
            if raw_vehicle_id[:1] in ['4', '5', '6']:
                return [OBAConstants.ST + '_' + raw_vehicle_id]
            elif raw_vehicle_id[:1] in ['1', '2']:
                return [OBAConstants.CT + '_' + raw_vehicle_id]
            else:
                return []
        return []
