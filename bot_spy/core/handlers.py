import asyncio
from contextlib import suppress
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified

from core.config import settings
import core.constants as const
from core.logger import logger
from core.keyboards import get_options_buttons, get_url_index, get_cancel_button
from core.services import get_spy_list, add_urls_in_db, delete_url

class SpyFSM(StatesGroup):
    urls = State()

class Handers:
    def __init__(self, bot, dp) -> None:
        self.bot: Bot = bot
        self.dp: Dispatcher = dp

    async def start_command_handler(self, event: Message | CallbackQuery):
        logger.debug(f"{event.from_user.id}: Start command")
        if isinstance(event, Message):
            if event.from_user.id in settings.ADMIN_IDS:
                logger.debug(f"{event.from_user.id}: Admin is auth")
                keyboard = await get_options_buttons()
                return await event.answer(text=const.START_MESSAGE, reply_markup=keyboard)
            return await event.answer(text="🥷🏼 У вас нет прав на пользование ботом.")
        if isinstance(event, CallbackQuery):
            keyboard = await get_options_buttons()
            return await event.message.edit_text(text=const.START_MESSAGE, reply_markup=keyboard)


    async def show_spy_list_handler(self, event: CallbackQuery):
        logger.debug(f"{event.from_user.id}: Spy list command")
        spy_list, ok = await get_spy_list(settings.CLIENT_ID)
        if ok:
            keyboard = await get_url_index(settings.CLIENT_ID)
            await event.answer("📀")
            return await event.message.answer(text=spy_list, reply_markup=keyboard)
        return await event.message.answer(text=spy_list)

    async def add_spy_url_handler(self, event: CallbackQuery):
        keyboard = await get_cancel_button()
        await event.message.answer(text=const.SPY_START_MESSAGE, reply_markup=keyboard)
        await SpyFSM.urls.set()


    async def add_url_handler(self, event: Message, state=FSMContext):
        urls = event.text.split(",")
        await event.delete()
        ok = await add_urls_in_db(settings.CLIENT_ID, urls)
        if ok:
            await event.answer("🥷🏼 Добавление прошло успешно! ✅")
            return await state.finish()
        await event.answer("При добавлении произошла ошибка!")
        return await state.finish() 


    async def delete_url_handler(self, event: CallbackQuery):
        index = int(event.data.split("-")[1])
        logger.debug(f"delete_url_handler -> index {index}")
        await delete_url(client_id=settings.CLIENT_ID, index=index)
        await event.answer("Удалено ✅")
        spy_list, ok = await get_spy_list(settings.CLIENT_ID)
        if ok:
            await asyncio.sleep(1)
            keyboard = await get_url_index(settings.CLIENT_ID)
            await event.answer("📀")
            return await event.message.edit_text(text=spy_list, reply_markup=keyboard)
        return await event.message.edit_text(text="🥷🏼 Список отслеживания пуст.")


    async def cancel_button_handler(self, event: CallbackQuery, state: FSMContext):
        await event.answer("Запрос отменен ✅")
        await state.finish()


    async def register_handlers(self):
        self.dp.register_message_handler(self.start_command_handler, 
                                         filters.RegexpCommandsFilter(
                                            regexp_commands=[r"(?i)\/start"]))
        self.dp.register_callback_query_handler(self.start_command_handler,
                                                lambda callback: callback.data == "start")
        self.dp.register_callback_query_handler(self.show_spy_list_handler, 
                                                lambda callback: callback.data == "spy_list")
        self.dp.register_callback_query_handler(self.add_spy_url_handler, 
                                                lambda callback: callback.data == "add_spy")
        self.dp.register_message_handler(self.add_url_handler, 
                                         state=SpyFSM.urls)
        self.dp.register_callback_query_handler(self.delete_url_handler, 
                                                lambda callback: callback.data.startswith("index-"))
        self.dp.register_callback_query_handler(self.cancel_button_handler,
                                                lambda callback: callback.data == "cancel",
                                                state="*")
