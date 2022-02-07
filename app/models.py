from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Coupons(Base):
    __tablename__= "Coupons"
    id = Column(String,primary_key=True,nullable=False)
    type = Column(String,nullable=False)
    discount = Column(Integer,nullable=False)
    start_date = Column(Integer,nullable=False)
    expiry_date = Column(Integer,nullable=False)
    min_amount =Column(Integer,nullable=False)
