import socket
import json

hote = "localhost"
portCapteur = 1036
portWatchdog = 1251

data = {'1' : '', '2' : '', '3' : '', '4' : '', '5' : '', '6' : '', '7' :'', '8' : '', '9' : '', '10' : ''}

with open('backup.json', 'w') as outfile:
    json.dump(data, outfile, indent = 4)

def connexion():
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, portCapteur))
    connexion_principale.listen(5)
    print("Le Service écoute à présent sur le port {}".format(1036))

    connexion_avec_Watchdog = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_Watchdog.connect((hote, portWatchdog))
    print("Connexion établie avec le Watchdog sur le port {}".format(portWatchdog))

    connexion_avec_Capteur, infos_connexion = connexion_principale.accept()
    return [connexion_avec_Capteur, infos_connexion,connexion_avec_Watchdog]

def printit(x) :
    # Starting the thread
    #threading.Timer(1.0, printit).start()

    # Loading json file
    jsonFile = open('backup.json','r')
    json_object = json.load(jsonFile)
    jsonFile.close()
    #print(json_object)

    # Modify the values
    #x = random.randint(0,10)
    #Update File
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
    jsonFile = open('backup.json','w')
    json.dump(json_object, jsonFile, indent = 4)
    jsonFile.close()

if __name__ == "__main__":
    
    [connexion_avec_Capteur, infos_connexion,connexion_avec_Watchdog] =connexion()

    msg_to_Backup = b""
    msg_from_capteur = b""

    while msg_from_capteur != b"fin":

    #Reception depuis capteur
        msg_from_capteur = connexion_avec_Capteur.recv(1024)
        print(msg_from_capteur.decode())
        connexion_avec_Capteur.send(b"5 / 5")

    #Discussion avec Watchdog
        msg_to_Watchdog = b"I'm Alive"
        connexion_avec_Watchdog.send(msg_to_Watchdog)
        reponse_from_watchdog = connexion_avec_Watchdog.recv(1024)
        #print(reponse_from_watchdog.decode())

    #Partie Memoire stable
        printit(msg_from_capteur.decode())

    print("Fermeture de la connexion")
    connexion_avec_Watchdog.close()
    connexion_avec_Capteur.close()
    connexion_principale.close()