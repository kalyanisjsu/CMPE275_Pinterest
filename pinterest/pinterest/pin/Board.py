

class Board(object):
    def __init__(self):
        self._board_id = None
        self._board_name = None
        self._username = None
        self._userId = None


    @property
    def board_id(self):
        return self._id

    @property
    def board_name(self):
        return self._name

    @property
    def username(self):
        return self._username
	
    @property
    def userId(self):
        return self._userId

    @board_id.setter
    def x(self, value):
        self._id = value

    @board_name.setter
    def x(self, value):
        self._name = value


    @username.setter
    def x(self, value):
        self._username = value
		
    @userId.setter
    def x(self, value):
        self._userId = value

    @board_id.deleter
    def x(self):
        del self._id

    @board_name.deleter
    def x(self):
        del self._name

    @username.deleter
    def x(self):
        del self._username
		
    @userId.deleter
    def x(self):
        del self._userId
