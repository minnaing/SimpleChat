import sys, threading
sys.path.append("..")
import config

class ChatRoom:
    def __init__(self, room):
        self.name = room
        self.user = []

    def add_user(self, name):
        if name in self.user:
            return 'ERROR'
        else:
            self.user.append(name)

    def del_user(self, name):
        if name in self.user:
            self.user.remove(name)
        else:
            return 'ERROR'

    def broadcast(self, msg):
        pass


class Error:
    """
    100: --- Wrong Protocol, Error Parsing Message ---
    101: Invalid Protocol           // can't parse json
    102: Invalid Data provided      // value error
    200: --- Name Related Error ---
    201: Empty Name                 // When send message, name should be set
    202: Duplicated Name            // When you acquire name
    203: Invalid User Name          // Not registered name
    300: --- Room Related Error ---
    301: Empty Room                 // When message send, room should be set
    302: Invalid Room               // Invalid room to join
    400: ---
    """
    def __init__(self):
        pass


class Msg:
    def __init__(self):
        self.user = ''      # User should have name
        self.room = ''      # User should have room
        self.msg = ''       # if user and room are valid: msg success
        self.error = ''     # True = 0 or False > 1
        self.state = ''     # [name, room, msg]

    @staticmethod
    def parse(self, s):
        pass

    @staticmethod
    def json(self):
        data = {'data': self.user, 'room': self.room, 'msg': self.msg, 'error': self.error, 'state': self.state}
        return data

def process_query(s, data):
    if data[0] == '\\':
        data = data[1:]
        if data == 'rooms':
            s.send('rooms !!!')
        elif data == 'join':
            s.send('join !!!')
        elif data == 'leave':
            s.send('leave !!!')
        elif data == 'quit':
            s.send('quit !!!')
    else:
        s.send(data)


class ChatHandler(threading.Thread):
    def __init__(self, client_socket, address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        self.buffer_size = config.BUFFER_SIZE
        self.chat_room = ''
        self.username = ''
        self.state = ''
        print "Connection: ", self.address, " has been initiated."

    def run(self):
        while True:
            data = self.client_socket.recv(self.buffer_size)
            if data:
                #self.client_socket.send(data)
                #process_query(self.client_socket, data)
                if data[0] == '\\':
                    data = data[1:]
                    if data == 'rooms':
                        self.client_socket.send(self.chat_room)
                    elif data == 'join chat':
                        pass
                    elif data == 'leave':
                        pass
                else:
                    self.client_socket.send(data)
            else:
                self.client_socket.close()
                print "Connection: ", self.address, " closed."
                break
