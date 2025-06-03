from FirebaseNotificacionesPush import EnviarNotificacionPorCanal
import requests

# Obtener la URL pública de ngrok desde la API local
try:
    respuesta = requests.get("http://127.0.0.1:4040/api/tunnels")
    if respuesta.status_code == 200:
        datos = respuesta.json()
        for tunel in datos.get("tunnels", []):
            public_url = tunel.get("public_url")
    else:
        public_url = None
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
