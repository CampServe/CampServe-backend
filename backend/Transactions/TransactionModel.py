from sqlalchemy import String, Integer, Date, ForeignKey, Column
from sqlalchemy.orm import relationship
from Requests.RequestsModel import Requests
from Users.UserModel import User


from base import Base


class Transactions(Base):
    __tablename__ ="transactions"
    transaction_id = Column("transaction_id",Integer, primary_key=True,nullable=False)
    request_id = Column("request_id",Integer, ForeignKey(Requests.request_id),nullable=False)
    user_id = Column("user_id",Integer, ForeignKey(User.user_id),nullable=False)
    amount = Column("amount",String(255),nullable = False)
    has_paid =  Column("has_paid",String(255),nullable = True)
    recepient_number=Column("recepient_number",String(255),nullable=False)
    paylink=Column("paylink",String(255),nullable=True)
