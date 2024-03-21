import socket
import pandas as pd
import random

city_data = pd.read_excel("C:\Users\ecena\OneDrive\Belgeler\PlateCodePrediction\plate_list.xlsx")
cities = city_data['City'].tolist()
codes = city_data['Code'].tolist()
city_codes = dict(zip(cities, codes))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 12345
server_socket.bind((host, port))
server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    selected_city = random.choice(list(city_codes.keys()))
    client_socket.send(f"Guess the plate code for {selected_city}: ".encode())

    while True:
        guess = client_socket.recv(1024).decode().strip()
        if guess.upper() == "END":
            client_socket.close()
            server_socket.close()
            print("Server shutting down.")
            exit()
        try:
            guess = int(guess)
            if guess < 1 or guess > 81:
                msg = "Invalid plate code. It must be between 1 and 81."
            elif guess in codes:
                if city_codes[selected_city] == guess:
                    msg = "Correct! Connection closing."
                    client_socket.send(msg.encode())
                    client_socket.close()
                    break
                else:
                    city_for_guess = cities[codes.index(guess)]
                    msg = f"Incorrect. {guess} is the plate code for {city_for_guess}."
            else:
                msg = "Incorrect guess."
        except ValueError:
            msg = "Please enter a numeric value."
        
        client_socket.send(msg.encode())
