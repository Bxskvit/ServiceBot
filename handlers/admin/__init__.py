from aiogram import Router
from .admin_mode_handler import router as admin_mode_router


# create a router
admin_router: Router = Router()

admin_router.include_router(admin_mode_router)

__all__ = ["admin_router"]
