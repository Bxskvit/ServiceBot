from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


class HistoryMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state: FSMContext = data["state"]

        # Handle go_back BEFORE handler
        if isinstance(event, CallbackQuery) and event.data == "go_back":
            return await self.go_back(event, state)

        # Run handler first
        result = await handler(event, data)

        # Then auto-save screen
        if isinstance(event, CallbackQuery):
            msg = event.message

            # If handler deleted message → ignore
            if msg and msg.text:
                await self.save_screen(state, msg)

        return result

    async def save_screen(self, state: FSMContext, msg: Message):
        data = await state.get_data()
        stack = data.get("screen_stack", [])

        screen = {
            "text": msg.text,
            "keyboard": msg.reply_markup.model_dump() if msg.reply_markup else None,
            "fsm_state": await state.get_state()
        }

        # Ignore duplicate
        if stack and stack[-1] == screen:
            return

        stack.append(screen)
        await state.update_data(screen_stack=stack)

    async def go_back(self, event: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        stack = data.get("screen_stack", [])

        # If no history → wipe state
        if not stack:
            await state.clear()
            await event.answer("Nothing to go back to.")
            return

        # Remove current screen
        current = stack.pop()

        # Optional: remove temp keys
        for key in ("item_id", "bid_price", "temp_data"):
            data.pop(key, None)

        if not stack:
            await state.clear()
            await state.update_data(screen_stack=[])
            await event.message.edit_text("Main Menu")
            return

        last = stack[-1]
        await state.update_data(screen_stack=stack)

        # Restore FSM state
        await state.set_state(last["fsm_state"]) if last["fsm_state"] else await state.clear()

        kb = None
        if last["keyboard"]:
            from aiogram.types import InlineKeyboardMarkup
            kb = InlineKeyboardMarkup.model_validate(last["keyboard"])

        try:
            await event.message.edit_text(last["text"], reply_markup=kb)
        except:
            await event.message.answer(last["text"], reply_markup=kb)

        await event.answer()

#
# from aiogram import BaseMiddleware
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
#
#
# class HistoryMiddleware(BaseMiddleware):
#     async def __call__(self, handler, event, data):
#         if isinstance(event, CallbackQuery):
#             state: FSMContext = data["state"]
#
#             if event.data == "go_back":
#                 return await self.go_back(event, state)
#             else:
#                 msg = event.message
#                 if msg:
#                     await self.push_screen_if_changed(state, msg)
#
#         return await handler(event, data)
#
#     async def push_screen_if_changed(self, state: FSMContext, msg):
#         data = await state.get_data()
#         stack = data.get("screen_stack", [])
#
#         last = stack[-1] if stack else None
#         current_state = await state.get_state()  # current FSM state
#
#         screen_obj = {
#             "text": msg.text,
#             "keyboard": msg.reply_markup.model_dump() if msg.reply_markup else None,
#             "fsm_state": current_state
#         }
#
#         # Skip duplicate
#         if last:
#             if last["text"] == screen_obj["text"] and last["keyboard"] == screen_obj["keyboard"]:
#                 return
#
#         # Save new screen
#         stack.append(screen_obj)
#         await state.update_data(screen_stack=stack)
#
#     async def go_back(self, event: CallbackQuery, state: FSMContext):
#         data = await state.get_data()
#         stack = data.get("screen_stack", [])
#
#         if not stack:
#             await state.clear()
#             await event.answer("Nothing to go back to.")
#             return
#
#         # Pop current screen
#         current_screen = stack.pop()
#
#         # Remove any temporary data associated with this screen
#         keys_to_remove = ["item_id", "bid_price", "temp_data"]  # add keys you use per screen
#         for key in keys_to_remove:
#             if key in data:
#                 data.pop(key)
#
#         if not stack:
#             # Nothing left → clear everything
#             await state.clear()
#             await state.update_data(screen_stack=[])
#             await event.answer("Back.")
#             return
#
#         # Restore previous screen
#         last = stack[-1]
#         await state.update_data(screen_stack=stack)
#
#         # Restore FSM state
#         if last.get("fsm_state"):
#             await state.set_state(last["fsm_state"])
#         else:
#             await state.clear()
#
#         # Restore message
#         text = last["text"]
#         kb = last["keyboard"]
#
#         await event.message.edit_text(
#             text=text,
#             reply_markup=event.message.reply_markup.__class__.model_validate(kb)
#             if kb else None
#         )
#
#         await event.answer()