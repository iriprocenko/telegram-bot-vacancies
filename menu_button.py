import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.info import TOKEN_TG


logging.basicConfig(filename=r"data/log.txt", level=logging.INFO, format="%(asctime)s %(processName)s %(message)s")
proxy_url = 'http://proxy.server:3128'
storage = MemoryStorage()
bot = Bot(token=TOKEN_TG, proxy=proxy_url)
dp = Dispatcher(bot, storage=storage)


main_keyboard = InlineKeyboardMarkup(row_width=4)
main_keyboard.add(
        InlineKeyboardButton("Город", callback_data="btn_city"),
        InlineKeyboardButton("Должность", callback_data="btn_name")
    )
main_keyboard.add(
        InlineKeyboardButton("Офис", callback_data="btn_office"),
        InlineKeyboardButton("Удалённо", callback_data="btn_distant")
    )
main_keyboard.add(
        InlineKeyboardButton("Зарплата от", callback_data="btn_salary"),
        InlineKeyboardButton("Опыт", callback_data="btn_experience")
    )
main_keyboard.add(
        InlineKeyboardButton("Закрыть меню", callback_data="btn_close_menu")
        )


@dp.message_handler(commands=['menu'])
async def start_command_handler(message: types.Message):
    await show_main_menu(message.chat.id)


# Create the inline keyboard markup
async def show_main_menu(chat_id):
    # Send the menu message with the inline main_keyboard
    await bot.send_message(chat_id=chat_id, text="Выберите раздел:", reply_markup=main_keyboard)


# Submenu btn_city
@dp.callback_query_handler(lambda c: c.data == 'btn_city')
async def btn_city_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_city(callback_query.message.chat.id, callback_query.message.message_id)


# Show submenu city
async def show_btn_city(chat_id, message_id):
    keyboard = InlineKeyboardMarkup(row_width=4)
    keyboard.add(
        InlineKeyboardButton("Москва", callback_data="btn_moscow"),
        InlineKeyboardButton("Санкт-Петербург", callback_data="btn_spb")
    )
    keyboard.add(
        InlineKeyboardButton("Екатеринбург", callback_data="btn_ekb"),
        InlineKeyboardButton("Нижний Новгород", callback_data="btn_nn")
    )
    keyboard.add(
        InlineKeyboardButton("Новосибирск", callback_data="btn_nsbrsk"),
        InlineKeyboardButton("Далее →", callback_data="btn_next")
    )
    keyboard.add(
        InlineKeyboardButton("← Назад", callback_data="btn_back")
    )

    # await bot.send_message(chat_id=user_id, text="city", reply_markup=keyboard)
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)


# Submenu btn_name
@dp.callback_query_handler(lambda c: c.data == 'btn_name')
async def btn_name_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_name(callback_query.message.chat.id, callback_query.message.message_id)


# Show submenu name
async def show_btn_name(chat_id, message_id):
    keyboard = InlineKeyboardMarkup(row_width=4)
    keyboard.add(
        InlineKeyboardButton("Должность1", callback_data="btn_moscow"),
        InlineKeyboardButton("Должность2", callback_data="btn_spb")
    )
    keyboard.add(
        InlineKeyboardButton("Должность3", callback_data="btn_ekb"),
        InlineKeyboardButton("Должность4", callback_data="btn_nn")
    )
    keyboard.add(
        InlineKeyboardButton("Должность5", callback_data="btn_nsbrsk"),
        InlineKeyboardButton("Далее →", callback_data="btn_next")
    )
    keyboard.add(
        InlineKeyboardButton("← Назад", callback_data="btn_back")
    )

    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)


# Submenu btn_office
@dp.callback_query_handler(lambda c: c.data == 'btn_office')
async def btn_office_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_office(callback_query.message.chat.id, callback_query.message.message_id)


# Show submenu office
async def show_btn_office(chat_id, message_id):
    await bot.send_message(chat_id=chat_id, text="Работа в офисе: <...>")


# Submenu btn_distant
@dp.callback_query_handler(lambda c: c.data == 'btn_distant')
async def btn_distant_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_distant(callback_query.message.chat.id, callback_query.message.message_id)


# Show submenu distant
async def show_btn_distant(chat_id, message_id):
    await bot.send_message(chat_id=chat_id, text="Удалённая работа: <...>")


# Submenu btn_salary
@dp.callback_query_handler(lambda c: c.data == 'btn_salary')
async def btn_salary_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_salary(callback_query.message.chat.id, callback_query.message.message_id)


# Show submenu salary
async def show_btn_salary(chat_id, message_id):
    await bot.send_message(chat_id=chat_id, text="От: ")


# Submenu btn_experience
@dp.callback_query_handler(lambda c: c.data == 'btn_experience')
async def btn_experience_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_experience(callback_query.message.chat.id, callback_query.message.message_id)


# Show submenu experience
async def show_btn_experience(chat_id, message_id):
    keyboard = InlineKeyboardMarkup(row_width=4)
    keyboard.add(
        InlineKeyboardButton("Нет опыта", callback_data="btn_exp_no"),
        InlineKeyboardButton("От 1 года до 3 лет", callback_data="btn_exp_1_3")
    )
    keyboard.add(
        InlineKeyboardButton("От 3 до 6 лет", callback_data="btn_exp_3_6"),
        InlineKeyboardButton("Более 6 лет", callback_data="btn_exp_6")
    )
    keyboard.add(
        InlineKeyboardButton("← Назад", callback_data="btn_back"),
        InlineKeyboardButton("Далее →", callback_data="btn_next")
        )

    # await bot.send_message(chat_id=user_id, text="city", reply_markup=keyboard)
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)


# Submenu btn_back
@dp.callback_query_handler(lambda c: c.data == 'btn_back')
async def btn_back_callback_handler(callback_query: types.CallbackQuery):

    # Answer the callback query to remove the loading state from the button
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=main_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'btn_close_menu')
async def callback_close_handler(callback_query: types.CallbackQuery):
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

    # Answer the callback query to remove the loading state from the button
    await callback_query.answer()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
