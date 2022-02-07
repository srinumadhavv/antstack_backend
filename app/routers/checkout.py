from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
import time 
import calendar

router = APIRouter(
    prefix='/checkout',
    tags=['Checkout']
)

@router.post('/',status_code=status.HTTP_200_OK)
def create_user( checkout : schemas.Checkout, db : Session = Depends(get_db)):
    amount = checkout.amount
    coupon_code = checkout.coupon
    current_time=calendar.timegm(time.gmtime())
    query=db.query(models.Coupons).filter(models.Coupons.id == coupon_code)
    coupon_exists=query.first()
    if coupon_exists :
        print(coupon_exists.expiry_date)
        print(current_time)
        if coupon_exists.start_date >= current_time:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Coupon Is not Valid")
        if coupon_exists.expiry_date <= current_time:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Coupon Expired")
        if amount < coupon_exists.min_amount :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="To apply this coupon amount should be greater then min amount")
        coupon_type= coupon_exists.type
        if coupon_type == "percentage":
            final_amount = amount - (coupon_exists.discount/100)*amount
            discounted_amount=(coupon_exists.discount/100)*amount
        elif coupon_type == "fixed":
            final_amount = amount - coupon_exists.discount
            discounted_amount = coupon_exists.discount
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Coupon Is not Valid")
    return {"total_amount":final_amount,"discount":discounted_amount}
