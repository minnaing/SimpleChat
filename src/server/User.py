from DB import USERS, ROOMS

class UserState:
    ANONYMOUS = "anonymous"
    REGISTERED = "registered"
    SESSION = "session"


# User Management
class User:
    @staticmethod
    def add_user(sock):
        USERS[sock] = {'status': UserState.ANONYMOUS}

    def __init__(self, sock):
        self.sock = sock
        self.info = USERS[sock]

    def get_status(self):
        return self.info['status']

    def get_name(self):
        return self.info['name']

    def get_room(self):
        return self.info['room']

    def set_status(self, status):
        USERS[self.sock]['status'] = status

    def set_name(self, name):
        name = name.strip()
        if not name.isalpha():
            return False
        for k in USERS:
            if USERS[k].get('name') == name:
                return False
        self.info['status'] = UserState.REGISTERED
        self.info['name'] = name
        return True

    def rename_name(self, name):
        # Should combine with set_name()
        name = name.strip()
        if not name.isalpha():
            return False
        for k in USERS:
            if USERS[k].get('name') == name:
                return False
        self.info['name'] = name
        return True

    def set_room(self, room):
        room = room.strip()
        if room in ROOMS.keys():
            self.info['status'] = UserState.SESSION
            self.info['room'] = room
            ROOMS[room].append(self.sock)
            return True
        else:
            return False

    def unset_room(self):
        self.info['status'] = UserState.REGISTERED
        self.info['room'] = ''

    def leave(self):
        if self.info['status'] == UserState.SESSION:
            ROOMS[self.info['room']].remove(self.sock)
            self.unset_room()

    def get_peer(self, name=False):
        if self.info['status'] == UserState.SESSION:
            if name:
                temp = []
                for sock in ROOMS[self.info['room']]:
                    if USERS[sock]['name']:
                        temp.append(USERS[sock]['name'])
                return temp
            else:
                # return sockets
                return ROOMS[self.info['room']]
        return []

    def logoff(self):
        if self.info['status'] == UserState.SESSION:
            ROOMS[self.info['room']].remove(self.sock)
        USERS.pop(self.sock)
        self.sock.close()

    def __str__(self):
        return self.sock

    def more(self):
        result = '\n'
        if self.info['status'] == UserState.REGISTERED:
            result += 'Name: %s\n' % self.info['name']
        elif self.info['status'] == UserState.SESSION:
            result += 'Name: %s\n' % self.info['name']
            result += 'Room: %s\n' % self.info['room']
        return result


