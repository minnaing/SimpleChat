from DB import USERS, ROOMS

# Communication Channel
def send(to, msg):
    to.send(msg + '\n')


def broadcast(to, msg, exclude=[]):
    for sock in to:
        if sock not in exclude:
            send(sock, msg)


def send_sys_msg(to, msg):
    to.send("%s : %s" %('SERVER', msg))


def broadcast_sys_msg(to, msg, exclude=[]):
    for sock in to:
        if sock not in exclude:
            send_sys_msg(sock, msg)


def list_rooms():
    return ROOMS.keys()


def help():
    return '\n"\\rooms"               : show all active rooms\n' \
           '"\\leave"               : for leaving the chat room\n' \
           '"\\quit"                : for exiting from the server\n' \
           '"\\whoami"              : showing your name, active chat room etc\n' \
           '"\\rename [new_name]"   : changing your name\n' \
           '"\\peer"           : show people in your current chat room\n'
    # '"\\w [username] [msg]   : private message to the user\n' !!!! Later


def get_all_users():
    result = []
    for s in USERS.keys():
        if USERS[s].get('name', False):
            # no name ; skip
            break
        else:
            result.append(USERS[s]['name'])
    return result
