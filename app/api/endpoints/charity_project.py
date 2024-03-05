from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_closed_project, check_name_duplicate,
    check_project_for_invested_amount_before_delete)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import (CharityProjecDBSchema,
                                         CreateCharityProjectSchema,
                                         UpdateCharityProjectSchema)
from app.service.donations_func import distribution_donations_by_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjecDBSchema],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=CharityProjecDBSchema,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CreateCharityProjectSchema,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(
        name=charity_project.name,
        session=session
    )
    charity_project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session,
        need_commit=False
    )
    await distribution_donations_by_project(obj=charity_project, session=session)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjecDBSchema,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_for_invested_amount_before_delete(
        project_id=project_id, session=session
    )
    charity_project = await charity_project_crud.remove(charity_project, session=session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjecDBSchema,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: UpdateCharityProjectSchema,
    session: AsyncSession = Depends(get_async_session)
):
    if obj_in.name is not None:
        await check_name_duplicate(
            name=obj_in.name,
            session=session
        )
    charity_project = await check_closed_project(
        project_id=project_id,
        obj_in=obj_in,
        session=session,
    )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session, need_commit=False
    )
    await distribution_donations_by_project(obj=charity_project, session=session)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project