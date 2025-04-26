import json
import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER

from BD.Tablas import Acciones
from DatosSensibles import CargarDatosSensibles

ACCESS_ID = CargarDatosSensibles("ACCESS_ID")
ACCESS_KEY = CargarDatosSensibles("ACCESS_KEY")
API_ENDPOINT = "https://openapi.tuyaus.com"

openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

def EjecutarComandos(acciones: list[Acciones]):
    try:
        for accion in acciones:
            commands = json.loads(accion.comando.replace("'", "\""))
            id_device = accion.id_dispositivo
            openapi.post('/v1.0/devices/{}/commands'.format(id_device), commands)
    except Exception as e:
        print(f"Error: {e}")

def ObtenerDispositivos():
    response = openapi.get("/v2.0/cloud/thing/device?page_size=20")
    if response.get("success"):
        dispositivos = response.get("result", [])
        return dispositivos
    else:
        raise Exception(f"Error al obtener dispositivos: {response}")


def VerDispositivos():
    response = openapi.get("/v2.0/cloud/thing/device?page_size=20")
    if response.get("success"):
        dispositivos = response.get("result", [])
        for dispositivo in dispositivos:
            print(f"ID: {dispositivo['id']}, Nombre: {dispositivo['name']}")
    else:
        print(f"Error al obtener dispositivos: {response}")

#VerDispositivos()

# # Init OpenAPI and connect
# openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
# openapi.connect()
#
# # Enable debug log
# TUYA_LOGGER.setLevel(logging.DEBUG)
#
# # Set up device_id
#DEVICE_ID = "vdevo172387077326231"
#
# flag = True
# while True:
#     input('Hit Enter to toggle light switch.')
#     flag = not flag
#     commands = {'commands': [{'code': 'switch_1', 'value': True}]}
#     openapi.post('/v1.0/devices/{}/commands'.format(DEVICE_ID), commands)
