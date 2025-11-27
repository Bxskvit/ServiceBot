from aiogram import Router
from .start_handler import router as start_router


# create a router
user_router: Router = Router()

user_router.include_router(start_router)

__all__ = ["user_router"]
