import socket
import json

#Hote is the IP adresse or localhost of the service code
hote = "localhost"

#Port from which the numbers are sent 
port_capteur = 1036

#Port to kick the watchdog.
port_watchdog = 1251

#Data for creating the Json file
data = {'1' : '', '2' : '', '3' : '', '4' : '', '5' : '', '6' : '', '7' :'', '8' : '', '9' : '', '10' : ''}

with open('backup.json', 'w') as outfile:
    json.dump(data, outfile, indent = 4)

#Function that connects to the different sockets for the capter and watchdog 
def connexion():

    #Receive from capter
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port_capteur))
    connexion_principale.listen(5)
    print("Le Service écoute à présent sur le port {}".format(1036))

    #Send to Watchdog
    connexion_avec_Watchdog = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_Watchdog.connect((hote, port_watchdog))
    print("Connexion établie avec le Watchdog sur le port {}".format(port_watchdog))

    connexion_avec_Capteur, infos_connexion = connexion_principale.accept()

    #connexion_avec_Capteur and connexion_avec_Watchdog used to get and send messages
    return [connexion_avec_Capteur,connexion_avec_Watchdog]

def printit(x) :

    # Loading json file
    jsonFile = open('memoire.json','r')
    json_object = json.load(jsonFile)
    jsonFile.close()

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

#Main fonction
if __name__ == "__main__":
    
    #Starts the connections
    [connexion_avec_Capteur,connexion_avec_Watchdog] =connexion()

    #Inits messages
    msg_to_Backup = b""
    msg_from_capteur = b""

    while msg_from_capteur != b"fin":

        #Reception from capteur
        msg_from_capteur = connexion_avec_Capteur.recv(1024)
        print(msg_from_capteur.decode())
        connexion_avec_Capteur.send(b"5 / 5")

        #Discussion with Watchdog
        msg_to_Watchdog = b"I'm Alive"
        connexion_avec_Watchdog.send(msg_to_Watchdog)
        reponse_from_watchdog = connexion_avec_Watchdog.recv(1024)

        #Prints on the stable memoiry
        printit(msg_from_capteur.decode())

    #Closes the connecxions
    print("Fermeture de la connexion")
    connexion_avec_Watchdog.close()
    connexion_avec_Capteur.close()