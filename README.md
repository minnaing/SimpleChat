# Simple Chat

Multi user, multi chat room 

## Installation
    git clone https://github.com/minnaing/SimpleChat.git
    cd SimpleChat/src/server
    python Server.py
    # use \help to see supported command

## TODO
- fix the bugs
- private messaging
- implement with DB
- Encryption

## Notes:
- client.py is not stable. Just use telnet. If client.py is stable enough, we plan to add encryption feature.

## Possible bugs:
- if message size is greater than 65536
- socket.send(), socket.recv() on retired socket // wrap with try, except
- client.py is not stable

## State machine
![Simple Stage of user status](docs/UserState.png)
