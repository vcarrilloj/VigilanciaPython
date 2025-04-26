from BD.DB import CRUDAcciones
from TuyaDispositivos import EjecutarComandos


def EjecutarEscenario(idEscenario):
    if idEscenario is None:
        raise Exception('El identificador del escenario no puede se nulo.')
    acciones = CRUDAcciones.ConsultarPoreEscenario(idEscenario)
    if len(acciones) > 0:
        EjecutarComandos(acciones)
    print(f'Se ejecuto el escenario: {idEscenario}.')
