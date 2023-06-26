from sqlalchemy import String, Integer, Column, ForeignKey
from Users.UserModel import User
from Providers.ProviderModel import Providers



from base import Base

class Requests(Base):
    __tablename__ = "requests"
    request_id = Column("request_id",Integer, primary_key =True, nullable = False)
    provider_id = Column("provider_id",Integer,ForeignKey(Providers.provider_id),nullable=False)
    user_id = Column("user_id",Integer,ForeignKey(User.user_id),nullable=False)
    agreed_price = Column("agreed_price",String(255),nullable=False)        
    location = Column("location",String(255),nullable=False)
    payment_mode = Column("payment_mode",String(255),nullable=False)
    scheduled_datetime = Column("scheduled_datetime",String(255),nullable=False)
    status_comp_inco = Column("status_comp_inco",String(255),nullable=False)
    status_acc_dec = Column("status_acc_dec",String(255),nullable=False)
    payment_mode = Column("payment_mode",String(255),nullable=False)
    