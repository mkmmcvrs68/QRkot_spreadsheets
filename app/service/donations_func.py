from datetime import datetime
from typing import TypeVar, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject, Donation

ModelType = TypeVar('ModelType', CharityProject, Donation)


async def close(obj: Union[CharityProject, Donation]) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def distribution_donations_by_project(
        obj: Union[CharityProject, Donation],
        session: AsyncSession,
) -> None:
    model = Donation if isinstance(obj, CharityProject) else CharityProject
    open_objs = await charity_project_crud.get_all_open(model, session)
    amount_to_invest = obj.full_amount
    for open_obj in open_objs:
        amount = open_obj.full_amount - open_obj.invested_amount
        invested_amount = min(amount, amount_to_invest)
        open_obj.invested_amount += invested_amount
        amount_to_invest -= invested_amount
        if open_obj.full_amount == open_obj.invested_amount:
            await close(open_obj)
        if not amount_to_invest:
            await close(obj)
