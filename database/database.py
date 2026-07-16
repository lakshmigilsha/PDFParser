from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("sqlite://", echo=True)
#Base.metadata.create_all(engine)
class Base(DeclarativeBase):
    pass