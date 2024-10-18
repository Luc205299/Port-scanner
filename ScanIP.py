import socket
from threading import Thread, Lock
import queue

# Fonction appelée par chaque thread pour récupérer le nom d'hôte
def gethostname(address, q, lock):
    try:
        hostname, alias, _ = socket.gethostbyaddr(address)
    except socket.herror:
        hostname = None
    
    # Utilisation d'un verrou pour éviter la modification concurrente
    with lock:
        q.put((address, hostname))

# Main function
def Scan_ip():
    target_ip = str(input("Enter the target IP ex:(192.168.177) or hostname : "))
    q = queue.Queue()
    threads = []
    lock = Lock()

    # Dictionnaire qui stockera les noms d'hôte récupérés
    hostnames = {}

    # Plage d'adresse IP à scruter
    for ping in range(1, 254):
        address = target_ip+'.'+ str(ping)
        
        # Création du thread avec appel de la fonction gethostname
        t = Thread(target=gethostname, args=(address, q, lock))
        threads.append(t)

    # Démarrage des threads
    for t in threads:
        t.start()

    # Attente que tous les threads soient terminés
    for t in threads:
        t.join()

    # Récupération des résultats de la queue
    while not q.empty():
        address, hostname = q.get()
        hostnames[address] = hostname

    # Affichage des résultats
    for address, hostname in hostnames.items():
        if hostname is not None:
            print(f"{address} => {hostname}")
        else:
            print(f"{address} => No hostname found")
