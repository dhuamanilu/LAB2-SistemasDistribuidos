# Programa en Python3 que imita un proceso de cliente

from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket 
import time


# Función de hilo del cliente utilizada para enviar la hora en el lado del cliente
def empezarEnviarHora(cliente_esclavo):

    while True:
        # Proporcionar al servidor la hora del reloj en el cliente
        cliente_esclavo.send(str(
                       datetime.datetime.now()).encode())

        print("Hora reciente enviada exitosamente",
                                          end = "\n\n")
        time.sleep(5)


# Función de hilo del cliente utilizada para recibir tiempo sincronizado
def empezarRecibirHora(cliente_esclavo):

    while True:
        # Recibir datos del servidor
        tiempo_sincronizado = parser.parse(
                          cliente_esclavo.recv(1024).decode())

        print("Hora sincronizada en el cliente es: " + \
                                    str(tiempo_sincronizado),
                                    end = "\n\n")


# Función utilizada para sincronizar el tiempo del proceso del cliente
def iniciarClienteEsclavo(puerto = 8080):

    cliente_esclavo = socket.socket()          

    # Conectar al servidor de reloj en la computadora local 
    cliente_esclavo.connect(('127.0.0.1', puerto)) 

    # Empezar a enviar tiempo al servidor
    print("Comenzando a recibir tiempo del servidor\n")
    hilo_enviar_tiempo = threading.Thread(
                      target = empezarEnviarHora,
                      args = (cliente_esclavo, ))
    hilo_enviar_tiempo.start()


    # Empezar a recibir tiempo sincronizado del servidor
    print("Comenzando a recibir " + \
                         "tiempo sincronizado del servidor\n")
    hilo_recibir_tiempo = threading.Thread(
                       target = empezarRecibirHora,
                       args = (cliente_esclavo, ))
    hilo_recibir_tiempo.start()


# Función principal
if __name__ == '__main__':

    # Inicializar el Cliente Esclavo
    iniciarClienteEsclavo(puerto = 8080)