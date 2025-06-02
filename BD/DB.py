import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from BD.Tablas import CondicionesManuales, Evento, Escenarios, Acciones, EventoCondicionEscenario

load_dotenv()

# Acceder a las variables
database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()


# Métodos CRUD CONDICIONES_MANUALES
class CRUDCondicionesManuales:
    @staticmethod
    def Insertar(condiciones):
        try:
            for condicon in condiciones:
                nuevo_registro = CondicionesManuales(
                    nombre=condicon.nombre,
                    descripcion=condicon.descripcion,
                    seleccionado=condicon.seleccionado
                )
                session.add(nuevo_registro)
            session.commit()
            print("Registro insertado correctamente.")
        except Exception as e:
            print(f"Error al insertar: {e}")
            session.rollback()

    @staticmethod
    def ConsultarTodos(id: int):
        try:
            if id:
                return session.query(CondicionesManuales).filter_by(id=id).all()
            else:
                return session.query(CondicionesManuales).all()
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def ConsultarMarcado():
        try:
            return session.query(CondicionesManuales).filter_by(seleccionado=True).first()
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def Editar(id, descripcion=None):
        try:
            registro = session.query(CondicionesManuales).filter_by(id=id).first()
            if registro:
                if descripcion is not None:
                    registro.descripcion = descripcion
                session.commit()
                print("Registro actualizado correctamente.")
            else:
                print("Registro no encontrado.")
        except Exception as e:
            print(f"Error al editar: {e}")
            session.rollback()

    @staticmethod
    def Eliminar(id):
        try:
            registro = session.query(CondicionesManuales).filter_by(id=id).first()
            if registro:
                session.delete(registro)
                session.commit()
                print("Registro eliminado correctamente.")
            else:
                print("Registro no encontrado.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
            session.rollback()

    @staticmethod
    def Marcar(id):
        try:
            session.query(CondicionesManuales).update({CondicionesManuales.seleccionado: False})
            registro = session.query(CondicionesManuales).filter_by(id=id).first()
            if registro:
                registro.seleccionado = True
            session.commit()
            print(f"Se marco la condicion {registro.descripcion}.")
        except Exception as e:
            print(f"Error al actualizar: {e}")
            session.rollback()


# Métodos CRUD EVENTOS
class CRUDEventos:
    @staticmethod
    def Insertar(eventos):
        try:
            for evento in eventos:
                nuevo_evento = Evento(nombre=evento.nombre,
                                      descripcion=evento.descripcion,
                                      dispositivo_origen=evento.dispositivo,
                                      tipo=evento.tipo,
                                      url=evento.url,
                                      titulo=evento.titulo,
                                      canal_notificacion=evento.canal_notificacion,
                                      destinatarios=evento.destinatarios)

                session.add(nuevo_evento)
            session.commit()
            print("Registro insertado correctamente.")
        except Exception as e:
            print(f"Error al insertar: {e}")
            session.rollback()

    @staticmethod
    def Consultar(id: int):
        try:
            if id:
                return session.query(Evento).filter_by(id=id).first()
            else:
                return session.query(Evento).all()
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def ConsultarPorNombre(nombre: str):
        try:
            if nombre:
                return session.query(Evento).filter_by(nombre=nombre).first()
            else:
                raise Exception("Debe ingresar el nombre del evento.")
        except Exception as e:
            print(f"Error al consultar: {e}")
            return None

    @staticmethod
    def Editar(id, **kwargs):
        try:
            evento = session.query(Evento).filter_by(id=id).first()
            if not evento:
                print("Evento no encontrado.")
                return
            for key, value in kwargs.items():
                if hasattr(evento, key):
                    setattr(evento, key, value)
            session.commit()
            print(f"Evento {id} actualizado exitosamente.")
        except Exception as e:
            print(f"Error al editar: {e}")
            session.rollback()

    @staticmethod
    def Eliminar(id):
        try:
            evento = session.query(Evento).filter_by(id=id).first()
            if not evento:
                print("Evento no encontrado.")
                return
            session.delete(evento)
            session.commit()
            print(f"Evento {id} eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
            session.rollback()


class CRUDEscenarios:
    @staticmethod
    def Insertar(escenarios):
        try:
            for escenario in escenarios:
                nuevo_escenario = Escenarios(
                    nombre=escenario.nombre,
                    descripcion=escenario.descripcion
                )
                session.add(nuevo_escenario)
            session.commit()
            print("Escenario insertado correctamente.")
        except Exception as e:
            print(f"Error al insertar: {e}")
            session.rollback()

    @staticmethod
    def ConsultarTodos(id: int):
        try:
            if id:
                return session.query(Escenarios).filter_by(id=id).all()
            else:
                return session.query(Escenarios).all()
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def Eliminar(id):
        try:
            acciones = session.query(Acciones).filter_by(escenario=id).delete()
            if acciones > 0:
                print(f"Se eliminaron {acciones} registros con el id '{id}'.")
            else:
                print(f"No se encontraron registros con el id '{id}'.")
            escenarios = session.query(Escenarios).filter_by(id=id).delete()
            session.commit()
            if escenarios > 0:
                print(f"Se eliminaron {escenarios} registros con el id '{id}'.")
            else:
                print(f"No se encontraron registros con el nombre '{id}'.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
            session.rollback()


class CRUDAcciones:
    @staticmethod
    def Insertar(acciones):
        try:
            for accion in acciones:
                nueva_accion = Acciones(
                    escenario=accion.escenario,
                    id_dispositivo=accion.id_dispositivo,
                    comando=accion.comando,
                    orden=accion.orden
                )
                session.add(nueva_accion)
            session.commit()
            print("Acción insertada correctamente.")
        except Exception as e:
            print(f"Error al insertar: {e}")
            session.rollback()

    @staticmethod
    def Consultar():
        try:
            acciones = session.query(Acciones).all()
            return acciones
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def ConsultarPoreEscenario(escenario):
        try:
            acciones = session.query(Acciones).filter_by(escenario=escenario).all()
            return acciones
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def Actualizar(escenario, orden, id_dispositivo=None, comando=None):
        try:
            accion = session.query(Acciones).filter_by(escenario=escenario).filter_by(orden=orden).first()
            if not accion:
                print("Acción no encontrada.")
                return

            if id_dispositivo:
                accion.id_dispositivo = id_dispositivo
            if comando:
                accion.comando = comando

            session.commit()
            print("Acción actualizada correctamente.")
        except Exception as e:
            print(f"Error al actualizar: {e}")
            session.rollback()

    @staticmethod
    def Eliminar(escenario, orden):
        try:
            registros_eliminados = session.query(Acciones).filter_by(escenario=escenario).filter_by(
                orden=orden).delete()
            session.commit()
            if registros_eliminados > 0:
                print("Acción eliminada correctamente.")
            else:
                print("No se encontró la acción para eliminar.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
            session.rollback()


class CRUDEventoCondicionEscenario:
    @staticmethod
    def Insertar(evento, condicion, escenario):
        try:
            ece = EventoCondicionEscenario(
                evento=evento,
                condicion=condicion,
                escenario=escenario
            )
            session.add(ece)
            session.commit()
            print("ECE insertada correctamente.")
        except Exception as e:
            print(f"Error al insertar: {e}")
            session.rollback()

    @staticmethod
    def CosultarEC(evento, condicion):
        try:
            ece = session.query(EventoCondicionEscenario).filter_by(evento=evento).filter_by(condicion=condicion).all()
            return ece
        except Exception as e:
            print(f"Error al consultar: {e}")

    @staticmethod
    def Eliminar(evento, condicion, escenario):
        try:
            registros_eliminados = session.query(Acciones).filter_by(evento=evento).filter_by(
                condicion=condicion).filter_by(escenario=escenario).delete()
            session.commit()
            if registros_eliminados > 0:
                print("ECE eliminada correctamente.")
            else:
                print("No se encontró la acción para eliminar.")
        except Exception as e:
            print(f"Error al eliminar: {e}")
            session.rollback()
