from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field
    password: str
    active: Optional[bool] = Field(default = True, index=True)
    uuid: Optional[str] = Field(index=True)
    created_at: Optional[datetime] = Field(default = datetime.now())