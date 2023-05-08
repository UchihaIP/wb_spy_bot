from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.services import get_lenght_spy_list


async def get_options_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(InlineKeyboardButton(text="Просмотреть список отслеживания", callback_data="spy_list"))
    keyboard.row(InlineKeyboardButton(text="Добавить новые ссылки", callback_data="add_spy"))
    return keyboard


async def get_url_index(client_id: int):
    ids = await get_lenght_spy_list(client_id=client_id)
    keyboard = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [InlineKeyboardButton(text=f"❌ {id}", callback_data=f"index-{id}")]
                                        for id in ids
                                    ])
    keyboard.row(InlineKeyboardButton(text="Вернуться в меню.", callback_data="start"))
    return keyboard


async def get_cancel_button():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return keyboard
