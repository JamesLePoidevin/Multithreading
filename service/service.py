import socket

hote = "localhost"
portCapteur = 1036
#portWatchdog = 1000

def connexion():
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, portCapteur))
    connexion_principale.listen(5)
    print("Le Service écoute à présent sur le port {}".format(1036))

    #connexion_avec_Watchdog = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connexion_avec_Watchdog.connect((hote, portWatchdog))
    #print("Connexion établie avec le Watchdog sur le port {}".format(portWatchdog))

    return connexion_principale.accept()

if __name__ == "__main__":
    
    connexion_avec_Capteur, infos_connexion =connexion()

    msg_to_Backup = b""
    msg_from_capteur = b""

    while msg_from_capteur != b"fin":

    #Reception depuis capteur
        msg_from_capteur = connexion_avec_Capteur.recv(1024)
        print(msg_from_capteur.decode())
        connexion_avec_Capteur.send(b"5 / 5")

    #Discussion avec Watchdog
    #    msg_to_Watchdog = b"I am alive"
    #    msg_to_Watchdog = msg_to_Watchdog.encode()
    #    connexion_avec_Watchdog.send(msg_to_Watchdog)
    #    reponse_from_watchdog = connexion_avec_Watchdog.recv(1024)
    #    print(reponse_from_watchdog.decode())

    #Partie Memoire stable


    print("Fermeture de la connexion")
    #connexion_avec_Watchdog.close()
    connexion_avec_Capteur.close()
    connexion_principale.close()