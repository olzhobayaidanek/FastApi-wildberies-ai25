from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Category
from mysite.db.schema import CategorySchema
from typing import List




category_router = APIRouter(prefix='/category',tags=['Category'])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/create', response_model=CategorySchema)
async def create_category(category_date: CategorySchema, db:Session = Depends(get_db)):
    category_db = Category(category_name=category_date.category_name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.get('/list',response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    category_db = db.query(Category).all()
    return category_db

@category_router.get('/detail',response_model=CategorySchema)
async def detail_category(category_id: int,db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mynday category jok')
    return category_db


@category_router.put('/update', response_model=CategorySchema)
async def update_category(category_id: int ,category_data: CategorySchema, db:Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mynday category jok eken')
    category_db.category_name = category_data.category_name
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.delete('/delete', response_model=dict)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Mynday category jok eken')
    db.delete(category_db)
    db.commit()
    return {'message': 'Success delete'}









