import datetime


class DatetimeService:
    @staticmethod
    def get_current_date_and_time() -> datetime:
        return datetime.now()
