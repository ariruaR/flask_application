import socket
from main import app


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 2000))
server.listen(4)
print('Server start')
client_socket, address = server.accept()
data = client_socket.recv(1024).decode('utf-8')
print('data')

if __name__ == "__main__":
  app.run(host='127.0.0.1',port=2000,debug=True)
