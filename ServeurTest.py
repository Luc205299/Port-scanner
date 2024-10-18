import socket
import threading

class Serveur: 
    def __init__(self):
        print("Serveur démarré")
        
        # Creation of the server socket
        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Link the socket to the IP address and port
        self.socket_ecoute.bind(('', 1234))

        # Listen mode to accept incoming connections
        self.socket_ecoute.listen()
        print("Serveur en écoute sur le port 1234...")

        # Démarrer un thread pour accepter plusieurs clients
        self.running = True
        self.threads = []
        self.accept_thread = threading.Thread(target=self.accepter_clients)
        self.accept_thread.start()
        
    def affichage(self):
        print(self.socket_ecoute)

    def accepter_clients(self):
        """Accepte les connexions des clients dans un thread séparé."""
        while self.running:
            try:
                # Attendre une nouvelle connexion
                connexion_client, adresse_client = self.socket_ecoute.accept()
                print(f"Connexion acceptée de {adresse_client}")

                # Créer un thread pour gérer ce client
                client_thread = threading.Thread(target=self.gerer_client, args=(connexion_client,))
                self.threads.append(client_thread)
                client_thread.start()

            except Exception as e:
                print(f"Erreur lors de l'acceptation d'un client : {e}")

    def gerer_client(self, connexion_client):
        """Gère la communication avec un client spécifique."""
        try:
            while self.running:
                # Recevoir des données du client
                data = connexion_client.recv(1024)
                
                if not data:
                    print("Client déconnecté")
                    break

                print(f"Message reçu : {data.decode('utf-8')}")

                # Envoyer une réponse au client
                connexion_client.send("Message bien reçu".encode('utf-8'))
                
        except Exception as e:
            print(f"Erreur avec le client : {e}")
        finally:
            # Fermer la connexion proprement
            connexion_client.close()
            print("Connexion avec le client fermée")

    def fermer_serveur(self):
        """Ferme le serveur proprement."""
        self.running = False
        self.socket_ecoute.close()
        for thread in self.threads:
            thread.join()  # Attendre que tous les threads se terminent
        print("Serveur fermé")

# Démarrer le serveur
if __name__ == "__main__":
    serveur = Serveur()
    Serveur.affichage(serveur)
    # Arrêter le serveur après un certain temps ou en pressant une touche
    input("Appuyez sur Entrée pour arrêter le serveur...\n")
    serveur.fermer_serveur()
