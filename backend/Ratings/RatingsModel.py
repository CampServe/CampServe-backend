from sqlite3 import Date
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from Providers.ProviderModel import Providers
from Users.UserModel import User


from base import Base


class Ratings(Base):
    __tablename__ = "ratings"
    rating_id = Column("rating_id", Integer, primary_key=True, nullable=False)
    provider_id = Column("provider_id",Integer, ForeignKey(Providers.provider_id), nullable=False)
    user_id = Column("user_id",Integer,ForeignKey(User.user_id),nullable=False)
    no_of_stars = Column("no_of_stars",Integer, nullable=False)
    comments = Column("comments", String(255), nullable=False)
    timestamp = Column("timestamp",String(255),nullable=False)

# Relationships
provider = relationship("providers",uselist=False,back_populates="providers")
