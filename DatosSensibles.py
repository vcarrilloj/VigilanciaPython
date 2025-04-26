import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

from BD.DB import session
from BD.Tablas import DatosSensibles, Usuarios

load_dotenv()

# Cargar las variables desde el archivo .env
secret_key = os.getenv("SECRET_KEY")
cipher = Fernet(secret_key)


def GuardarDatosSensiblesBD(keyName: str, value: str):
    encrypted_value = cipher.encrypt(value.encode())
    nuevoDato = DatosSensibles(key_name=keyName, value=encrypted_value)
    session.add(nuevoDato)
    session.commit()


def CargarDatosSensibles(keyName: str):
    dato = session.query(DatosSensibles).filter_by(key_name=keyName).first()
    if dato:
        decrypted_value = cipher.decrypt(dato.value).decode()
        return decrypted_value
    else:
        return None


def GuardarUsuario(usuario: str, clave: str):
    encrypted_value = cipher.encrypt(clave.encode())
    usuario_nuevo = Usuarios(usuario=usuario, clave=encrypted_value)
    session.add(usuario_nuevo)
    session.commit()


def VerificarUsuario(usuario: str, clave: str):
    usuario = session.query(Usuarios).filter_by(usuario=usuario).first()
    if usuario:
        decrypted_value = cipher.decrypt(usuario.clave).decode()
        if decrypted_value == clave:
            return usuario
        else:
            return None
    else:
        return usuario


# GuardarDatosSensibles("","")
# print(CargarDatosSensibles(""))
#VerificarUsuario("MAESTRIA", "Maestria.123456")
