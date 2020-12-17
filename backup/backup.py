import json
import threading
import random

data = {'1' : '', '2' : '', '3' : '', '4' : '', '5' : '', '6' : '', '7' :'', '8' : '', '9' : '', '10' : ''}

with open('backup.json', 'w') as outfile:
    json.dump(data, outfile, indent = 4)


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

#printit()
