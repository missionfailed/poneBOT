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
chat(s, "Bienvenidos!")

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        if "PRIVMSG" not in response and "JOIN" in response:
            usuario_nuevo = response.split()
            usuario_nuevo = usuario_nuevo[0]
            chat(s, "{0} entro al stream.".format(usuario_nuevo))

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

        time.sleep(1 / cfg.RATE)