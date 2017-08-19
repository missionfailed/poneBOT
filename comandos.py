# comandos.py Contiene la logica de los comandos y sus nombres

import re
import sys
import socket
import random
import config as cfg

COMANDOS = {
    "Timeout": r"robot",
    "Saludo": r"!hola",
    "Aleatorio": r"!aleatorio",
    "Terminar": r"!bye",
    "Fecha": r"!hora",
    "Adivina": r"!adivina",
    "NO_Adivina": r"!stop"
}

def chat(sock, msg):
    """Manda mensaje al servidor de Twitch"""
    mensaje = "PRIVMSG {} :{} \r\n".format(cfg.CHAN, msg)
    print(mensaje)
    sock.send(mensaje.encode())

def ban(sock, user):
    """Banea a un usuario"""
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """Da timeout a un usuario por el tiempo especificado"""
    mensaje = ".timeout {}".format(user, secs)
    chat(sock, mensaje)

def hola(sock, user):
    """Saluda a un usuario"""
    mensaje = "Bienvenido {0}!".format(user)
    chat(sock, mensaje)

def numero_magico(sock):
    """Regresa un numero aleatorio a un usuario"""
    numero = random.randint(1,11)
    mensaje = "Tu numero magico es: {0}".format(numero)
    chat(sock, mensaje)

def hora(sock):
    """Regresa la fecha a un usuario"""
    tiempo = datetime.datetime.now()
    chat(sock, tiempo)

def terminar(sock):
    """Exterminar el bot"""
    sys.exit()

def empieza_numero(sock):
    """Empieza una rifa"""
    numero = random.randint(1, 20)
    chat(sock, "Adivina el numero magico! (1 al 20)")
    return numero