import os
from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel

from BD.DB import CRUDEscenarios, CRUDCondicionesManuales,  CRUDEventos, CRUDAcciones
from DatosSensibles import VerificarUsuario, GuardarUsuario, GuardarDatosSensiblesBD
from Escenarios import EjecutarEscenario
from TuyaDispositivos import ObtenerDispositivos

app = FastAPI()

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


class LoginModel(BaseModel):
    usuario: str
    clave: str


class EscenarioModel(BaseModel):
    nombre: str
    descripcion: str


class CondicionModel(BaseModel):
    nombre: str
    descripcion: str
    seleccionado: bool


class EventoModel(BaseModel):
    nombre: str
    descripcion: str
    dispositivo: str
    tipo: str
    url: str
    titulo: str
    canal_notificacion: str
    destinatarios: list[str]


class AccionModel(BaseModel):
    escenario: int
    id_dispositivo: str
    comando: str
    orden: int


class DatosSensiblesModel(BaseModel):
    llave: str
    valor: str


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=404
        )


@app.post("/Usuarios/Registro")
async def Registro(loginModel: LoginModel, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        GuardarUsuario(loginModel.usuario, loginModel.clave)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al registrar el usuario {loginModel.usuario}")
    else:
        response.status_code = 200
        return response


@app.post("/Usuarios/Login")
async def Login(loginModel: LoginModel, response: Response, api_key: APIKey = Depends(get_api_key)):
    usuario_bd = VerificarUsuario(loginModel.usuario, loginModel.clave)
    if usuario_bd is None:
        raise HTTPException(status_code=401, detail="Usuario o clave incorrectos")
    response.status_code = 200
    return response


@app.get("/Capturas/{nombreImagen}")
def RetornarCaptura(nombreImagen: str, api_key: APIKey = Depends(get_api_key)):
    rutaImagen = f'Capturas/{nombreImagen}'

    if os.path.exists(rutaImagen):
        return FileResponse(rutaImagen)
    else:
        # Si no se encuentra la imagen, devolver un error 404
        raise HTTPException(status_code=404)


@app.get("/Dispositivos/Consultar")
def ConsultarDispositivos(api_key: APIKey = Depends(get_api_key)):
    try:
        resultado = ObtenerDispositivos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        return resultado


@app.get("/Escenarios/Consultar/")
def ConsultarEscenarios(id: Optional[int] = None, api_key: APIKey = Depends(get_api_key)):
    try:
        resultado = CRUDEscenarios.ConsultarTodos(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        return resultado


@app.get("/Escenarios/Acciones/{id}")
def ConsultarEscenarios(id: int, api_key: APIKey = Depends(get_api_key)):
    try:
        resultado = CRUDAcciones.ConsultarPoreEscenario(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        return resultado


@app.post("/Escenarios/Insertar")
def InsertarEscenarios(escenarios: list[EscenarioModel], response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDEscenarios.Insertar(escenarios)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.delete("/Escenarios/Eliminar")
def EliminarEscenarios(id_escenario: int, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDEscenarios.Eliminar(id_escenario)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.post("/Escenarios/Ejecutar/{id}")
def EjecutarEscenarios(id: int, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        EjecutarEscenario(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.get("/Condiciones/Consultar/")
def ConsultarCondiciones(id: Optional[int] = None, api_key: APIKey = Depends(get_api_key)):
    try:
        resultado = CRUDCondicionesManuales.ConsultarTodos(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        return resultado


@app.post("/Condiciones/Insertar")
def InsertarCondiciones(condiciones: list[CondicionModel], response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDCondicionesManuales.Insertar(condiciones)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.put("/Condiciones/Editar/{id}/{descripcion}")
def EditarCondiciones(id: int, descripcion: str, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDCondicionesManuales.Editar(id, descripcion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.delete("/Condiciones/Eliminar/{id}")
def EliminarCondiciones(id: int, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDCondicionesManuales.Eliminar(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.put("/Condiciones/Seleccionar/{id}")
def MarcarCondicion(id: int, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDCondicionesManuales.Marcar(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.get("/Eventos/Consultar/")
def ConsultarEventos(id: Optional[int] = None, api_key: APIKey = Depends(get_api_key)):
    try:
        resultado = CRUDEventos.Consultar(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        return resultado


@app.post("/Eventos/Insertar")
def InsertarEventos(eventos: list[EventoModel], response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDEventos.Insertar(eventos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.put("/Eventos/Editar/{id}")
def EditarEventos(id, evento: EventoModel, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        """
        CRUDEventos.Editar(id,
                           nombre=evento.nombre,
                           descripcion=evento.descripcion,
                           dispositivo_origen=evento.dispositivo,
                           tipo=evento.tipo,
                           url=evento.url,
                           titulo=evento.titulo,
                           canal_notificacion=evento.canal_notificacion,
                           destinatarios=evento.destinatarios)
                           """
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.delete("/Eventos/Eliminar/{id}")
def EditarEventos(id, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDEventos.Eliminar(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.get("/Acciones/Consultar/")
def ConsultarAcciones(api_key: APIKey = Depends(get_api_key)):
    try:
        resultado = CRUDAcciones.Consultar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        return resultado


@app.post("/Acciones/Insertar")
def InsertarAcciones(acciones: list[AccionModel], response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDAcciones.Insertar(acciones)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.put("/Acciones/Editar")
def EditarAcciones(acciones: AccionModel, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDAcciones.Actualizar(acciones.escenario, acciones.orden, acciones.id_dispositivo, acciones.comando)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.delete("/Acciones/Eliminar/{escenario}/{orden}")
def EliminarAcciones(escenario: int, orden: int, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        CRUDAcciones.Eliminar(escenario, orden)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        return response


@app.post("/DatosSensibles/Guardar")
def GuardarDatosSensibles(datoSensible: DatosSensiblesModel, response: Response, api_key: APIKey = Depends(get_api_key)):
    try:
        GuardarDatosSensiblesBD(datoSensible.llave, datoSensible.valor)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    else:
        response.status_code = 200
        response.body = api_key
        return response
