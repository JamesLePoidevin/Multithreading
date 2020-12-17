import socket
import random
import time

hote = "localhost"
port = 1036

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""
compteur = 0
while compteur != 50:
    msg_a_envoyer = msg_a_envoyer + str(random.randint(0, 2)).encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)
    msg_recu = connexion_avec_serveur.recv(1024)
    print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents
    time.sleep(1)
    msg_a_envoyer = b""
    compteur = compteur +1

print("Fermeture de la connexion")
connexion_avec_serveur.close()

