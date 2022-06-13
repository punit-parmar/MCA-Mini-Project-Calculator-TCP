import socket
import re


def sanitizeExpression(exp):
    op = "+-*/%"
    opIndex = []
    clean = ''

    for i in range(len(exp)):
        if exp[i] in op:
            opIndex.append(i)
    opIndex.append(len(exp))

    k = 0
    i = 0
    while i < len(exp):
        if exp[i] == '0' and i != opIndex[k] - 1:
            i += 1
            continue
        else:
            clean = clean + exp[i:opIndex[k] + 1]
            i = opIndex[k]
            k += 1
        i += 1

    return clean


host = socket.gethostname()
port = 5000
print("Server is up and running...")

server = socket.socket()

server.bind((host, port))
server.listen(10)
print("listening to 10 concurrent requests...")
print("-----------------------------------")


while True:
    conn, addr = server.accept()
    print("Received Request from: ", addr)
    data = conn.recv(1024).decode()
    print("Request Received: ", data)
    data = sanitizeExpression(data)
    print("After Sanitization: ", data)

    result = ""
    try:
        if(data != ""):
            result = eval(data)
    except Exception as e:
        result = "Invalid Expression!!"
    print("Sending reply: ", result)

    conn.send(str(result).encode())
    conn.close()
    print("Connection Closed")
    print("-----------------------------------")
