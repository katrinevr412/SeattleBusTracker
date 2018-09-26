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
            is_on_same_route, better_line = Formatters._is_on_same_route(last_record, record)
            if not is_on_same_route:
                last_record = record
                cleaned_record.append(record)
            else:
                last_record = better_line
        return cleaned_record

    @staticmethod
    def _is_on_same_route(line1, line2):
        if not line1:
            return False, line2
        cleaned_line1 = Formatters._clean_route_headline(line1)
        cleaned_line2 = Formatters._clean_route_headline(line2)
        if cleaned_line1[:10] != cleaned_line2[:10]:
            return False, line2
        elif len(cleaned_line1) > len(cleaned_line2):
            return True, line1
        else:
            return True, line2

    @staticmethod
    def _clean_route_headline(line):
        return line.lower().replace('rapidride a line to', '671') \
            .replace('rapidride b line to', '672') \
            .replace('rapidride c line to', '673') \
            .replace('rapidride d line to', '674') \
            .replace('rapidride e line to', '675') \
            .replace('rapidride f line to', '676') \
            .replace('-', '').replace(' ', '')
