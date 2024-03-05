from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (CLOSSED_PROJECT_CANT_EDIT,
                                DETAIL_FOR_CHECK_DUPLICATE_NAME,
                                INCORRECT_FULL_AMOUNT,
                                INVESTED_AMOUNT_IN_PROJECT_CANT_DELETE,
                                PROJECT_NOT_FOUND)
from app.crud import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_by_name(
        name=name, session=session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DETAIL_FOR_CHECK_DUPLICATE_NAME,
        )


async def get_project_by_id(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_NOT_FOUND
        )

    return charity_project


async def check_project_for_invested_amount_before_delete(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await get_project_by_id(
        project_id=project_id,
        session=session
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=INVESTED_AMOUNT_IN_PROJECT_CANT_DELETE
        )

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CLOSSED_PROJECT_CANT_EDIT
        )
    return charity_project


async def check_closed_project(
    project_id: int,
    obj_in: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await get_project_by_id(
        project_id=project_id, session=session
    )

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CLOSSED_PROJECT_CANT_EDIT
        )
    if (obj_in.full_amount and (charity_project.invested_amount > obj_in.full_amount)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=INCORRECT_FULL_AMOUNT
        )

    return charity_project