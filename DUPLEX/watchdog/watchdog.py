import socket
import time

#Hote is the IP adresse or localhost of the service code
hote = "localhost"

#Port from which the service PRIMARY sends the kick
port = 1251

#Port from which the service BACKUP sends the kick
port_Backup = 1252

#Port to give green light to BACKUP
port_service_BACKUP = 1400

#If the primary is working then True else False
primary = True

#Init and connecxion to Primary service
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le Service écoute à présent sur le port {}".format(port))

#Init and connecxion to BACKUP service
connexion_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_backup.bind((hote, port_Backup))
connexion_backup.listen(5)
print("BACKUP : Le Service écoute à présent sur le port {}".format(port))


connexion_avec_Service, infos_connexion = connexion_principale.accept()
print("Watchdog connecté PRIMARY")
connexion_backup, infos_connexion_backup = connexion_backup.accept()
print("Watchdog connecté BACKUP")

#Counter for the timer
cmpt = 0

#Init the messages
msg_from_service = b""
msg_from_service_backup = b""

while msg_from_service != b"fin" or msg_from_service_backup!= b"fin":

    #PRIMARY mode
    if primary:
        msg_from_service = connexion_avec_Service.recv(1024)

        #Primary kicking the watchdog
        if msg_from_service == b"I'm Alive" :
            cmpt = 0
            connexion_avec_Service.send(b"Watchdog 5/5")

        #No message from service    
        else :

            #
            cmpt += 1
            if cmpt == 3:
                #Connecxiont to the BACKUP
                connexion_avec_service_backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connexion_avec_service_backup.connect((hote, port_service_BACKUP))

                #Gives the green light the backup to start
                msg_to_BACKUP = b"go"
                connexion_avec_service_backup.send(msg_to_BACKUP)
                print("Watchdog TIMEDOUT passing on Secondary service")

                primary = False
                cmpt = 0

        #TIMER
        time.sleep(1)

    #BACKUP mode
    else:
        msg_from_service_backup = connexion_backup.recv(1024)

        #Backup kicking the watchdog
        if msg_from_service_backup == b"I'm Alive" :
            cmpt = 0
            connexion_backup.send(b"Watchdog 5/5")
        else :
            cmpt += 1
            if cmpt == 3:
                print("Watchdog TIMEDOUT")
                break
        time.sleep(1)      

#Closes the connecxions
print("Erreur Watchdog")
connexion_avec_Service.close()
connexion_principale.close()
connexion_backup.close()