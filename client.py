import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 8080
client_socket.connect((host, port))

while True:
    server_msg = client_socket.recv(1024).decode()
    if "Correct" in server_msg or "Invalid" in server_msg:
        print(server_msg)
        break
    print(server_msg)
    guess = input("Your guess: ")
    client_socket.send(guess.encode())
    if guess.upper() == "END":
        break

client_socket.close()
