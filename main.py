from bot import bot, dp
from filters.custom_filters import AllowedUserFilter
import asyncio
import handlers
from middleware.callback import HistoryMiddleware


async def run_bot():
    # Register routers
    dp.include_router(handlers.user.user_router)
    dp.include_router(handlers.admin.admin_router)
    dp.include_router(handlers.callback.callback_router)
    dp.message.filter(AllowedUserFilter())
    dp.callback_query.middleware(HistoryMiddleware())
    print('Bot was started successfully!')
    # Start polling the bot (this should be awaited)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(
        run_bot()
    )


if __name__ == '__main__':
    asyncio.run(main())
