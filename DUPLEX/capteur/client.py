import socket
import random
import time

#Hote is the IP adresse or localhost of the service code
hote = "localhost"
port = 1036

#Init and connecxion to the services using TCP/IP 
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""

#Counter used to send a set amout of numbers.
compteur = 0

while compteur != 100:

    #Creating the message to send
    msg_a_envoyer = msg_a_envoyer + str(random.randint(0, 2)).encode()
    
    #Try to connect (used if the primary has a fault)
    try:
        connexion_avec_serveur.send(msg_a_envoyer)
        msg_recu = connexion_avec_serveur.recv(1024)
        print(msg_recu.decode()) 

    #If not able to send message
    except:
        print("No one to send to")
        
        #Try to reconnect to the new receiver
        try:
            connexion_avec_serveur.close()
            connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connexion_avec_serveur.connect((hote, port))
        except:
            print("connection failed, please wait...")

    #Sent every second
    time.sleep(1)
    
    #Creating new empty message
    msg_a_envoyer = b""

    #Incrementing counter
    compteur = compteur +1

#Once the 100 messages are send close the connexion
connexion_avec_serveur.send(b"fin")
print("Fermeture de la connexion")
connexion_avec_serveur.close()