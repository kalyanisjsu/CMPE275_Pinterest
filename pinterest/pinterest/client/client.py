import os
import socket
import httplib
import urlparse
import sys
import mimetypes
import json
from distutils import log
import webbrowser



try:
    bytes
except NameError:
    bytes = str


def b(str_or_bytes):
    if not isinstance(str_or_bytes, bytes):
        return str_or_bytes.encode('ascii')
    else:
        return str_or_bytes

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class ClientPy:

    def __init__(self):
        if len(sys.argv) > 1:
            self.host = sys.argv[1]
            self.url = ''
            self.flg = False
            self.userid = 0
            cmd = self.printusage()
            while(cmd <> '0'):
                    if cmd == '1':
                        self.signUp()
                        cmd = self.printusage()
                    elif cmd == '2':
                        self.signIn()
                        cmd = self.printusage()
                    elif cmd == '3':
                        self.getAllBoards()
                        cmd = self.printusage()
                    elif cmd == '4':
                        self.getAllPins()
                        cmd = self.printusage()
                    elif cmd == '5':
                        self.getBoard()
                        cmd = self.printusage()
                    elif cmd == '6':
                        self.getPin()
                        cmd = self.printusage()
                    elif cmd > 6 :
                        if(self.flg):
                            if cmd == '7':
                                self.getUserBoard()
                                cmd = self.printusage()
                            elif cmd == '8':
                                savepath = raw_input('\nEnter the path of the file to be copied :')
                                self.upload_file(savepath)
                                cmd = self.printusage()
                            elif cmd == '9':
                                self.createBoard()
                                cmd = self.printusage()
                            elif cmd == '10':
                                self.attachPin()
                                cmd = self.printusage()
                            elif cmd == '11':
                                self.addComment()
                                cmd = self.printusage()
                            elif cmd == '12':
                                self.deleteBoard()
                                cmd = self.printusage()
                            elif cmd > '12':
                                print "Please enter correct option!!!!"
                                cmd = self.printusage()
                        else:
                            print "Please enter correct option and login for more functions"
                            cmd = self.printusage()
            self.quitConnection()
        else:
            print "usage:", sys.argv[0],"[host ip] example 'x.x.x.x.'"

    def printusage(self):
        if(self.flg):
            print "Press the Key of Choice" \
                "\n1. Registration" \
                "\n2. Login" \
                "\n3. See All Boards" \
                "\n4. See All Pins" \
                "\n5. Get a Board (Requires Board ID)" \
                "\n6. Get a Pin (Requires Pin ID)" \
                "\n7. Get UserBoard" \
                "\n8. Upload pin" \
                "\n9. Create Board" \
                "\n10.Attach Pin" \
                "\n11.Add Comment" \
                "\n12.Delete Board" \
                "\n0. Quit"
        else:
            print "Press the Key of Choice" \
                "\n1. Registration" \
                "\n2. Login" \
                "\n3. See All Boards" \
                "\n4. See All Pins" \
                "\n5. Get a Board (Requires Board ID)" \
                "\n6. Get a Pin (Requires Pin ID)" \
                "\n0. Quit"
        cmd = raw_input("\nEnter option :")
        return cmd

    def signUp(self):
        name = raw_input("Enter Name : ")
        username = raw_input("Enter Username : ")
        password = raw_input("Enter Password : ")
        url = 'http://'+self.host+':8080/v1/reg'
        test = {
            'name' : name,
            'username' : username,
            'password' : password
        }
        bo = json.dumps(test).encode('utf-8')

        #body = "name="+name+"&username="+ username + "&password="+ password
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.connect()
            self.conn.putrequest("POST", url)
            self.conn.putheader('Accept', 'application/json')
            self.conn.putheader('Content-type','application/json-rpc;charset=utf-8')
            self.conn.putheader('Content-length', str(len(bo)))
            self.conn.endheaders()
            self.conn.send(bo)
        except socket.error, e:
            print(str(e), log.ERROR)
            return

        response = self.conn.getresponse()
        body = response.read()
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        if(response.status == 200):
            self.flg = True
            jsonobj = json.loads(str(body))
            self.userid = jsonobj['user_id']
            print "   Response Content:"
            for key in jsonobj:
                print "%15s \t=   %s" % (key, jsonobj[key])
        print ('\n   JSON Received:')
        print '%60s' % body
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()


    def signIn(self):
        username = raw_input("Enter Username : ")
        password = raw_input("Enter Password : ")
        url = 'http://'+self.host+':8080/v1/login'
        body={
             'username' : username,
             'password' : password
        }
        data = json.dumps(body).encode('utf-8')
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.connect()
            self.conn.putrequest("POST", url)
            self.conn.putheader('Accept', 'application/json')
            self.conn.putheader('Content-type','application/json-rpc;charset=utf-8')
            self.conn.putheader('Content-length', str(len(data)))
            self.conn.endheaders()
            self.conn.send(data)
        except socket.error, e:
            print(str(e), log.ERROR)
            return

        response = self.conn.getresponse()
        body = response.read()
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        if(response.status == 200):
            self.flg = True
            jsonobj = json.loads(str(body))
            self.userid = jsonobj['user_id']
            print "   Response Content:"
            for key in jsonobj:
                print "%15s \t=   %s" % (key, jsonobj[key])
        print ('\n   JSON Received:')
        print '%60s' % body
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def getAllBoards(self):
        print "**Get All Boards**"
        route_url = 'http://' + self.host + ':8080'
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('GET','/v1/boards')
        except socket.error, e:
            print(str(e), log.ERROR)
            return
        response = self.conn.getresponse()
        body = response.read()
        jsonobj = json.loads(str(body))
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        print "   Response Content:"
        print "%15s" % "Boards"
        for k in jsonobj['boards']:
           print "%20s = %s %15s = %s" % ("board_id",k['board_id'],"boardname",k['board_name'])
        print ('\n   JSON Received:')
        print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()


    def getAllPins(self):
        print "**Get All Pins**"
        route_url = 'http://' + self.host + ":8080"
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('GET','/v1/pins')
        except socket.error, e:
            print(str(e), log.ERROR)
            return
        response = self.conn.getresponse()
        print "\n***Response received:"
        body = response.read()
        jsonobj = json.loads(str(body))
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        print "   Response Content:"
        print "%15s" % "Pins"
        for k in jsonobj['pins']:
           print "%20s = %s %15s = %s %15s = %s" % ("pin_id",k['pin_id'],"pin_name",k['pin_name'],"pin_url", k['pin_url'])
        print ('\n   JSON Received:')
        print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def getBoard(self):
        print "**Get Board**"
        board_id = raw_input("\nEnter board ID that you want to view:")
        route_url = 'http://' + self.host + ":8080"
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('GET','/v1/boards/'+board_id)
        except socket.error, e:
            print(str(e), log.ERROR)
            return
        response = self.conn.getresponse()

        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        body = response.read()
        jsonobj = json.loads(str(body))
        print "   Response Content:"
        if(len(jsonobj) == 0):
            print "%15s" % "Empty Board"
        else:
            for k in jsonobj['pins']:
               print "%20s = %s %15s = %s %15s = %s" % ("pin_id",k['pin_id'],"pin_name",k['pin_name'],"pin_url", k['pin_url'])
            print ('\n   JSON Received:')
            print '%60s' % body
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def getPin(self):
        print "**Get Pin**"
        pin_id = raw_input("\nEnter pin ID that you want to view:")
        route_url = 'http://' + self.host + ":8080"
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('GET','/v1/pin/'+ pin_id)
        except socket.error, e:
            print(str(e), log.ERROR)
            return
        response = self.conn.getresponse()
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        body = response.read()
        if(body.__len__() > 0):
            jsonobj = json.loads(str(body))
            if(jsonobj['pin_url']==''):
                print("Pin ID could not be found!")
            else:
                print ('\n   JSON Received:')
                print '         %s' % (body)

                print "   Response Content:"
                print "%15s" % "Pins"
                for key in jsonobj:
                    print "%15s \t=   %s" % (key, jsonobj[key])
                #webbrowser.open(jsonobj['pin_url'])
                print ('\n   JSON Received:')
                print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def quitConnection(self):
        self.conn.close()
        return

    def getUserBoard(self):
        route_url = 'http://' + self.host + ":8080"
        #user_id = '3'
        print route_url
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('GET','/v1/user/'+str(self.userid))
        except socket.error, e:
            print(str(e), log.ERROR)
            return
        response = self.conn.getresponse()
        body = response.read()
        jsonobj = json.loads(str(body))
        print jsonobj
        if(len(jsonobj)<=0):
            print 'You have not created boards!'
        else:
            print "\nResponse Received:"
            print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
            print "   Response Content:"
            print "%15s" % "Boards"
            for k in jsonobj['boards']:
                print "%20s = %s %15s = %s" % ("board_id",k['board_id'],"boardname",k['board_name'])
            print ('\n   JSON Received:')
            print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def createBoard(self):
        print "**Create Board**"
        boardname = str(raw_input("\nEnter board name that you want to create:"))
        #userid = '27'
        data = {"boardname" : boardname}
        data_json = json.dumps(data).encode('utf-8')

        head = {'Content-type': 'application/json-rpc;charset=utf-8'}
        route_url = 'http://' + self.host + ":8080"
        print route_url
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('POST','/v1/user/'+str(self.userid) +'/board',body =data_json, headers = head )
        except socket.error, e:
            print(str(e), log.ERROR)
            return
        response = self.conn.getresponse()
        body = response.read()
        jsonobj = json.loads(str(body))
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        print "   Response Content:"
        for key in jsonobj:
           print "%15s \t=   %s" % (key, jsonobj[key])
        print ('\n   JSON Received:')
        print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()


    def attachPin(self):
        print "**Attaching Pin**"

        board_id = raw_input("\nEnter Board ID to which it has to be Pinned:")
        pin_id = raw_input("\nEnter Pin ID to which it has to be Pinned:")

        data = {"pin_id" : pin_id}
        data_json = json.dumps(data).encode('utf-8')

        head = {'Content-type': 'application/json-rpc;charset=utf-8'}
        route_url = 'http://' + self.host + ":8080"

        print route_url
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('PUT','/v1/user/'+str(self.userid) +'/board/'+ str(board_id),body =data_json, headers = head)

        except socket.error, e:
            print(str(e), log.ERROR)
            return

        response = self.conn.getresponse()
        body = response.read()
        jsonobj = json.loads(str(body))
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        print "   Response Content:"
        for key in jsonobj:
           print "%15s \t=   %s" % (key, jsonobj[key])
        print ('\n   JSON Received:')
        print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()


    def addComment(self):
        print "**Adding Comment**"
        pin_id = raw_input("\nEnter Pin ID:")
        comment = raw_input("\nEnter Comment:")
        route_url = 'http://' + self.host + ":8080"
        data = {"comment" : comment}
        data_json = json.dumps(data).encode('utf-8')
        head = {'Content-type': 'application/json-rpc;charset=utf-8'}
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('POST','/v1/user/'+str(self.userid) +'/pin/'+ str(pin_id),body =data_json,headers=head)

        except socket.error, e:
            print(str(e), log.ERROR)
            return

        response = self.conn.getresponse()
        body = response.read()
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        print ('    Message Received: %s') % body
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def deleteBoard(self):
        print "**Deleting Board**"
        board_id= str(raw_input("\nEnter Board ID for the board to be deleted:"))
        route_url = 'http://' + self.host + ":8080"
        head = {'Content-type': 'application/json'}
        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(route_url)
        self.conn = httplib.HTTPConnection(netloc)
        try:
            self.conn.request('DELETE','/v1/user/'+str(self.userid) +'/board/'+str(board_id) ,headers=head)

        except socket.error, e:
            print(str(e), log.ERROR)
            return

        response = self.conn.getresponse()
        body = response.read()
        jsonobj = json.loads(str(body))
        print "\nResponse Received:"
        print "%s %s %s \n%s"%("Status:",response.status, response.reason, response.msg)
        print ('\n   JSON Received:')
        print '         %s' % (body)
        print '\n'+ '-'*70 + '***************'+ '-'*70 + '\n'
        self.conn.close()

    def upload_file(self,savepath):
        url = 'http://'+self.host+':8080/v1/user/'+str(self.userid) +'/pin/upload'
        filename = savepath
        #files = {'file': open('image.jpg', 'rb')}
        content = open(filename, 'rb').read()

        data = {
            ':action': 'doc_upload',
            'content': (os.path.basename(filename), content),
        }

        boundary = b('--------------GHSKFJDLGDS7543FJKLFHRE75642756743254')
        sep_boundary = b('\n--') + boundary
        end_boundary = sep_boundary + b('--')
        body = []

        for key, values in data.items():
            # handle multiple entries for the same name
            if type(values) != type([]):
                values = [values]
            for value in values:
                if type(value) is tuple:
                    fn = b(';filename="%s"' % value[0])
                    value = value[1]
                else:
                    fn = b("")
                body.append(sep_boundary)
                body.append(b('\nContent-Disposition: form-data; name="%s"'%(key)))
                body.append(fn)
                body.append(b("\n\n"))
                body.append(b(value))
                if value and value[-1] == b('\r'):
                    body.append(b('\n'))  # write an extra newline (lurve Macs)
        body.append(end_boundary)
        body.append(b("\n"))
        body = b('').join(body)


        schema, netloc, url, params, query, fragments = \
            urlparse.urlparse(url)

        self.conn = httplib.HTTPConnection(netloc)

        try:
            self.conn.connect()
            self.conn.putrequest("POST", url)
            self.conn.putheader('Accept',
                           'image/jpeg')
            self.conn.putheader('Content-type',
                           'multipart/form-data; boundary=%s'%boundary)
            self.conn.putheader('Content-length', str(len(body)))
            self.conn.endheaders()
            self.conn.send(body)
        except socket.error, e:
            print(str(e), log.ERROR)
            return

        r = self.conn.getresponse()
        body = r.read()

        if r.status == 200:
            print "\nResponse Received:"
            print "%s %s %s \n%s"%("Status:",r.status, r.reason, r.msg)
            print "   Response Content:"
            jsonobj = json.loads(str(body))
            for key in jsonobj:
                print "%15s \t=   %s" % (key, jsonobj[key])
            print ('\n   JSON Received:')
            print '         %s' % (body)

        elif r.status == 301:
            location = r.getheader('Location')
            if location is None:
                location = 'http://packages.python.org/%s/' % meta.get_name()
            print('Upload successful. Visit %s') % (location)
        else:
            print('Upload failed (%s): %s') % (r.status, r.reason)

        print '-'*70, '**********', '-'*70

if __name__ == "__main__":
    sam = ClientPy()



