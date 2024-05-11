# Programa en Python3 que imita un servidor de reloj

from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

# Estructura de datos utilizada para almacenar la dirección del cliente y los datos del reloj
datos_cliente = {}

''' Función de hilo anidada utilizada para recibir
    el tiempo del reloj de un cliente conectado '''
def empezarRecibirHoraReloj(conector, direccion):

    while True:
        # Recibir tiempo del reloj
        hora_reloj_string = conector.recv(1024).decode()
        hora_reloj = parser.parse(hora_reloj_string)
        diferencia_hora_reloj = datetime.datetime.now() - hora_reloj

        datos_cliente[direccion] = {
                       "hora_reloj"      : hora_reloj,
                       "diferencia_tiempo" : diferencia_hora_reloj,
                       "conector"       : conector
                       }

        print("Datos del cliente actualizados con: "+ str(direccion),
                                              end = "\n\n")
        time.sleep(5)

''' Función de hilo principal utilizada para abrir el portal para
    aceptar clientes sobre el puerto dado '''
def empezarConectar(servidor_maestro):
     
    # Obtener tiempo del reloj en esclavos / clientes
    while True:
        # Aceptar un cliente / reloj esclavo
        conector_esclavo_maestro, addr = servidor_maestro.accept()
        direccion_esclavo = str(addr[0]) + ":" + str(addr[1])

        print(direccion_esclavo + " se conectó correctamente")

        hilo_actual = threading.Thread(
                         target = empezarRecibirHoraReloj,
                         args = (conector_esclavo_maestro,
                                           direccion_esclavo, ))
        hilo_actual.start()

# Función de subrutina utilizada para obtener la diferencia de tiempo promedio
def obtenerDiferenciaTiempoPromedio():

    datos_cliente_actuales = datos_cliente.copy()

    lista_diferencias_tiempo = list(cliente['diferencia_tiempo'] 
                                for direccion_cliente, cliente 
                                    in datos_cliente.items())
                                    

    suma_diferencias_tiempo = sum(lista_diferencias_tiempo, \
                                   datetime.timedelta(0, 0))

    diferencia_tiempo_promedio = suma_diferencias_tiempo \
                                         / len(datos_cliente)

    return  diferencia_tiempo_promedio

''' Función de hilo de sincronización maestra utilizada para generar
    ciclos de sincronización de relojes en la red '''
def sincronizarTodosRelojes():

    while True:

        print("Nuevo ciclo de sincronización iniciado.")
        print("Número de clientes a sincronizar: " + \
                                     str(len(datos_cliente)))

        if len(datos_cliente) > 0:

            diferencia_tiempo_promedio = obtenerDiferenciaTiempoPromedio()

            for direccion_cliente, cliente in datos_cliente.items():
                try:
                    tiempo_sincronizado = \
                         datetime.datetime.now() + \
                                    diferencia_tiempo_promedio

                    cliente['conector'].send(str(
                               tiempo_sincronizado).encode())

                except Exception as e:
                    print("Algo salió mal mientras " + \
                          "enviaba el tiempo sincronizado " + \
                          "a través de " + str(direccion_cliente))

        else :
            print("No hay datos del cliente." + \
                        " La sincronización no es aplicable.")

        print("\n\n")

        time.sleep(5)

# Función utilizada para iniciar el Servidor de Reloj / Nodo Maestro
def iniciarServidorReloj(puerto = 8080):

    servidor_maestro = socket.socket()
    servidor_maestro.setsockopt(socket.SOL_SOCKET,
                                   socket.SO_REUSEADDR, 1)

    print("Socket en el nodo maestro creado exitosamente\n")
       
    servidor_maestro.bind(('', puerto))

    # Comenzar a escuchar solicitudes
    servidor_maestro.listen(10)
    print("Servidor de reloj iniciado...\n")

    # comenzar a hacer conexiones
    print("Comenzando a hacer conexiones...\n")
    hilo_maestro = threading.Thread(
                        target = empezarConectar,
                        args = (servidor_maestro, ))
    hilo_maestro.start()

    # comenzar sincronización
    print("Comenzando sincronización en paralelo...\n")
    hilo_sincronizacion = threading.Thread(
                          target = sincronizarTodosRelojes,
                          args = ())
    hilo_sincronizacion.start()



# Función principal
if __name__ == '__main__':

    # Iniciar el Servidor de Reloj
    iniciarServidorReloj(puerto = 8080)
