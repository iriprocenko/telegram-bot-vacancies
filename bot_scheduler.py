import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import time
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from get_hh_ru import Job, get_data, vacancy, print_txt
from data.info import TOKEN_TG, TOKEN_HH, group, params
from data.txt import template
from menu_button import *


logging.basicConfig(filename=r"data/log.txt", level=logging.INFO, format="%(asctime)s %(processName)s %(message)s")
storage = MemoryStorage()
bot = Bot(token=TOKEN_TG, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


# set date
dt = date.today()-timedelta(days=1)

# set parameters
it_params = params.copy()
it_params['schedule'] = 'remote'

finance_params = params.copy()
finance_params['schedule'] = 'remote'

marketing_params = params.copy()
marketing_params['schedule'] = 'remote'

lawyer_params = params.copy()
params['area'] = [1, 2, 3, 4, 66]

# create objects
IT = Job("it", TOKEN_HH, 90000, it_params)
finance = Job("finance", TOKEN_HH, 50000, finance_params)
lawyer = Job("lawyer", TOKEN_HH, 50000, lawyer_params)
marketing = Job("marketing", TOKEN_HH, 50000, marketing_params)


@dp.chat_join_request_handler()
async def join_request(update: types.ChatJoinRequest):
    # .decline() если отклоняем
    await update.approve()
    await bot.send_message(chat_id=group['tech']['id'], text="+1 присоединился")


@dp.message_handler(commands=['get_id', ])
async def send_welcome(message: types.Message):
    await message.reply(message.chat.id)


@dp.channel_post_handler(Command(commands=['menu',]))
@dp.message_handler(commands=['menu'])
async def start_command_handler(message: types.Message):
    await show_main_menu(message.chat.id)


# Submenu btn_city
@dp.callback_query_handler(lambda c: c.data == 'btn_city')
async def btn_city_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_city(callback_query.message.chat.id, callback_query.message.message_id)


# Submenu btn_name
@dp.callback_query_handler(lambda c: c.data == 'btn_name')
async def btn_name_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_name(callback_query.message.chat.id, callback_query.message.message_id)


# Submenu btn_office
@dp.callback_query_handler(lambda c: c.data == 'btn_office')
async def btn_office_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_office(callback_query.message.chat.id, callback_query.message.message_id)


# Submenu btn_distant
@dp.callback_query_handler(lambda c: c.data == 'btn_distant')
async def btn_distant_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_distant(callback_query.message.chat.id, callback_query.message.message_id)


# Submenu btn_salary
@dp.callback_query_handler(lambda c: c.data == 'btn_salary')
async def btn_salary_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_salary(callback_query.message.chat.id, callback_query.message.message_id)


# Submenu btn_experience
@dp.callback_query_handler(lambda c: c.data == 'btn_experience')
async def btn_experience_callback_handler(callback_query: types.CallbackQuery):
    await show_btn_experience(callback_query.message.chat.id, callback_query.message.message_id)


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


async def get_vacancies_list():
    await bot.send_message(chat_id=group['tech']['id'], text="start {}".format(time.strftime('%X')))

    data_IT_lst = get_data(IT)
    data_IT = vacancy(IT, data_IT_lst)
    data_IT.to_pickle(r"data/db/it {0:%d}.{0:%m}.pkl".format(datetime.now()))
    await bot.send_message(chat_id=group['tech']['id'], text="IT {0}".format(len(data_IT)))

    data_finance_lst = get_data(finance)
    data_finance = vacancy(finance, data_finance_lst)
    data_finance.to_pickle(r"data/db/finance {0:%d}.{0:%m}.pkl".format(datetime.now()))
    await bot.send_message(chat_id=group['tech']['id'], text="finance {0}".format(len(data_finance)))

    data_lawyer_lst = get_data(lawyer)
    data_lawyer = vacancy(lawyer, data_lawyer_lst)
    data_lawyer.to_pickle(r"data/db/lawyer {0:%d}.{0:%m}.pkl".format(datetime.now()))
    await bot.send_message(chat_id=group['tech']['id'], text="lawyer {0}".format(len(data_lawyer)))

    data_marketing_lst = get_data(marketing)
    data_marketing = vacancy(marketing, data_marketing_lst)
    data_marketing.to_pickle(r"data/db/marketing {0:%d}.{0:%m}.pkl".format(datetime.now()))
    await bot.send_message(chat_id=group['tech']['id'], text="marketing {0}".format(len(data_marketing)))

    await bot.send_message(chat_id=group['tech']['id'], text="end {}".format(time.strftime('%X')))


async def public_vacancies(vacancies_obj):
    role_df = pd.read_pickle(r"data/db/{0} {1:%d}.{1:%m}.pkl".format(vacancies_obj.professional_role, datetime.now()))
    role_df_f = role_df[role_df['published']==False]
    if role_df_f.empty:
        pass

    else:
        try:
            ind = role_df_f.index[role_df_f['id']==role_df_f['id'].iloc[0]]
            data = {
                'name': role_df_f['name'].iloc[0],
                'professional_roles': role_df_f['professional_roles'].iloc[0],
                'area': role_df_f['area'].iloc[0].replace(" ", "").replace("-", ""),
                'experience': role_df_f['experience'].iloc[0],
                'schedule': role_df_f['schedule'].iloc[0],
                'employment': role_df_f['employment'].iloc[0],
                'salary_from': role_df_f['salary_from'].iloc[0],
                'salary_currency': role_df_f['salary_currency'].iloc[0],
                'description': role_df_f['description'].iloc[0],
                'contacts_name': role_df_f['contacts_name'].iloc[0],
            }
            if pd.isna(role_df_f['salary_to'].iloc[0]):
                data['salary_to'] = ""
            else:
                data['salary_to'] = " до %d" % role_df_f['salary_to'].iloc[0]
            if role_df_f['contacts_email'].iloc[0]:
                data['contacts_email'] = "\n%s" % role_df_f['contacts_email'].iloc[0]
            else:
                data['contacts_email'] = ""
            if role_df_f['contacts_phones'].iloc[0]:
                data['contacts_phones'] = "\n%s" % role_df_f['contacts_phones'].iloc[0]
            else:
                data['contacts_phones'] = ""
            if role_df_f['has_test'].iloc[0]:
                data['apply_alternate_url'] = r'\n<a href="%s">Ссылка на тестовое задание<\a>' % role_df_f['apply_alternate_url'].iloc[0]
            else:
                data['apply_alternate_url'] = ""
            txt = template.format(**data)
            # formatting line break
            txt = print_txt(txt)

            if len(txt) < 4095:
                await bot.send_message(chat_id=group[vacancies_obj.professional_role]['id'], text=txt)
                role_df.at[ind[0], 'published'] = True
                role_df.at[ind[0], 'published_time'] =  datetime.now()
                role_df.to_pickle(r"data/db/{0} {1:%d}.{1:%m}.pkl".format(vacancies_obj.professional_role, datetime.now()))
            else:
                await bot.send_message(chat_id=group['tech']['id'], text="%s %s longer" % (vacancies_obj.professional_role, data['name']))
                role_df.at[ind[0], 'published'] = True
                role_df.to_pickle(r"data/db/{0} {1:%d}.{1:%m}.pkl".format(vacancies_obj.professional_role, datetime.now()))

        except:
            await bot.send_message(chat_id=group['tech']['id'], text="ошибка {0}: {1}".format(time.strftime('%X'), role_df['name'].iloc[0]))
            role_df.at[ind[0], 'published'] = True
            role_df.to_pickle(r"data/db/{0} {1:%d}.{1:%m}.pkl".format(vacancies_obj.professional_role, datetime.now()))

    await asyncio.sleep(10)


async def on_startup():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    time1 = "4"
    time2 = "5-11, 15-19"
    t = "03/20"

    scheduler.add_job(get_vacancies_list, "cron", minute="1", hour=time1, day="*", args=[])
    scheduler.add_job(public_vacancies, "cron", minute=t, jitter=90, hour=time2, day="*", args=[IT, ])
    scheduler.add_job(public_vacancies, "cron", minute=t, jitter=90, hour=time2, day="*", args=[finance, ])
    scheduler.add_job(public_vacancies, "cron", minute=t, jitter=90, hour=time2, day="*", args=[lawyer, ])
    scheduler.add_job(public_vacancies, "cron", minute=t, jitter=90, hour=time2, day="*", args=[marketing, ])

    scheduler.start()

    try:
        await dp.start_polling(bot, allowed_updates=["message", "inline_query", "callback_query", "chat_member", "channel_post", "chat_join_request"])
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(on_startup())
