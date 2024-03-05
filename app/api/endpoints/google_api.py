from aiogoogle import Aiogoogle
from app.core.constants import SHEETS_URL
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import CharityProjecDBSchema
from app.service.google_api import (set_user_permissions, spreadsheets_create,
                                    spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjecDBSchema],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session=session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services=wrapper_services)
    await set_user_permissions(
        spreadsheetid=spreadsheet_id,
        wrapper_services=wrapper_services
    )
    await spreadsheets_update_value(
        spreadsheetid=spreadsheet_id,
        close_projects=projects,
        wrapper_services=wrapper_services
    )
    print(SHEETS_URL + spreadsheet_id)
    return projects