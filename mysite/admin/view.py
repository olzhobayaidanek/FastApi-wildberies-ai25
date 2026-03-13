from sqladmin import ModelView
from mysite.db.models import UserProfile,SubCategory,Product,Category



class UserProfileView(ModelView,model=UserProfile):
    column_list = [UserProfile.id,UserProfile.username]

class SubCategoryView(ModelView,model=SubCategory):
    column_list = [SubCategory.id,SubCategory.sub_category_name]

class ProductView(ModelView,model=Product):
    column_list = [Product.id,Product.product_name]

class CategoryView(ModelView,model=Category):
    column_list = [Category.id,Category.category_name]
