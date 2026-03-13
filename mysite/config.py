import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

ACCESS_EXPIRE_TOKEN= int(os.getenv('ACCESS_EXPIRE_TOKEN','60'))
REFRESH_EXPIRE_TOKEN= int(os.getenv('REFRESH_EXPIRE_TOKEN','3'))
ALGORITHM= os.getenv('ALGORITHM','HS256')









