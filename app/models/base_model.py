from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.constants import INVESTED_AMOUNT_DEFAULT
from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=INVESTED_AMOUNT_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
