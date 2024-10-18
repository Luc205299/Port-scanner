import socket

print("Client")

class Client: 
    def __init__(self):
        print("Client initialized")
        self.clientStart = True
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = int(input("Enter the port you want to connect to: "))
        self.name = str(input("Enter the server name (use 'localhost' if on the same machine): "))
        self.ClientOn()
        
    def Ask_connection(self):
        print(f"Trying to connect to {self.name} on port {self.port}...")
        try:
            self.server_connection.connect((self.name, self.port))
            print(f"Connected to server {self.name} on port {self.port}")
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.clientStart = False
        
    def Close_connection(self):
        self.server_connection.close()
        print("Connection closed")
        
    def Send_data(self, message):
        try:
            self.server_connection.send(message.encode('utf-8'))
            print(f"Message sent: {message}")
            
            # Receive the server's answer after sending 
            data = self.server_connection.recv(1024)
            print(f"Response from server: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Error sending message: {e}")
            
    def ClientOn(self):
        print("Client started")
        self.Ask_connection()
        
        if self.clientStart:  # Continue only if the connection was successful
            while self.clientStart:
                print("What do you want to do?")
                try:
                    choice = int(input("1. Send a message\n2. Quit\n"))
                except ValueError:
                    print("Please enter a valid number")
                    continue
                
                if choice == 1:
                    message = input("Enter the message to send: ")
                    self.Send_data(message)
                elif choice == 2:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice")
                    
            self.Close_connection()
            self.clientStart = False
            print("Client closed")

Client()