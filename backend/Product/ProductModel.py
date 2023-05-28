from sqlalchemy import String, Integer, Column,ForeignKey
from sqlalchemy.orm import relationship
from Providers.ProviderModel import Providers



from base import Base

class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True, nullable=False)
    provider_id = Column(Integer, ForeignKey(Providers.provider_id), nullable=False)
    product_name = Column(String(255), nullable=False)

    # Relationships
    provider = relationship("Providers", back_populates="product")