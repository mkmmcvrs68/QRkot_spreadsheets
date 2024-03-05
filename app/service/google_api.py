from datetime import datetime

from aiogoogle import Aiogoogle
from typing import Optional
from copy import deepcopy
from app.core.config import settings
from app.core.constants import COLUMNCOUNT, FORMAT, ROWCOUNT, SHEETID


PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

SPREADSHEET_BODY_TITLE = 'Отчет на {}'

SPREADSHEET_BODY = {
    'properties': {
        'title': SPREADSHEET_BODY_TITLE,
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': SHEETID,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': ROWCOUNT,
                    'columnCount': COLUMNCOUNT
                }
            }
        }
    ]
}


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body: Optional[dict] = SPREADSHEET_BODY
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(spreadsheet_body)
    spreadsheet_body['properties']['title'] = SPREADSHEET_BODY_TITLE.format(now_date_time)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        close_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    table_values = [
        *table_values,
        *[(
            str(project.name),
            str((project.close_date - project.create_date)),
            str(project.description)
        ) for project in close_projects]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
