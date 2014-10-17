"""

Using bottle (python) RESTful web service.

"""

import time
import socket
import os
import User
import random
import json
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

# bottle framework
from bottle import request, response, route, run, template, get, post, error,HTTPError
from couchdatabase import CreateDB

import Board
import Pin
import comments

# setup the configuration for our service

def setup(base, conf_fn):
    print '\n**** service initialization ****\n'
    global db, user, signin_done, pin , board, comment
    db = CreateDB()
    user = User.User()
    pin = Pin.Pin()
    comment = comments.comments()
    signin_done = 0
    board = Board.Board()
	
@route('/')
def root():
    return 'welcome to our website'

@route('/v1/ping', method='GET')
def ping():
    return 'ping %s - %s' % (socket.gethostname(), time.ctime())

@route('/v1/reg', method='POST')
def signup():

    jsonBody=request.body.read()
    jsonObj=json.loads(jsonBody)
    user._name = jsonObj['name']
    print user._name
    user._username = jsonObj['username']
    print user._username
    user._password = jsonObj['password']
    userResponse = db.insertUser(user)
    if(userResponse.__len__() < 1):
        return HTTPError(404)
    response.set_header("content-type", "application/json")
    response.body = userResponse
    print "***Response returned is:\n"
    print response.status
    print response.body
    print "\n***"
    return response
    #return "Sign Up Successfully!!! User ID is " + str(uid)


@route('/v1/login', method='POST')
def signin():
    jsonBody=request.body.read()
    jsonObj=json.loads(jsonBody)
    user._username = jsonObj['username']
    user._password = jsonObj['password']
    userResponse = db.retrieveUser(user)
    if(userResponse.__len__() < 1):
        return HTTPError(401)
    response.set_header("content-type", "application/json")
    response.body = userResponse
    print "***Response returned is:\n"
    print response.status
    print response.body
    print "\n***"
    return response


@route('/v1/user/:user_id', method='GET')
def getuserboards(user_id):
    if(db.isvaliduser(user_id)):
        user_boards = db.retrieveUserBoards(user_id)
        if not user_boards:
            return
        response.set_header("content-type","application/json")
        response.body = user_boards
        print "***Response returned is:\n"
        print response.status
        print response.body
        print "\n***"
        return response
    else:
        return erroruser()

@route('/v1/user/:user_id/board', method='POST')
def createBoard(user_id):
    print "Inside the creating board  %s" %user_id
    jsonBody=request.body.read()
    jsonObj=json.loads(jsonBody)

    for key in sorted(request.forms.iterkeys()):
       print "%s=%s" % (key, request.forms[key])
    if(db.isvaliduser(user_id)):
        print "Creating board for user -> " + user_id
        id = random.randint(1, 100)
        board._board_id = id
        print str(board._board_id) + "\n"

        board._board_name = jsonObj['boardname'] # request.forms.get('boardName')
        print "BoardName: " + board._board_name
        board._userId = user_id
        new_board = db.insertBoard(board)
        response.set_header("content-type","application/json")
        response.body = new_board
        print "***Response returned is:\n"
        print response.status
        print response.body
        print "\n***"
        return response
    else:
        return erroruser()

@route('/v1/user/:user_id/board/:board_id', method='DELETE')
def deleteBoard(user_id,board_id):
    try :
        if(db.isvaliduser(user_id)):
            print "Deleting board boardId: " +  str(board_id) +" for user -> " + str(user_id)
            boardid= board_id
            #curl -i -H "Accept: application/json" -H "X-HTTP-Method-Override: DELETE" -X DELETE http://localhost:8080/v1/user/14/board/96
            del_board = db.deleteBoard(boardid,user_id)
            response.set_header("content-type","application/json")
            response.body = del_board
            print "***Response returned is----->deleteBoard:\n"
            print response.status
            print response.body
            print "\n***"
            return response
        else:
            return erroruser()
    except:
        return erroruser()
    #return "Deleting board boardId: " +  str(board_id) +" for user -> " + str(user_id) + "\n"

@route('/v1/boards',method='GET')
def getAllBoards():
    boards = db.getAllBoards()
    response.set_header("content-type","application/json")
    response.body = boards
    print "***Response returned is:\n"
    print response.status
    print response.body
    print "\n***"
    return response

@route('/v1/boards/:board_id', method='GET')
def getOneBoard(board_id):
    print 'get one board'
    board = db.getOneBoard(board_id)
    print 'all pins in board',board_id, '->', board
    response.set_header("content-type","application/json")
    response.body = board
    print "***Response returned is:\n"
    print response.status
    print response.body
    print "\n***"
    return response


