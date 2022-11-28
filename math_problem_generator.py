# Written by Chris

import zmq
import random
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:3000")


while True:
    #  Wait for next request from client
    message = socket.recv_string()
    print(f"Received request: '{message}'")

    categories = ['addition', 'subtraction', 'multiplication']
    if message in categories:

        if message == 'addition':
            key = {}
            # Generate 5 math addition problems
            for i in range(5):
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                answer = a + b
                key[f'{a} + {b}'] = answer

            json_object = json.dumps(key)
            print('Sending json file..')
            socket.send_json(json_object)

        elif message == 'subtraction':
            key = {}
            # Generate 5 math subtraction problems
            for i in range(5):
                a = random.randint(50, 100)
                b = random.randint(1, 49)
                answer = a - b
                key[f'{a} - {b}'] = answer

            json_object = json.dumps(key)
            print('Sending json file..')
            socket.send_json(json_object)

        elif message == 'multiplication':
            key = {}
            # Generate 5 math multi problems
            for i in range(5):
                a = random.randint(1, 20)
                b = random.randint(1, 10)
                answer = a * b
                key[f'{a} * {b}'] = answer

            json_object = json.dumps(key)
            print('Sending json file..')
            socket.send_json(json_object)

    else:
        print(f"Message: '{message}' not recognized.")
        socket.send(b'Message not recognized.')