from pydantic import BaseModel
from .models import UserStatus
from typing import Optional
from datetime import datetime

class UserProfileSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    age: Optional[int]
    phone_number: str
    profile_image: str
    status: UserStatus
    password: str

class RegisterSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    age: int | None = None

class LoginSchema(BaseModel):
    username: str
    password: str

class CategorySchema(BaseModel):
    category_name: str

class SubCategorySchema(BaseModel):
    category_id: int
    sub_category_name: str

class ProductSchema(BaseModel):
    category_id: int
    sub_category: int
    product_name: str
    description: str | None
    price: int
    product_image: str

class ImageProductSchema(BaseModel):
    product_id: int
    image: str

class ReviewSchema(BaseModel):
    user_id: int
    product_id: int
    images: str | None
    video: str | None
    comment: Optional[str]
    stars: Optional[int]





class CartSchema(BaseModel):
    user_id: int

class CartItemSchema(BaseModel):
    cart_id: int
    product_id: int
    quantity: int

class FavoriteSchema(BaseModel):
    user_id: int

class FavoriteItemSchema(BaseModel):
    favorite_id: int
    product_id: int
    like: bool



