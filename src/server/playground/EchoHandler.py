import sys, threading, select, socket
import config


class EchoHandler(threading.Thread):
    def __init__(self, client_socket, address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        self.buffer_size = config.BUFFER_SIZE
        print "Connection: ", self.address, " has been initiated."

    def run(self):
        while True:
            data = self.client_socket.recv(self.buffer_size)
            if data:
                self.client_socket.send(data)
            else:
                self.client_socket.close()
                print "Connection: ", self.address, " closed."
                break

class Server:
    def __init__(self):
        self.host = ''
        self.port = config.PORT
        self.backlog = config.BACKLOG
        self.buffer_size = config.BUFFER_SIZE
        self.server_socket = None
        self.threads = []

    def __server_socket_init(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind( (self.host, self.port) )
            self.server_socket.listen(self.backlog)
            print "Server is listening on port ", self.port, " ... "
        except socket.error, (value, message):
            if self.server_socket:
                self.server_socket.close()
            print "ERROR: Unable to create server socket."
            print value, message
            sys.exit(1)

    def run(self):
        self.__server_socket_init()
        inputs = [self.server_socket, sys.stdin]
        while True:
            readable, writable, exception = select.select(inputs,[],[])
            for s in readable:
                if s == self.server_socket:
                    client_socket, address = self.server_socket.accept()
                    response = EchoHandler(client_socket, address)
                    response.start()
                    self.threads.append(response)
                elif s == sys.stdin:
                    not_use = sys.stdin.readline()
                    break

        # Closing
        self.server_socket.close()
        print "Server shutdowned."
        for c in self.threads:
            c.join()

if __name__ == "__main__":
    s = Server()
    s.run()
