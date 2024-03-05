from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    @staticmethod
    async def get_user_donations(
            user: User,
            session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)