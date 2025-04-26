import firebase_admin
from firebase_admin import credentials, messaging

# Inicializar la aplicación Firebase con el archivo de credenciales
cred = credentials.Certificate('Llave/vigilancia.json')
firebase_admin.initialize_app(cred)


def EnviarNotificacion(registration_token, message_title, message_body):
    # Crear el mensaje
    message = messaging.Message(
        notification=messaging.Notification(
            title=message_title,
            body=message_body,
        ),
        token=registration_token,
    )

    # Enviar el mensaje
    response = messaging.send(message)
    return response


def EnviarNotificacionPorCanal(canal, titulo, mensaje, foto):
    data = {
        'foto': foto,
        "titulo": titulo,
        "mensaje": mensaje
    }

    message = messaging.Message(
        topic=canal,
        data=data
    )

    response = messaging.send(message)
    return response


# Ejemplo de uso
topic = 'CanalVigilancia'
message_title = "Detección de Movimiento"
message_body = "Se detecto movimiento en la puerta."
foto = 'prueba.png'

response = EnviarNotificacionPorCanal(topic, message_title, message_body, foto)

print(f'Mensaje enviado: {response}')
