


class User(object):
    def __init__(self):
        self._id = None
        self._name = None
        self._username = None
        self._password = None


    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @id.setter
    def x(self, value):
        self._id = value

    @name.setter
    def x(self, value):
        self._name = value


    @username.setter
    def x(self, value):
        self._username = value

    @password.setter
    def x(self, value):
        self._password = value

    @id.deleter
    def x(self):
        del self._id

    @name.deleter
    def x(self):
        del self._name

    @username.deleter
    def x(self):
        del self._username

    @password.deleter
    def x(self):
        del self._password


