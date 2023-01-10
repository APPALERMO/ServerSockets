import socket
import os
import Tool
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from Tool.createJson import createJson

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.26.89", 8000)
print('inizio a fare l\'ascolto su {} porta {}'.format(*server_address))

df = pd.read_csv('Dati.csv')


def sendmessage(message):
    connection.sendall(str(message).encode())


def takeWeb():
    webs = {}
    extractor = Tool.extractor(arr_wifi=[], arr_pass=[], dict_rete=webs)
    reti = extractor.extractWeb()

    return reti


def takeInfo():
    createJson("Informazioni")
    file = open("Informazioni.json", "r")
    contenuto = file.read()
    file.close()
    os.remove("Informazioni.json")
    return contenuto


def writeWebs(file_name):
    name = file_name
    createJson(name)


def openGUI():
    return "Ciao Mondo"

sock.bind(server_address)

sock.listen(1)


risposte = {

    "tookWebs": takeWeb(),
    "tookINFO": takeInfo(),
    "writeWebs": "writeWebs",
    "OPEN-GUI": openGUI()

}


while True:
    connection, client_address = sock.accept()
    data = connection.recv(1024).decode()
    data = data.split(" ")

    if len(data) >= 3:
        arg2 = data[2:]
        data = data[:2]

        print("Dati ricevuti dal client: {}, {}".format(data, arg2))
    else:
        print("Dati ricevuti dal client: {}".format(data))

    try:
        X = df[data]
    except KeyError:
        sendmessage("Inserisci bene l'argomento")
        continue
    except ValueError:
        break
        break
    y = df["RISPOSTA"]

    model = DecisionTreeClassifier()
    model.fit(X.values, y.values)
    prev = model.predict([[1, 1]])
    prev = " ".join(prev)
    # print(prev)

    risp = risposte.get(prev)
    # print(risp)
    if risp is None:
        print("Riprova!")
        sendmessage("Riprova!")
    else:
        if risp == "writeWebs":
            try:
                filename = " ".join(arg2)
                writeWebs(filename)
                print("Fatto!  !")
                sendmessage("File creato con successo!")
            except NameError:
                sendmessage("Inserisci il nome del File!")
                print("Errore")
        else:
            print(risp)
            sendmessage(risp)


connection.close()
