


class Pin(object):

    def __init__(self):
        self._pinid = None
        self._pinname = None
        self._pinurl = None
        self._boardid = None

    @property
    def pinid(self):
        return self._pinid

    @property
    def pinname(self):
        return self._pinname

    @property
    def pinurl(self):
        return self._pinurl

    @property
    def boardid(self):
        return self._boardid

    @pinid.setter
    def x(self, value):
        self._pinid = value

    @pinname.setter
    def x(self, value):
        self._pinname = value

    @pinurl.setter
    def x(self, value):
        self._pinurl = value

    @boardid.setter
    def x(self, value):
        self._boardid = value

    @pinid.deleter
    def x(self):
        del self._pinid

    @pinname.deleter
    def x(self):
        del self._pinname

    @pinurl.deleter
    def x(self):
        del self._pinurl

    @boardid.deleter
    def x(self):
        del self._boardid


