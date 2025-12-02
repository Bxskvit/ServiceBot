from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup


class HistoryMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, CallbackQuery):
            state: FSMContext = data["state"]

            # Skip saving when going back
            if event.data != "go_back":
                msg = event.message
                if msg:
                    await self.push_screen_if_changed(state, msg)

        return await handler(event, data)

    async def push_screen_if_changed(self, state: FSMContext, msg):
        data = await state.get_data()
        stack = data.get("screen_stack", [])

        last = stack[-1] if stack else None

        # If last screen is identical → skip push
        if last:
            if last["text"] == msg.text and \
               last["keyboard"] == (msg.reply_markup.model_dump() if msg.reply_markup else None):
                return  # skip duplicate

        # Otherwise push
        stack.append({
            "text": msg.text,
            "keyboard": msg.reply_markup.model_dump() if msg.reply_markup else None
        })

        await state.update_data(screen_stack=stack)

