from fastapi import APIRouter ,Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Product
from mysite.db.schema import ProductSchema
from typing import List

product_router = APIRouter(prefix='/product', tags=['Product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/create')
async def create_product(product_data: ProductSchema, db:Session =  Depends(get_db)):
    product_db  = Product(**product_data.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get('/list', response_model=List[ProductSchema])
def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/detail',response_model=ProductSchema)
async def detail_product(product_id: int,db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mynday category jok')
    return product_db



@product_router.put('/update/{product_id}', response_model=ProductSchema)
def update_product(
    product_id: int,
    product_data: ProductSchema,
    db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mynday product jok' )

    product_db.product_name = product_data.product_name
    db.commit()
    db.refresh(product_db)
    return product_db



@product_router.delete('/delete', response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mynday category jok eken')
    db.delete(product_db)
    db.commit()
    return {'message': 'Success delete'}


