from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    credentials_path = settings.GOOGLE_CALENDAR_CREDENTIALS

    if not credentials_path:
        raise ValueError("GOOGLE_CALENDAR_CREDENTIALS não está configurado.")

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES
    )

    return build("calendar", "v3", credentials=credentials)


def get_inicio_fim(test_drive):
    timezone = ZoneInfo("Europe/Lisbon")

    inicio = datetime.combine(
        test_drive.tdr_data,
        test_drive.tdr_hora
    ).replace(tzinfo=timezone)

    fim = inicio + timedelta(hours=1)

    return inicio, fim


def criar_evento_test_drive(test_drive):
    service = get_calendar_service()
    inicio, fim = get_inicio_fim(test_drive)

    evento = {
        "summary": f"{test_drive.tdr_estado.upper()} - Test-drive - {test_drive.tdr_nome}",
        "description": f"""
Cliente: {test_drive.tdr_nome}
Email: {test_drive.tdr_email}
Telefone: {test_drive.tdr_telefone}

Veículo: {test_drive.tdr_vei.marca} {test_drive.tdr_vei.modelo}
Matrícula: {test_drive.tdr_vei.vei_matricula}

Estado: {test_drive.tdr_estado}

Observações:
{test_drive.tdr_observacoes or "Sem observações."}
""",
        "start": {
            "dateTime": inicio.isoformat(),
            "timeZone": "Europe/Lisbon",
        },
        "end": {
            "dateTime": fim.isoformat(),
            "timeZone": "Europe/Lisbon",
        },
    }

    return service.events().insert(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        body=evento
    ).execute()