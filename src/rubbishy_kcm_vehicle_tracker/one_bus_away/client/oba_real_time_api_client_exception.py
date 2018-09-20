import httplib


class OneBusAwayRealTimeAPIClientException(Exception):

    def __init__(self, message, status_code=httplib.NOT_FOUND):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return 'OBA API exception %d: %s' % (self.status_code, self.message)
