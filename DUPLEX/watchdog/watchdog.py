import socket
import time

hote = "localhost"
port = 1251
port_service_BACKUP = 1400

primary = True

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le Service écoute à présent sur le port {}".format(port))

connexion_avec_service_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_service_backup.connect((hote, port_service_BACKUP))

connexion_avec_Service, infos_connexion = connexion_principale.accept()
print("Watchdog connecté")

cmpt = 0
msg_from_service = b""

while msg_from_service != b"fin":

    msg_from_service = connexion_avec_Service.recv(1024)
    #print(msg_from_service.decode())
    
    if msg_from_service == b"I'm Alive" :
        cmpt = 0
        connexion_avec_Service.send(b"Watchdog 5/5")
    else :
        cmpt += 1
        if cmpt == 3 and primary:
            msg_to_Watchdog = b"I'm Alive"
            connexion_avec_Watchdog.send(msg_to_Watchdog)
            reponse_from_watchdog = connexion_avec_Watchdog.recv(1024)
            print("Watchdog TIMEDOUT passsing on Secondary service")
            break 
     
    #print("Compteur : ",cmpt)   
    time.sleep(1)   


print("Erreur Watchdog")
connexion_avec_Service.close()
connexion_principale.close()