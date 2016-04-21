
import socket, select, sys, threading
sys.path.append("..")
import config

__author__ = 'hannaing'

USERS = {}
ALL_CONNECTION = []

def send(msg, to):
    to.send("%-24s : %s" % (to, msg))


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



def broadcast(msg, src, to, exclude):
    for sock in to:
        if sock not in exclude:
            sock.send("%-24s : %s" % (src, msg))


def logoff(who, to, exclude):
    print to
    for sock in to:
        if sock not in exclude:
            sock.send("%-24s : %s" % ("SERVER", "Logoff"))
    who.close()
    ALL_CONNECTION.remove(who)


class Server:
    def __init__(self):
        self.host = config.IP_ADDR
        self.port = config.PORT
        self.backlog = config.BACKLOG
        self.buffer_size = config.BUFFER_SIZE
        self.server_socket = None
        self.threads = []

    def __server_socket_init(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.backlog)
            print "Server is listening on port ", self.port, " ... "
            ALL_CONNECTION.append(self.server_socket)
        except socket.error, (value, message):
            if self.server_socket:
                self.server_socket.close()
            print "ERROR %d: %s" % (value, message)
            print " >>> Unable to create server socket."
            sys.exit(1)

    def run(self):
        self.__server_socket_init()
        #inputs = [self.server_socket]
        while True:
            readable, writable, exception = select.select(ALL_CONNECTION, [], [])
            for sock in readable:
                if sock == self.server_socket:
                    # New
                    client_socket, address = self.server_socket.accept()
                    ALL_CONNECTION.append(client_socket)
                    print 'Connect ', address, 'success !'
                    broadcast('New User %s:%s connect.\n' % address, 'SERVER', ALL_CONNECTION, [self.server_socket,client_socket])
                elif s == sys.stdin:
                    not_use = sys.stdin.readline()
                    break
                else:  # Existing User
                    #data = sock.recv(config.BUFFER_SIZE)
                    '''
                    if data:
                        print address, ':', data,
                        if data.strip() == 'exit':
                            #sock.close()
                            #ALL_CONNECTION.remove(sock)
                            logoff(sock, ALL_CONNECTION, [sock, self.server_socket])
                        #elif data.strip() ==
                        else:
                            broadcast(data, address, ALL_CONNECTION, [self.server_socket])
                    else:
                        if sock in ALL_CONNECTION:
                            sock.close()
                            ALL_CONNECTION.remove(sock)
                            broadcast('%s:%s logoff.\n' % address, 'SERVER', ALL_CONNECTION, [self.server_socket])
                    '''
                    client_socket, address = self.server_socket.accept()
                    response = ChatHandler(client_socket, address)
                    response.start()
                    self.threads.append(response)


        # Closing
        self.server_socket.close()
        print "Server is shutting down ... BYE !"
        for c in self.threads:
            c.join()


if __name__ == "__main__":
    s = Server()
    s.run()
