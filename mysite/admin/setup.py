from .view import UserProfile,SubCategory,Product,Category
from sqladmin import Admin
from fastapi import FastAPI
from mysite.db.database import engine


from mysite.admin.view import (UserProfileView, CategoryView,ProductView,SubCategoryView)


def setup_admin(app:FastAPI):
    admin = Admin(app, engine=engine)
    admin.add_view(UserProfileView)
    admin.add_view(CategoryView)
    admin.add_view(ProductView)
    admin.add_view(SubCategoryView)





