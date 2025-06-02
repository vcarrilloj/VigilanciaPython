import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from DatosSensibles import CargarDatosSensibles

SMTP_SERVER = CargarDatosSensibles("SMTP_SERVER")
SMTP_PORT = 465  # Se usa SSL en este caso
EMAIL_SENDER = CargarDatosSensibles("EMAIL_SENDER")
EMAIL_PASSWORD = CargarDatosSensibles("EMAIL_PASSWORD")


def EnviarCorreo(destinatarios: list[str], asunto: str, cuerpo: str, adjunto: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain"))

    if adjunto:
        if os.path.exists(adjunto):
            with open(adjunto, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-Disposition", f"attachment; filename={os.path.basename(adjunto)}")
                msg.attach(img)
        else:
            raise Exception("La imagen no existe en la ruta especificada.")

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatarios, msg.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"Error al enviar el correo: {e}")
