from .database import Base
from sqlalchemy .orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,Enum,ForeignKey,Text,SmallInteger,Boolean
from typing import Optional,List
from enum import Enum as PyEnum

class UserStatus(str,PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(32), unique=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[str] = mapped_column(String)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.simple)
    password: Mapped[str] = mapped_column(String)


    user_review: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                                    cascade='all, delete-orphan')
    cart_user: Mapped['Cart'] = relationship('Cart',back_populates='user', cascade='all, delete-orphan')

    refresh_token: Mapped[List['RefreshToken']] = relationship('RefreshToken',back_populates='user',
                                                               cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='refresh_token')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)

    sub_category: Mapped[List['SubCategory']] = relationship('SubCategory',
                                              back_populates='category',cascade='all, delete-orphan')
    category_product: Mapped[List['Product']] = relationship('Product',
                                              back_populates='category',cascade='all,delete-orphan')

class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    sub_category_name: Mapped[str] = mapped_column(String(32))

    category: Mapped['Category'] = relationship('Category',back_populates='sub_category')
    sub_product: Mapped[List['Product']] = relationship('Product', back_populates='sub_category',
                                                        cascade='all,delete-orphan')

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    sub_category_id: Mapped[int] = mapped_column(ForeignKey('sub_category.id'))
    product_name: Mapped[str] = mapped_column(String(32))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(Integer, default=0)
    product_image: Mapped[str] = mapped_column(String)

    category: Mapped['Category'] = relationship('Category', back_populates='category_product')
    sub_category: Mapped['SubCategory'] = relationship('SubCategory',back_populates='sub_product')
    images_product: Mapped[List['ImageProduct']] = relationship('ImageProduct', back_populates='product',
                                                                cascade='all,delete-orphan')
    reviews_product: Mapped[List['Review']] = relationship('Review',back_populates='product',
                                                                cascade='all, delete-orphan')
    cart_product: Mapped[List['CartItem']] = relationship('CartItem', back_populates='product',
                                                                 cascade='all, delete-orphan')
    favorite_product: Mapped['FavoriteItem'] = relationship('FavoriteItem', back_populates='product',
                                                                cascade='all, delete-orphan' )


class ImageProduct(Base):
    __tablename__ = 'image_product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    image: Mapped[str] = mapped_column(String)

    product: Mapped['Product'] = relationship('Product', back_populates='images_product')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    images: Mapped[Optional[str]] = mapped_column(String,nullable=True)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stars: Mapped[Optional[int]] = mapped_column(SmallInteger,nullable=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_review')
    product: Mapped['Product'] = relationship('Product',back_populates='reviews_product')


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'),unique=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem',back_populates='cart',
                                                   cascade='all,delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int] = mapped_column(SmallInteger,default=1)

    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product: Mapped['Product'] = relationship('Product',back_populates='cart_product')

class Favorite(Base):
    __tablename__ = 'favorite'


    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'),unique=True)

    favorite_items: Mapped[List['FavoriteItem']] = relationship('FavoriteItem',back_populates='favorite',
                                                                cascade='all, delete-orphan')

class FavoriteItem(Base):
    __tablename__ = 'favorite-item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), unique=True)
    like: Mapped[bool] = mapped_column(Boolean, default=False)


    favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='favorite_items')
    product: Mapped['Product'] = relationship('Product',back_populates='favorite_product')
