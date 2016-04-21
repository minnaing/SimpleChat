import socket, sys, select
sys.path.append("../server")
import config


__author__ = 'hannaing'

BUFFER = config.BUFFER_SIZE
HOST = (config.IP_ADDR, config.PORT)

print " ### Connected to ", HOST, " ### "
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(4)
s.connect(HOST)

while True:
    all_sock = [sys.stdin, s]
    read_sock, write_sock, error = select.select(all_sock , [], [])
    for sock in read_sock:
        if sock == s:
            data = sock.recv(BUFFER)
            if not data:
                sys.exit()
            else:
                print data,
        else:
            msg = sys.stdin.readline()
            s.send(msg)
s.close()

