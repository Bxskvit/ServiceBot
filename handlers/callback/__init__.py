from aiogram import Router
from .comptuer_list_handler import router as computers_list_router
from .posting_details_handlers import router as posting_details_router
from .go_back_handler import router as go_back_router
from .order_list_handler import router as order_list_router

# create a router
callback_router: Router = Router()

callback_router.include_router(computers_list_router)
callback_router.include_router(posting_details_router)
callback_router.include_router(go_back_router)
callback_router.include_router(order_list_router)


__all__ = ["callback_router"]
