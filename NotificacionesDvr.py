import logging
from datetime import datetime

import pyhik.hikvision as hikvision
import requests
from requests.auth import HTTPDigestAuth

from BD.DB import CRUDEventos, CRUDCondicionesManuales, CRUDEventoCondicionEscenario
from CorreoElectronico import EnviarCorreo
from DatosSensibles import CargarDatosSensibles
from Escenarios import EjecutarEscenario
from FirebaseNotificacionesPush import EnviarNotificacionPorCanal

logging.basicConfig(filename='Logs/out.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class HikCamObject(object):
    """Representation of HIk camera."""

    def __init__(self, url, port, user, passw):
        """initalize camera"""

        # Establish camera
        self.cam = hikvision.HikCamera(url, port, user, passw)

        self._name = self.cam.get_name
        self.motion = self.cam.current_motion_detection_state

        # Start event stream
        self.cam.start_stream()

        self._event_states = self.cam.current_event_states
        self._id = self.cam.get_id

        print('NAME: {}'.format(self._name))
        print('ID: {}'.format(self._id))
        print('{}'.format(self._event_states))
        print('Motion Dectect State: {}'.format(self.motion))

    @property
    def sensors(self):
        """Return list of available sensors and their states."""
        return self.cam.current_event_states

    def get_attributes(self, sensor, channel):
        """Return attribute list for sensor/channel."""
        return self.cam.fetch_attributes(sensor, channel)

    def stop_hik(self):
        """Shutdown Hikvision subscriptions and subscription thread on exit."""
        self.cam.disconnect()

    def flip_motion(self, value):
        """Toggle motion detection"""
        if value:
            self.cam.enable_motion_detection()
        else:
            self.cam.disable_motion_detection()


def CapturarImagen(url):
    # Realizar la petición HTTP GET
    response = requests.get(url, auth=HTTPDigestAuth(usuario, clave))

    # Comprobar si la petición fue exitosa (código de estado 200)
    if response.status_code == 200:
        fecha_formateada = datetime.now().strftime("%d%m%Y%H%M%S")
        nombreFoto = f'{fecha_formateada}.jpg'
        with open(f'Capturas/{fecha_formateada}.jpg', "wb") as f:
            f.write(response.content)
        return nombreFoto
    else:
        raise Exception(f"Error al obtener la imagen. Código de estado: {response.status_code}")


def ManejarEveto(self):
    if self._sensor_state():
        evento = CRUDEventos.ConsultarPorNombre(self.name)
        if evento:
            foto = CapturarImagen(IpDvr + evento.url)

            EnviarNotificacionPorCanal(evento.canal_notificacion, evento.titulo, evento.descripcion, foto)

            condiciones = CRUDCondicionesManuales.ConsultarMarcado()
            escenarios = CRUDEventoCondicionEscenario.CosultarEC(evento.id, condiciones.id)
            for escenario in escenarios:
                EjecutarEscenario(escenario.escenario)

            EnviarCorreo(evento.destinatarios, evento.titulo, evento.descripcion, f"Capturas/{foto}")


class HikSensor(object):
    """ Hik camera sensor."""

    def __init__(self, sensor, channel, cam):
        """Init"""
        self._cam = cam
        self._name = "{} {} {}".format(self._cam.cam.name, sensor, channel)
        self._id = "{}.{}.{}".format(self._cam.cam.cam_id, sensor, channel)
        self._sensor = sensor
        self._channel = channel

        self._cam.cam.add_update_callback(self.update_callback, self._id)

    def _sensor_state(self):
        """Extract sensor state."""
        return self._cam.get_attributes(self._sensor, self._channel)[0]

    def _sensor_last_update(self):
        """Extract sensor last update time."""
        return self._cam.get_attributes(self._sensor, self._channel)[3]

    @property
    def name(self):
        """Return the name of the Hikvision sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return '{}.{}'.format(self.__class__, self._id)

    @property
    def is_on(self):
        """Return true if sensor is on."""
        return self._sensor_state()

    def update_callback(self, msg):
        print('Callback: {}'.format(msg))
        print('{}:{} @ {}'.format(self.name, self._sensor_state(), self._sensor_last_update()))
        ManejarEveto(self)


IpDvr = CargarDatosSensibles("IP_DVR")
usuario = CargarDatosSensibles("USUARIO_DVR")
clave = CargarDatosSensibles("CLAVE_DVR")


def main():
    cam = HikCamObject(IpDvr, 80, usuario, clave)

    entities = []

    for sensor, channel_list in cam.sensors.items():
        for channel in channel_list:
            entities.append(HikSensor(sensor, channel[1], cam))


main()
