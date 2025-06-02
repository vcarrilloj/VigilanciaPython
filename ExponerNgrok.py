import subprocess
import time
import requests

from CorreoElectronico import EnviarCorreo
from FirebaseNotificacionesPush import EnviarNotificacionPorCanal

# Iniciar ngrok (modo http en el puerto 5000)
subprocess.Popen(['ngrok', 'http', '8050'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Esperar unos segundos para que ngrok arranque
time.sleep(5)

# Obtener la URL pública de ngrok desde la API local
try:
    response = requests.get("http://localhost:4040/api/tunnels")
    public_url = response.json()['tunnels'][0]['public_url']
    print(response)
except Exception as e:
    print(f"Error obteniendo la URL de ngrok: {e}")
    public_url = None

# Enviar por Firebase si se obtuvo la URL
if public_url:
    canal = 'CanalVigilancia'
    titulo = 'URL'
    mensaje = public_url
    foto = ''
    EnviarNotificacionPorCanal(canal, titulo, mensaje, foto)
    #EnviarCorreo(["juliofer93@gmail.com"], "Url NGROK", public_url, None)
