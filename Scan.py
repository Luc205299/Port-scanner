import socket
import threading
from queue import Queue
from ScanIP import Scan_ip

# Nombre de threads à utiliser
NUM_THREADS = 100

# Queue pour stocker les ports à scanner
port_queue = Queue()

# Stockage des ports ouverts
open_ports = []
host={}

class NetscanThread(threading.Thread):
    def __init__(self, address):
        self.address = address
        threading.Thread.__init__(self)
    
    def run(self):
        self.lookup(self.address)
        
    def lookup(self, address):
        try:
            hostname, alias, _ = socket.gethostbyaddr(address)
            global host
            host[address] = hostname
        except socket.herror:
            host[address] = "hostname not found"
        except Exception as e:
            print(f"Error : {e}")

# Fonction de scan de port
def port_scanner(target):
    while not port_queue.empty():
        port = port_queue.get()  # Récupérer un port de la queue
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout de 1 seconde
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)  # Ajouter le port ouvert à la liste
        except Exception as e:
            pass
        finally:
            sock.close()

# Fonction pour créer des threads
def threader(target):
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=port_scanner, args=(target,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()  # Attendre que tous les threads soient terminés

# Main function
if __name__ == "__main__":
    print(r"|=========================================================================|")
    print(r"|                    ,--.       ,--.                                      |")
    print(r"|         ,-.----.     ,---,   ,--/  /|   ,--/  /|   ,---,                |")
    print(r"|         \    /  \ ,`--.' |,---,': / ',---,': / '  '  .' \               |")
    print(r"|         ;   :    \|   :  ::   : '/ / :   : '/ /  /  ;    '.             |")
    print(r"|         |   | .\ ::   |  '|   '   ,  |   '   ,  :  :       \            |")
    print(r"|         .   : |: ||   :  |'   |  /   '   |  /   :  |   /\   \           |")
    print(r"|         |   |  \ :'   '  ;|   ;  ;   |   ;  ;   |  :  ' ;.   :          |")
    print(r"|         |   : .  /|   |  |:   '   \  :   '   \  |  |  ;/  \   \         |")
    print(r"|         ;   | |  '   :  ;|   |    ' |   |    ' '  :  | \  \ ,'          |")
    print(r"|         |   | ;\  \   |  ''   : |.  '   : |.  \|  |  '  '--'            |")
    print(r"|         :   ' | \.'   :  ||   | '_\.'|   | '_\.'|  :  :                 |")
    print(r"|         :   : :-' ;   |.' '   : |    '   : |    |  | ,'                 |")
    print(r"|         |   |.'   '---'   ;   |,'    ;   |,'    `--''                   |")
    print(r"|         `---'             '---'      '---'                              |")
    print(r"|                                                                         |")
    print(r"|=========================================================================|")


    print("1. Scan a range of port\n2. Scan a range of ip")
    choice = int(input("Select your choice : \n"))
    
    
    if choice ==1 :
        
        target_ip = input("Enter the target IP or hostname (e.g., localhost): ")
        start_port = int(input("Enter the start port: "))
        end_port = int(input("Enter the end port: "))

        # Ajouter les ports à la queue
        for port in range(start_port, end_port + 1):
            port_queue.put(port)

        # Démarrer les threads
        threader(target_ip)

        # Afficher les ports ouverts
        if open_ports:
            print(f"Open ports on {target_ip}: {open_ports}")
        else:
            print(f"No open ports found on {target_ip}")

    elif choice == 2 : 
        Scan_ip()
        
        
        
                    
            
    
    
    