class Date:
    def __init__(self,year,month,day):
        self.day = day
        self.month = month
        self.year = year

    @property
    def time(self):
        return "{0}-{1}-{2}".format(
            self.year,
            self.month,
            self.day
        )

    @classmethod
    def createDate(cls,date):
        year, month, day = map(str, date.split('-'))
        return cls(year, month, day)

    @staticmethod
    def is_month_validate(month):
        return int(month) <= 12 and int(month) >= 1

