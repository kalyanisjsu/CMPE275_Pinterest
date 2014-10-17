import couchdb
import json
import random
from bottle import HTTPError

class CreateDB(object):

    def getAllPins(self):
        """
        1. Get All Pins
        """
        server=couchdb.Server()
        db=server['pins']
        pins = {}
        all_pins=[]
        for db_object in db:
            doc=db[db_object]
            #Create dictionary object
            pin = {}
            pin['pin_id'] = doc['pinid']
            pin['pin_name'] = str(doc['pinname'])
            pin['pin_url'] = str(doc['pinurl'])
            all_pins.append(pin)
        pins['pins'] = all_pins
        return json.dumps(pins)

    def getAllBoards(self):
        """
        2. Get All Boards
        """
        server = couchdb.Server()
        db = server['boards']
        all_boards = []
        boards = {}
        for db_object in db:
            doc = db[db_object]
            #creating dictionary object
            board = {}
            board['board_id'] = doc['board_id']
            board['board_name'] = str(doc['board_name'])
            all_boards.append(board)
        #return list of dictionaries
        boards['boards'] = all_boards
        return json.dumps(boards)

    def getOneBoard(self,board_id):
        """
        3. Get one board
        """
        server = couchdb.Server()
        db = server['pins']
        pins = {}
        all_pins = []
        for db_object in db:
            doc = db[db_object]
            for boardobj in doc['boardid']:
                if str(boardobj) == str(board_id):
                    pin = {}
                    pin['pin_id'] = doc['pinid']
                    pin['pin_name'] = str(doc['pinname'])
                    pin['pin_url'] = str(doc['pinurl'])
                    all_pins.append(pin)
        pins['pins'] = all_pins
        return json.dumps(pins)


    def getOnePin(self,pin_id):
        """
        4. Get one pin
        """
        pin_url=""
        server=couchdb.Server()
        db=server['pins']
        pin_url =''
        for db_object in db:
            doc=db[db_object]
            if str(doc['pinid'])==str(pin_id):
                pin_url = str(doc['pinurl'])
                break
        if pin_url=='':
            #No Pin found
            pin={}
            pin['pin_url']=''
            return json.dumps(pin)
        else:
            pin={}
            pin['pin_url']=pin_url
            pin['pin_name'] = doc['pinname']
            all_comments=[]
            db=server['comments']
            for db_object in db:
                doc=db[db_object]
                if str(doc['pinid'])== str(pin_id):
                    comment={}
                    comment['usercomid']=doc['usercomid']
                    comment['comment']=doc['comment']
                    all_comments.append(comment)
            #result.append(all_comments)

        pin['comments'] = all_comments
        return json.dumps(pin)

    def insertUser(self, user):
        """
        5. Register/Signup User
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        userid_db = 0
        for dbObj in db:
            doc = db[dbObj]
            userid_db = doc['id']
            if doc['username'] == user._username:
                return ""

        user._id = int(userid_db)+1
        print user.name
        print user.username
        print user.password
        doc_id, doc_rev = db.save({'id': str(user.id), 'name': user.name, 'username': user.username, 'password': user.password})
        doc = db[doc_id]
        userData = {}
        userData['user_id'] = doc['id']
        userData['name'] = str(doc['name'])
        userData['username'] = str(doc['username'])
        return json.dumps(userData)

    def retrieveUser(self, user):
        """
        6. Login
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['users']
        for dbObj in db:
            doc = db[dbObj]
            if doc['username'] == user._username:
                 if doc['password'] == user._password:

                     userData = {}
                     userData['user_id'] = doc['id']
                     userData['name'] = str(doc['name'])
                     userData['username'] = str(doc['username'])
                     return json.dumps(userData)
        #userData = {}
        #userData['user_id'] = "Null"
        #userData['username'] = "Wrong Username"
        #userData['password'] = "Wrong Password"
        #return json.dumps(userData)
        return ""


    def retrieveUserBoards(self, user_id):
        """
        7. Get User Boards #TODO here only one board is returned
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        boards = {}
        all_boards = []
        for dbObj in db:
            doc = db[dbObj]
            uid = doc['userId']

            if str(user_id) == str(uid):
                #user is found in db

                board = {}
                board['board_id'] = doc['board_id']
                board['board_name'] = str(doc['board_name'])
                all_boards.append(board)
                boards['boards'] = all_boards
        return json.dumps(boards)

        board = "No boards are created!!"
        return json.dumps(board)

    def insertPin(self, pin):
        """
        8. Upload Pin
        """
        server = couchdb.Server()
        db = server['pins']
        pin_id = db.save({'pinid': pin._pinid,'pinname': pin.pinname, 'pinurl': pin.pinurl, 'boardid':[]})
        pin_dict = {}
        pin_dict['pin_id'] = pin.pinid
        return json.dumps(pin_dict)

    def returnPinid(self):
        server = couchdb.Server()
        db = server['pins']
        max_id = 0
        for dbObj in db:
            doc = db[dbObj]
            max_id = doc['pinid']
        return int(max_id) + 1

    def insertBoard(self, board):
        """
        9. Create Board
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        boardid_db = 0
        for dbObj in db:
            doc = db[dbObj]
            boardid_db = doc['board_id']

        board._board_id = int(boardid_db)+1
        doc_id, doc_rev = db.save({'board_id': board._board_id, 'board_name': board._board_name, 'userId': board._userId})
        board_dict = {}
        board_dict['board_id'] = board._board_id
        return json.dumps(board_dict)

    #todo what is the response to be returned? not mentioned in standards doc
    def updatePin(self,pin_id,userid,boardid):
        """
        10. Attach Pin
        """
        server=couchdb.Server()
        db=server['pins']
        for db_object in db:
            doc=db[db_object]
            if str(doc['pinid'])== str(pin_id):
                boards = doc['boardid']
                boards.append(boardid)
                #doc.setdefault('boardid', []).append(boardid)
                doc['boardid'] = boards
                db.save(doc)
        return self.getOneBoard(boardid)

    def deleteBoard(self,boardid,user_id):
        """
        11. Delete Board
        """
        server = couchdb.Server()  # insert hostname and port 5984 if db is not on local machine
        db = server['boards']
        for dbObj in db:
            doc= db[dbObj]
            if str(doc['board_id']) == str(boardid):
                if str(doc['userId']) == str(user_id):
                    db.delete(doc)
                    self.deleteboardfrompin(boardid)
                    return json.dumps("Deleted Board: " + boardid)
                else:
                    return json.dumps("Message: Only Created Board user can delete the board")
        return json.dumps("Message: Board id doesnt exist")

    def insertComments(self,comments):
        """
        12. Add Comment
        """
        server = couchdb.Server()
        db = server['comments']
        comment_id = db.save({'comment': comments.comment, 'usercomid':comments.usercomid, 'pinid':comments.pincommentid})
        return "Done"

    def isvaliduser(self,userid):
        """
        To check if the user id is valid
        """
        server = couchdb.Server()
        db = server['users']
        self.flag = False
        for dbObj in db:
             doc = db[dbObj]
             if str(userid) == str(doc['id']):
                self.flag = True
                break
        return self.flag

    def deleteboardfrompin(self,board_id):
        server = couchdb.Server()
        db = server['pins']
        boards = []
        for db_object in db:
            doc = db[db_object]
            for board in doc['boardid']:
                if(str(board) == str(board_id)):
                    print boards
                    boards = doc['boardid']
                    boards.remove(board_id)
                    doc['boardid'] = boards
                    db.save(doc)
                    break


