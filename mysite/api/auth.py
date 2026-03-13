from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import UserProfile,RefreshToken
from mysite.db.schema import RegisterSchema,LoginSchema
from passlib.context import CryptContext
from datetime import timedelta,timezone,datetime
from typing import Optional
from mysite.config import SECRET_KEY,ACCESS_EXPIRE_TOKEN,REFRESH_EXPIRE_TOKEN,ALGORITHM
from jose import jwt




auth_router = APIRouter(prefix='/auth', tags=['Authorization'])
pwd_context = CryptContext(schemes='bcrypt', deprecated='auto')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#def  create_access_token(data: dict,expires_delta:Optional[timedelta] = None ):
 #  to_encode = data.copy()
  # if expires_delta:
   #    expire = datetime.now(timezone.utc) + expires_delta
   #else:
    #   expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_TOKEN)
   #to_encode.update({'exp': expire})
   #encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
   #return encoded_jwt


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE_TOKEN)
    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def create_refresh_token(data: dict):
    return create_access_token(data=data, expires_delta=timedelta(days=REFRESH_EXPIRE_TOKEN))


@auth_router.post('/register',response_model= dict)
async def register(user_data: RegisterSchema,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user_data.username).first()
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Mynday adam registration bolgon')

    hash_password = get_password_hash(user_data.password)
    user = UserProfile(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        username = user_data.username,
        phone_number = user_data.phone_number,
        password = hash_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'massage': 'Ийгиликтуу Регистрация болдунуз'}

@auth_router.post('/login',response_model=dict)
async def login(user_data: LoginSchema,db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user_data.username).first()
    if not user_db or not verify_password(user_data.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Registration bolunuz')
    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    token_db = RefreshToken(token=refresh_token, user_id=user_db.id)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)


    return{
        'access_token' : access_token,
        'refresh_token' : refresh_token,
        'type':'bearer'
    }


@auth_router.post('/logout', response_model=dict)
async def logout(refresh_token: str, db:Session = Depends(get_db)):
    refresh_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    db.delete(refresh_db)
    db.commit()
    return{'message': 'success logout'}


@auth_router.post('/access_generate',response_model=dict)
async def generate_access(refresh_token: str, db:Session = Depends(get_db)):
    refresh_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    access_token = create_access_token({'sub': refresh_db.user_id})
    return {
        'access_token': access_token,
        'type': 'bearer'
    }











































