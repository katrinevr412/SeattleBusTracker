class IVehicle:
    """
        An interface for Vehicle class.
    """
    def __init__(self, id=''):
        self.id = id

    def get_route_number(self):
        return "0"

    def get_line_name(self):
        return "Unknown"

    def get_id(self):
        return str(self.id)
