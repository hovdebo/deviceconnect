
class FitbitApiClass:

    def __init__(self, json_dict):
        self._dict = json_dict
        self._df = None

    @classmethod
    def url(cls, user, date):
        raise NotImplementedError()

    @property
    def dataframe(self):
        return self._df

    @property
    def json(self):
        return self._dict


class FitbitSummary(FitbitApiClass):
    def __init__(self, json_dict):
        super().__init__(json_dict)
        self._date = None

    @property
    def date(self):
        return self._date

    @classmethod
    def url(cls, user, date):
        raise NotImplementedError()


class FitbitIntraday(FitbitApiClass):
    def __init__(self, json_dict):
        super().__init__(json_dict)
        self._date = None
        self._summary = None

    @property
    def date(self):
        return self.summary.date

    @property
    def summary(self):
        return self._summary

    @classmethod
    def url(cls, user, date):
        raise NotImplementedError()
