from fastapi import FastAPI

from mysite.api.sub_category import sub_category_router
from mysite.api.user_profile import user_router
from mysite.api.category import category_router
from mysite.api.product import product_router
from mysite.api.auth import auth_router
from mysite.admin.setup import setup_admin


wildberies_app = FastAPI(title='Wildberies-AI25')
wildberies_app.include_router(user_router)
wildberies_app.include_router(category_router)
wildberies_app.include_router(product_router)
wildberies_app.include_router(sub_category_router)
wildberies_app.include_router(auth_router)
setup_admin(wildberies_app)


