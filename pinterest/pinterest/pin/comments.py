


class comments(object):
    def __init__(self):
        self._commentid = None
        self._comment = None
        self._usercomid = None
        self._pincommentid = None


    @property
    def commentid(self):
        return self._commentid

    @property
    def comment(self):
        return self._comment

    @property
    def usercomid(self):
        return self._usercomid

    @property
    def pincommentid(self):
        return self._pincommentid

    @commentid.setter
    def x(self, value):
        self._commentid = value

    @comment.setter
    def x(self, value):
        self._comment = value

    @usercomid.setter
    def x(self, value):
        self._usercomid = value

    @pincommentid.setter
    def x(self, value):
        self._pincommentid = value

    @commentid.deleter
    def x(self):
        del self._commentid

    @comment.deleter
    def x(self):
        del self._comment

    @usercomid.deleter
    def x(self):
        del self._usercomid

    @pincommentid.deleter
    def x(self):
        del self._pincommentid

