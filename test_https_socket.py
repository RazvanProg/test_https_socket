import os
import socket
import threading
import urllib.parse
from flask import Flask, request

# Configurare aplicație Flask
app = Flask(__name__)

# Configurare server socket
HOST = '0.0.0.0'
PORT = 12345

def start_socket_server():        
    """Serverul socket care ascultă pe un port specific."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Serverul socket este pornit și ascultă pe {HOST}:{PORT}...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexiune acceptată de la: {client_address}")
        
        # Primirea și procesarea datelor de la client
        data = client_socket.recv(1024).decode()
        print(f"Mesaj primit: {data}")
        
        # 1. Extragem partea URL dintre "GET" și "HTTP/1.1"
        url = data.split(" ")[1]

        # 2. Parsăm URL-ul pentru a obține parametrii query
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # 3. Extragem valoarea parametrului 'msg'
        message = query_params.get("msg", [""])[0]  # Implicit, un string gol dacă 'msg' nu există
        print(f"Mesajul extras: {message}")

        # Răspuns către client
        response = f"Salut! Mesajul tau a fost primit: {data}"
        client_socket.sendall(response.encode())
        
        client_socket.close()

# Pornirea serverului socket într-un fir de execuție separat
socket_thread = threading.Thread(target=start_socket_server, daemon=True)
socket_thread.start()

# Endpoint HTTP simplu
@app.route('/')
def home():
    message = request.args.get('msg', 'Mesajul lipsește')  # Default dacă "msg" lipsește
    print(f"Mesaj primit (GET): {message}")
    return "Server HTTP și socket este în funcțiune!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Portul pentru Flask
    app.run(host='0.0.0.0', port=port)