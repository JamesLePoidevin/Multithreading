import socket
import json

#Hote is the IP adresse or localhost of the service code
hote = "localhost"

#Port from which the numbers are sent 
portCapteur = 1036

#Port to kick the watchdog.
portWatchdog = 1252

#Port that receives the green light from watchdog to start
portFromWatchdog = 1400

#Function that connects to the socket for the capter
def connexion():

    #Receive from capter
    connexion_server_capteur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_server_capteur.bind((hote, portCapteur))
    connexion_server_capteur.listen(5)
    print("Le Service Backup écoute à présent le capteur sur le port {}".format(portCapteur))

    connexion_avec_Capteur, infos_connexion_capteur = connexion_server_capteur.accept()
    
    #connexion_avec_Capteur used to get messages
    return connexion_avec_Capteur

#Function that connects to the different sockets for thewatchdog 
def connexion_watchdog():

    #Receive green light from watchdog
    connexion_server_watchdog = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_server_watchdog.bind((hote, portFromWatchdog))
    connexion_server_watchdog.listen(5)
    print("Le Service Backup écoute à présent le watchdog sur le port {}".format(portFromWatchdog))

    #Send to Watchdog
    connexion_client_Watchdog = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_client_Watchdog.connect((hote, portWatchdog))
    print("Connexion établie du Service Backup (client) avec le Watchdog sur le port {}".format(portWatchdog))

    connexion_avec_Watchdog, infos_connexion_watchdog = connexion_server_watchdog.accept()

    #connexion_client_Watchdog and connexion_avec_Watchdog used to get and send messages
    return [connexion_avec_Watchdog, connexion_client_Watchdog]

def printit(x) :

    # Loading json file
    jsonFile = open('memoire.json','r')
    json_object = json.load(jsonFile)
    jsonFile.close()
    #print(json_object)


    # Iterate over json items
    for item in json_object :
        # Fill the blanks 
        if (json_object[item] == ""):
            json_object[item] = x
            break
        # Keep the 10 most recent values and replace "1" with "2" etc..
        else :
            if item=="10":
                for itemBis in json_object :
                    if(itemBis=="10"): 
                        json_object[itemBis] = x
                    else :
                        json_object[itemBis] = json_object[str(int(itemBis)+1)]

    # Send the new json file
    jsonFile = open('memoire.json','w')
    json.dump(json_object, jsonFile, indent = 4)
    jsonFile.close()

if __name__ == "__main__":
    
    #Starts connecxion the the watchdog
    [connexion_avec_Watchdog, connexion_client_Watchdog] = connexion_watchdog()

    #Inits messages
    msg_to_Backup = b""
    msg_from_capteur = b""

    #Waiting for message from watchdog to start
    launch_from_watchdog = connexion_avec_Watchdog.recv(1024)

    #If the watchdog sends go
    if launch_from_watchdog == b"go" :

        #Creates connection the capter
        connexion_avec_Capteur = connexion()


        while msg_from_capteur != b"fin":
            
            #Reception from capteur
            msg_from_capteur = connexion_avec_Capteur.recv(1024)
            print(msg_from_capteur.decode())
            connexion_avec_Capteur.send(b"5 / 5")

            #Discussion with Watchdog
            msg_to_Watchdog = b"I'm Alive"
            connexion_client_Watchdog.send(msg_to_Watchdog)
            reponse_from_watchdog = connexion_client_Watchdog.recv(1024)


            #Prints on the stable memoiry
            printit(msg_from_capteur.decode())
        
        #Closes the connecxions
        print("Fermeture de la connexion")
        connexion_avec_Watchdog.close()
        connexion_avec_Capteur.close()
        connexion_client_Watchdog.close()
    