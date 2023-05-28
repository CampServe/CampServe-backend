from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from Providers.ProviderModel import Providers


from base import Base


class Ratings(Base):
    __tablename__ = "ratings"
    rating_id = Column(Integer, primary_key=True, nullable=False)
    provider_id = Column(Integer, ForeignKey(Providers.provider_id), nullable=False)
    no_of_stars = Column(Integer, nullable=False)
    comments = Column(String(255), nullable=False)

# Relationships
provider = relationship("Providers", back_populates="ratings")