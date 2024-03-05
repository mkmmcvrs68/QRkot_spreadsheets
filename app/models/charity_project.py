from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LENGTH_CHARITY_PROJECT_NAME

from .base_model import BaseModel


class CharityProject(BaseModel):
    name = Column(
        String(MAX_LENGTH_CHARITY_PROJECT_NAME),
        unique=True,
        nullable=False
    )
    description = Column(Text)
