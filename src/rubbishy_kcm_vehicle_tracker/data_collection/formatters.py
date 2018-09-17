from datetime import datetime, timedelta
import pytz


class Formatters:

    @staticmethod
    def date_formatter():
        '''
            TODO:
            since we merge data every day at 4:10AM we need to apply an offset.
        :return:
        '''
        last_day = datetime.now(pytz.timezone('America/Los_Angeles')) + timedelta(hours=-4) + timedelta(minutes=-11)
        return last_day.strftime('%Y-%m-%d %a')

    @staticmethod
    def route_file_formatter(_file):
        """
            For route -> vehicle data, we remove all duplicates for one day record.
        :param _file:
        :return:
        """
        records = filter(lambda line: line, [line.strip() for line in _file.readlines()])
        return '\t'.join(Formatters._remove_duplicate(records))

    @staticmethod
    def vehicle_file_formatter(_file):
        """
            For vehicle -> route data, we only remove repeated adjacent patterns.
        :param _file:
        :return:
        """
        records = filter(lambda line: line, [line.strip() for line in _file.readlines()])
        return '\t'.join(Formatters._clean_adjacent_record(records))

    @staticmethod
    def _remove_duplicate(records):
        return sorted(list(set(records)))

    @staticmethod
    def _clean_adjacent_record(records):
        last_record = None
        cleaned_record = []
        for record in records:
            if record != last_record:
                last_record = record
                cleaned_record.append(record)
        return cleaned_record
