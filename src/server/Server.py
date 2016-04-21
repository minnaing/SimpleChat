
import socket
import select
import sys
import config
from User import User, UserState
from Helper import *

__author__ = 'hannaing'

ALL_CONNECTION = []


class Server:
    def __init__(self):
        self.host = config.IP_ADDR
        self.port = config.PORT
        self.backlog = config.BACKLOG
        self.buffer_size = config.BUFFER_SIZE
        self.server_socket = None

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
        while True:
            readable, writable, exception = select.select(ALL_CONNECTION, [], [])
            for sock in readable:
                if sock == self.server_socket:
                    # New Connection
                    client_socket, address = self.server_socket.accept()
                    ALL_CONNECTION.append(client_socket)
                    User.add_user(client_socket)
                    print 'Connect ', address, 'success !'
                    send_sys_msg(client_socket, 'Welcome !\n Your name : ')
                elif sock == sys.stdin:
                    # not_use = sys.stdin.readline()
                    break
                else:  # Existing User
                    data = sock.recv(config.BUFFER_SIZE)
                    user = User(sock)

                    if len(data) > 1 and data[0] == '\\':
                        command = data[1:].strip()
                        # \room \join \leave \quit

                        if command == 'rooms':
                            send_sys_msg(sock, ', '.join(list_rooms()) + '\n')

                        elif command == 'help':
                            send_sys_msg(sock, help())

                        elif command == 'whoami':
                            send_sys_msg(sock, user.more())

                        elif command == 'peer':
                            send_sys_msg(sock, str(user.get_peer(name=True)) + '\n')

                        elif command == 'leave':
                            if user.get_status() == UserState.SESSION:
                                broadcast_sys_msg(user.get_peer(), 'User "%s" leave the room.\n' % user.get_name(), [sock])
                            user.leave()
                            msg = "Would you like to join new room ?\n So far %s available. \n " \
                                  "Choose the Room : " % list_rooms()
                            send_sys_msg(sock, msg)

                        elif command == 'quit':
                            send_sys_msg(sock, 'BYE\n')
                            if user.get_status() == UserState.SESSION:
                                broadcast_sys_msg(user.get_peer(), 'User "%s" logoff.\n' % user.get_name(), [sock])
                            ALL_CONNECTION.remove(sock)
                            user.logoff()

                        elif len(command.split(" ")) > 1:
                            # command, opt == command.split(" ", 1)
                            temp = command.split(" ")
                            command = temp[0].strip()

                            if command == 'rename':
                                old = user.get_name()
                                if user.rename_name(temp[1]):
                                    msg = 'Rename from "%s" to "%s"\n' % (old, user.get_name())
                                    send_sys_msg(sock, msg)
                                    broadcast_sys_msg(user.get_peer(), msg, [sock])

                        else:
                            send_sys_msg(sock, 'Invalid command "\\%s"\n Try "\\help" to see more option.' % command)
                    else:
                        data = data.strip()
                        if user.get_status() == UserState.ANONYMOUS:
                            if user.set_name(data):
                                send_sys_msg(sock, 'Would you like to join the room ?\n So far %s available. \n'
                                                   ' Room : ' % list_rooms())
                            else:
                                send_sys_msg(sock, 'The name you provided is invalid or taken. Try new one ...\n'
                                                   'Your name : ')

                        elif user.get_status() == UserState.REGISTERED:
                            if user.set_room(data):
                                send_sys_msg(sock, 'Welcome to "%s". You are ready to chat.\n' % user.get_room())
                                broadcast_sys_msg(user.get_peer(),
                                                  'New User "%s" join the room.\n' % user.get_name(), [sock])
                            else:
                                send_sys_msg(sock, 'There is no such room named "%s". \n So far %s available. \n '
                                                   'Choose the room : ' % (data, list_rooms()))

                        elif user.get_status() == UserState.SESSION:
                            msg = '%s @ %s :: %s' % (user.get_name(), user.get_room(), data)
                            broadcast(user.get_peer(), msg)

                        else:
                            # No such case; Should raise error
                            pass

        # Closing
        self.server_socket.close()
        print "Server is shutting down ... BYE !"
        for c in self.threads:
            c.join()


if __name__ == "__main__":
    s = Server()
    s.run()
