from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import SubCategory
from mysite.db.schema import SubCategorySchema
from typing import List


sub_category_router = APIRouter(prefix='/sub_category', tags=['SubCategory'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





@sub_category_router.post('/create')
def create_subcategory(data: SubCategorySchema, db: Session = Depends(get_db)):
    sub = SubCategory(sub_category_name=data.sub_category_name,category_id=data.category_id)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@sub_category_router.get('/list', response_model=List[SubCategorySchema])
def get_subcategories(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()

@sub_category_router.get('/detail',response_model=SubCategorySchema)
def get_subcategory(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(SubCategory).filter(SubCategory.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return sub


@sub_category_router.put('/update')
def update_subcategory(sub_id: int, data: SubCategorySchema, db: Session = Depends(get_db)):
    sub = db.query(SubCategory).filter(SubCategory.id == sub_id).first()

    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    sub.sub_category_name = data.sub_category_name
    sub.category_id = data.category_id

    db.commit()
    db.refresh(sub)
    return sub


@sub_category_router.delete('/delete')
def delete_subcategory(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(SubCategory).filter(SubCategory.id == sub_id).first()

    if not sub:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(sub)
    db.commit()

    return {"message": "Deleted successfully"}