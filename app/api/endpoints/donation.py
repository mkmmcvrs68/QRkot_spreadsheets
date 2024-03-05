from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import RESPONSE_MODEL_EXCLUDE
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas.donation import CreateDonationSchema, DonationDBSchema
from app.service.donations_func import distribution_donations_by_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSchema],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=DonationDBSchema,
    response_model_exclude=RESPONSE_MODEL_EXCLUDE,
    response_model_exclude_none=True
)
async def create_donation(
    donation_in: CreateDonationSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donate = await donation_crud.create(
        obj_in=donation_in,
        session=session,
        user=user,
        need_commit=False
    )
    await distribution_donations_by_project(obj=donate, session=session)
    await session.commit()
    await session.refresh(donate)
    return donate


@router.get(
    '/my',
    response_model=list[DonationDBSchema],
    response_model_exclude_none=True,
    response_model_exclude=RESPONSE_MODEL_EXCLUDE,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_user_donations(user=user, session=session)