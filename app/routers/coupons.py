from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
import time 
import calendar

router = APIRouter(
    prefix='/coupons',
    tags=['Coupons']
)

@router.get('/',status_code=status.HTTP_200_OK)
def get_coupons(db : Session = Depends(get_db)):
    coupouns=db.query(models.Coupons).all()
    return {"coupons":coupouns}

@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_user( coupon : schemas.CouponCreate, db : Session = Depends(get_db)):
    coupon_id=coupon.id
    coupon_type=coupon.type
    start_date=coupon.start_date
    expiry_date=coupon.expiry_date
    discount=coupon.discount
    min_amount = coupon.min_amount
    query = db.query(models.Coupons).filter(models.Coupons.id == coupon_id)
    coupon_name=query.first()
    current_time=calendar.timegm(time.gmtime(0))
    if coupon_name and coupon_name.expiry_date > current_time:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Coupon already exists in database")
    # if coupon_type.lower() not in ["percentage","fixed"] :
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"type must be either percentage or fixed")
    if start_date > expiry_date :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"expiry date must be greater than or equal to Start Date")
    if coupon_type == "fixed" and discount > min_amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Discount cannot be greater than Min Amount")
    new_coupon= models.Coupons(**coupon.dict())
    print(new_coupon)
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    res={"id":coupon_id,"expiry_date":expiry_date,"discount":discount,"min_amount":min_amount}
    return res
