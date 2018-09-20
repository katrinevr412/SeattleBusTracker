from rubbishy_kcm_vehicle_tracker.one_bus_away.utils.oba_utils import OBAUtils
from rubbishy_kcm_vehicle_tracker.one_bus_away.oba_constants import OBAConstants


class OBARoute:

    def __init__(self,
                 agency=OBAConstants.UNKNOWN,
                 id='0_000000',
                 number=OBAConstants.UNKNOWN,
                 name=OBAConstants.UNKNOWN):
        self.agency = agency
        self.id = id
        self.number = number
        self.name = name

    @staticmethod
    def from_json_obj(json_obj):
        return OBARoute(
            agency=OBAUtils.get_agency_name_from_id(json_obj['agencyId'].strip()),
            id=json_obj['id'],
            number=OBAUtils.get_route_number_from_short_name(json_obj['shortName']),
            name=json_obj['description'] or json_obj['longName']
        )

    @staticmethod
    def from_route_id(route_id):
        """
            Get an unrecognized route object from a raw route id.
            Used when the route id is not in our cache.
        :param route_id:
        :return:
        """
        return OBARoute(
            agency=OBAConstants.UNKNOWN,
            id=route_id,
            number=OBAConstants.UNKNOWN,
            name=OBAConstants.UNKNOWN
        )

    def serialize(self):
        return {
            'agencyId': OBAUtils.get_agency_id_from_name(self.agency),
            'id': self.id,
            'shortName': self.number,
            'description': self.name,
            'longName': self.name
        }

    def is_valid(self):
        return self.number != OBAConstants.UNKNOWN

    def get_plain_route_number(self):
        if self.number == OBAConstants.UNKNOWN:
            return self.id
        raw_id = self.number
        if self.id.startswith(OBAConstants.CT + '_5'):
            # Sound Transit routes 51X and 53X are considered Community Transit routes in OBA
            return raw_id
        elif self.id.startswith(OBAConstants.CT + '_'):
            raw_id = OBAConstants.CT_LINE_INDICATOR + raw_id
        elif self.id.startswith(OBAConstants.PT + '_'):
            raw_id = OBAConstants.PT_LINE_INDICATOR + raw_id
        return raw_id

    def get_printed_number(self):
        raw_id = self.get_plain_route_number()
        for route_desc in OBAConstants.SHORT_NAME_EXCEPTIONS:
            if self.number == OBAConstants.SHORT_NAME_EXCEPTIONS[route_desc]:
                return "%s (%s)" % (raw_id, route_desc)
        return raw_id

    def get_raw_number(self):
        return self.number