#TODO create response
@route('/v1/user/:user_id/pin/upload', method='POST')
def addimage(user_id):
    if(db.isvaliduser(user_id)):
        upload = request.files.get('content')
        name, ext = os.path.splitext(upload.filename)

        if ext not in ('.png','.jpg','.jpeg'):
            return 'File extension not allowed.'
        print ext

        #here check if the directory is existing
        #save_path = '/Users/poojasrinivas/Desktop/275/save'
        save_path = 'C:\\tmp'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        upload.save(save_path)
        addedPinPath = save_path + '\\' + name +ext
        #addedPinPath = save_path + '/' + name +ext

        boto.set_stream_logger('boto')
        #TODO removed s3 line
        s3 =  S3Connection('AKIAIZGBRZFQJ6ZO7O6Q', 'y5zskvZW+yyH0OuUlbOuq6alNQvQzalhLarp2MAv')
        #s3 = boto.connect_s3()

        pin._pinid = db.returnPinid()
        print 'Connected to S3'
        bucket = s3.get_bucket('bucket275')


        #create key
        k=Key(bucket)
        k.key=pin._pinid # TODO set auto generated pin id here
        print addedPinPath
        k.set_contents_from_filename(addedPinPath)
        time.sleep(2)

        #pin._pinid = '3' #TODO generate the pin id
        pin._pinname = name
        pin._pinurl='https://bucket275.s3.amazonaws.com/'+ str(pin._pinid)
        pin._boardid = ''

        pindetails = db.insertPin(pin)
        os.remove(addedPinPath)
        response.set_header("content-type","application/json")
        response.body = pindetails
        print "***Response returned is:\n"
        print response.status
        print response.body
        print "\n***"
        return response
    else:
        return erroruser()

@route('/v1/pins', method='GET')
def getAllPins():
    print 'Retrieving all pins...'
    pins=db.getAllPins()
    print "All pins ",pins
    response.set_header("content-type","application/json")
    response.body = pins
    print "***Response returned is:\n"
    print response.status
    print response.body
    print "\n***"
    return response

@route('/v1/pin/:pin_id',method='GET')
def getPin(pin_id):
    print 'Retrieving pin...'
    #pin_id=request.GET.get('pin_id')
    pin=db.getOnePin(pin_id)
    response.set_header("content-type","application/json")
    response.body = pin
    print "***Response returned is:\n"
    print response.status
    print response.body
    print "\n***"
    return response

#TODO what is response for this? not mentioned in standards doc
@route('/v1/user/:userid/board/:boardid',method='PUT')
def attachPin(userid,boardid):
    if(db.isvaliduser(userid)):
        jsonBody=request.body.read()
        jsonObj=json.loads(jsonBody)
        pin_id = jsonObj['pin_id']
        print "the pin id is " + pin_id
        res = db.updatePin(pin_id,userid,boardid)
        response.set_header("content-type","application/json")
        response.body = res
        print "***Response returned is:\n"
        print response.status
        print response.body
        print "\n***"
        return response
    else:
        return erroruser()


@route('/v1/user/:userid/pin/:pinid',method='POST')
def addComment(userid,pinid):
    if(db.isvaliduser(userid)):
        print "inside add comment"
        jsonBody=request.body.read()
        jsonObj=json.loads(jsonBody)
        comment._comment = jsonObj['comment']
        comment._usercomid = userid
        comment._pincommentid = pinid
        new_comm = db.insertComments(comment)
        response.set_header("content-type","application/json")
        response.body = new_comm
        print "***Response returned is:\n"
        print response.status
        print response.body
        print "\n***"
        return response
    else:
        return erroruser()

def erroruser():
    response.set_header("content-type","application/json")
    err = {}
    err['Error'] = "User Doesn't Exists"
    response.body = json.dumps(err)
    return response

@error(200)
def error200(error1):
    return 'OK'

@error(201)
def error201(error1):
    return 'Created'

@error(204)
def error204(error1):
    return 'No Content'

@error(400)
def error400(error1):
    return 'Bad Request'

@error(401)
def error401(error1):
    return 'Unauthorized Request, Wrong User id'

@error(404)
def error404(error1):
    return 'Username already exists'

@error(405)
def error405(error1):
    return 'Method Not Allowed'

@error(500)
def error500(error1):
    return 'Internal Server Error'


# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
#def __format(request):
    #for key in sorted(request.headers.iterkeys()):
    #   print "%s=%s" % (key, request.headers[key])

#    types = request.headers.get("Accept", '')
#    subtypes = types.split(",")
#    for st in subtypes:
#        sst = st.split(';')
#        if sst[0] == "text/html":
#            return Room.html
#        elif sst[0] == "text/plain":
#            return Room.text
#        elif sst[0] == "application/json":
#            return Room.json
#        elif sst[0] == "*/*":
#            return Room.json

            # TODO
            # xml: application/xhtml+xml, application/xml
            # image types: image/jpeg, etc

    # default
#    return Room.html

#
# The content type on the reply
#
#def __response_format(reqfmt):
#    if reqfmt == Room.html:
#        return "text/html"
#    elif reqfmt == Room.text:
#        return "text/plain"
#    elif reqfmt == Room.json:
#        return "application/json"
#    else:
#        return "*/*"

        # TODO
        # xml: application/xhtml+xml, application/xml
        # image types: image/jpeg, etc
