# ponebot.py

import socket
import time
import datetime
import re
import tok
import sys
import comandos
from comandos import *
import usuarios as us
import config as cfg

NUMERO_BOT = -1
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
JOIN =re.compile(r"^:\w+!\w+@\w+JOIN #\w+ :")

# Coneccion al servidor
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(tok.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))
s.send("CAP REQ :twitch.tv/membership \r\n".encode("utf-8"))
response = s.recv(1024).decode("utf-8")

chat(s, "Bienvenidos!")

while True:
    response_list = s.recv(1024).decode("utf-8")
    for response in response_list.split("\r\n"):
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            if "PRIVMSG" not in response and "JOIN" in response:
                nombre = response.split("!")[0][1:]
                chat(s,"{0} entro al stream.".format(nombre))
            elif "PRIVMSG" in response:
                username = re.search(r"\w+", response).group(0) # return the entire match
                message = CHAT_MSG.sub("", response)
                # print(username + ": " + message)
                global NUMERO_BOT

                # Comandos Superusuarios
                if username in us.USERS and re.match(COMANDOS["Adivina"], message):
                    NUMERO_BOT = empieza_numero(s)

                if username in us.USERS and re.match(COMANDOS["NO_Adivina"], message):
                    NUMERO_BOT = -1      

                if NUMERO_BOT != -1 and message.strip() == str(NUMERO_BOT):
                    chat(s, "Ganaste! {0}".format(username))
                    chat(s, "Calculando nuevo numero magico!")
                    NUMERO_BOT = random.randint(1, 20)

                if username in us.USERS and re.match(COMANDOS["Terminar"], message):
                    chat(s, "Bye!")
                    terminar(s)

                if re.match(COMANDOS["Saludo"], message):
                    hola(s, username)

                if re.match(COMANDOS["Aleatorio"], message):
                    numero_magico(s)

                if re.match(COMANDOS["Fecha"], message):
                    hora(s)

                if re.match(COMANDOS["Abre_Cuenta"], message):
                    abre_cuenta(s, username)

                if re.match(COMANDOS["Checa_Cuenta"], message):
                    checa_cuenta(s, username)
        time.sleep(1 / cfg.RATE)