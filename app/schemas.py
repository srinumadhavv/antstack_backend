from pydantic import BaseModel,EmailStr,ValidationError, validator
from datetime import datetime


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class CouponCreate(BaseModel):
    id:str
    start_date:int
    expiry_date:int
    type:str
    discount:int
    min_amount:int

class Checkout(BaseModel):
    amount:int
    coupon:str