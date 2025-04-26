import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.responses import FileResponse
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel

app = FastAPI()

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=404
        )

class LoginModel(BaseModel):
    usuario: str
    clave: str


@app.get("/Capturas/{nombreImagen}")
def RetornarCaptura(nombreImagen: str, api_key: APIKey = Depends(get_api_key)):
    rutaImagen = f'Capturas/{nombreImagen}'

    if os.path.exists(rutaImagen):
        return FileResponse(rutaImagen)
    else:
        # Si no se encuentra la imagen, devolver un error 404
        raise HTTPException(status_code=404)

@app.post("/Usuarios/Login")
async def Login(loginModel: LoginModel, response: Response, api_key: APIKey = Depends(get_api_key)):
    usuario_bd = True
    if usuario_bd is None:
        raise HTTPException(status_code=401, detail="Usuario o clave incorrectos")
    response.status_code = 200
    return response

# Api de Pruebas