from aiogram import Router
from .comptuer_list_handler import router as computers_list_router


# create a router
callback_router: Router = Router()

callback_router.include_router(computers_list_router)

__all__ = ["callback_router"]
