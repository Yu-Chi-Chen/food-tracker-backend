from datetime import datetime
import pytz


class DatetimeTool:

    @staticmethod
    def convert_to_utc(date_str):
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        dt = pytz.timezone('Asia/Taipei').localize(dt)
        dt = dt.astimezone(pytz.utc)

        return dt
