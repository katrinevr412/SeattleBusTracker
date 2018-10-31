from global_constants import GlobalConstants
from oba_constants import OBAConstants
from kcm_constants import KCMConstants


class Instructions:

    INSTRUCTION_COLOR = 'yellow'
    ERROR_COLOR = 'red'

    def __init__(self):
        try:
            from termcolor import colored
            self.color_enabled = True
        except ImportError:
            self.color_enabled = False

    def print_instruction(self, api):
        if api == GlobalConstants.OBA_API:
            self.__print_oba_instruction()
        elif api == GlobalConstants.KCM_API:
            self.__print_kcm_instruction()
        else:
            self.__print_text("Bad API configuration. Allowed values are %s" % GlobalConstants.ALL_SUPPORTED_APIS, self.ERROR_COLOR)
            return False
        return True

    def __print_oba_instruction(self):
        self.__print_text("Track buses using OneBusAway API.")
        self.__print_text(" - Base tracking: enter one or more bases of the following, separated by space: %s" % OBAConstants.TRACKING_LINES_FOR_BASES.keys())
        self.__print_text("     c, n, s, e are central, north, south and east base of KingCountyMetro, respectively.")
        self.__print_text("     x means KCM special lines, and kcm is an alias for tracking all KCM lines.")
        self.__print_text("     stk, stc, stp are SoundTransit lines operated by KCM, Community Transit and Pierce Transit, respectively.")
        self.__print_text("     st is an alias for tracking all ST lines.")
        self.__print_text("     ct and pt mean Community Transit and Pierce Transit respectively.")
        self.__print_text("     Example: \"c e stk\" means tracking all central, east bases of KCM and Sound Transit bus routes running by KCM.")
        self.__print_text(" - Route tracking: enter one or more routes to track, separated by space. Routes can begin with a C or a P meaning "
              "Community transit or Pierce transit. Sound transit doesn't need prefix. ")
        self.__print_text("     Route tracking doesn't need an 'r' header command, but you can add it if you want to."
              "We will auto detect route tracking requests.")
        self.__print_text("     Example: \"241 554 P401\" means tracking all vehicles on King County Metro route 241, Sound Transit route 554 and"
              "Pierce Transit route 401.")
        self.__print_text(" - Vehicle tracking: enter at most %d vehicles to track, separated by space. Vehicle numbers can begin with a C or a P "
              "which have the same meanings in Route tracking." % GlobalConstants.VEHICLE_COMMAND_LIMIT)
        self.__print_text("     Vehicle tracking needs explicit header command, 'v'.")
        self.__print_text("     Example: \"v 1120 9801 P8059\" means tracking the following three buses: KCM vehicle 1120, ST vehicle 9801 and "
              "PT vehicle 8059.")

    def __print_kcm_instruction(self):
        self.__print_text("Track buses using KingCountyMetro real-time API.")
        self.__print_text(" - Base tracking: enter one or more bases of the following, separated by space: %s" % KCMConstants.ALL_VALID_TRACKING_BASES)
        self.__print_text("     c, n, s, e are central, north, south and east base of KingCountyMetro, respectively.")
        self.__print_text(" - Route tracking: enter one or more routes to track, separated by space. Only KCM and ST routes are supported in this API.")

    def __print_text(self, text, color=INSTRUCTION_COLOR):
        if self.color_enabled:
            from termcolor import colored
            print colored(text, color)
        else:
            print text
