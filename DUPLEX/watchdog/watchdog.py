import socket
import time

hote = "localhost"
port = 1251
port_Backup = 1252
port_service_BACKUP = 1400

primary = True

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le Service écoute à présent sur le port {}".format(port))

connexion_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_backup.bind((hote, port_Backup))
connexion_backup.listen(5)
print("BACKUP : Le Service écoute à présent sur le port {}".format(port))


connexion_avec_Service, infos_connexion = connexion_principale.accept()
print("Watchdog connecté PRIMARY")
connexion_backup, infos_connexion_backup = connexion_backup.accept()
print("Watchdog connecté BACKUP")

cmpt = 0
msg_from_service = b""
msg_from_service_backup = b""

while msg_from_service != b"fin" or msg_from_service_backup!= b"fin":


    if primary:
        msg_from_service = connexion_avec_Service.recv(1024)
        #print(msg_from_service.decode())
    
        if msg_from_service == b"I'm Alive" :
            cmpt = 0
            connexion_avec_Service.send(b"Watchdog 5/5")
        else :
            cmpt += 1
            if cmpt == 3:
                connexion_avec_service_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connexion_avec_service_backup.connect((hote, port_service_BACKUP))

                msg_to_BACKUP = b"go"
                connexion_avec_service_backup.send(msg_to_BACKUP)
                #reponse_from_backup = connexion_avec_service_backup.recv(1024)
                print("Watchdog TIMEDOUT passing on Secondary service")
                primary = False
                cmpt = 0
     
        time.sleep(1)

    else:
        msg_from_service_backup = connexion_backup.recv(1024)
        #print(msg_from_service.decode())
    
        if msg_from_service_backup == b"I'm Alive" :
            cmpt = 0
            connexion_backup.send(b"Watchdog 5/5")
        else :
            cmpt += 1
            if cmpt == 3:
                print("Watchdog TIMEDOUT")
                break
        time.sleep(1)      


print("Erreur Watchdog")
connexion_avec_Service.close()
connexion_principale.close()
connexion_backup.close()