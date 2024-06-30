import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)

PORT = 3000        # Port to listen on (non-privileged ports are > 1023)

class SpotifyAuthorizationManager:
    def main():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((HOST, PORT))
        s.listen()
        data = []
        conn,address = s.accept()  # accept an incoming connection using accept() method which will block until a new client connects
        while True:
            datachunk = conn.recv(1024) # reads data chunk from the socket in batches using method recv() until it returns an empty string
            if not datachunk:
                break  # no more data coming in, so break out of the while loop
            data.append(datachunk)  # add chunk to your already collected data
        conn.close()
        print(data)

    # def listen_for_authentication_call(self):
    #     self.socket.accept()
    #     print('made it here')
        
    if __name__ == '__main__':
        main()

