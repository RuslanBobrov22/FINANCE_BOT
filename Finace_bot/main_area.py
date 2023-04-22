from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from manage_of_db import create, add_value, choose_column, max_column, min_column, store, store_add, store_less, \
    data_filter, data_count, count_column
from config import *

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)


def get_keyboard():  # клавиатура
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Начать работу!')).add('создать области').add('посмотреть статистику') \
        .add('максимум', 'минимум').add('ограничение', 'остаток').add('отфильтровать по дате') \
        .add('колличество за день', 'колличество в области')
    return kb


def get_cancel():
    kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
    kb2.add(KeyboardButton('/cancel'))
    return kb2


async def on_startup(_):  # информирования для старта бота
    print('the bot strated')


class Client_state_group(StatesGroup):  # классы для хранения
    desc = State()
    value = State()


class Client_state_table(StatesGroup):
    table = State()


class Client_state_stat(StatesGroup):
    col = State()


class Client_state_max(StatesGroup):
    name = State()


class Client_state_min(StatesGroup):
    name_2 = State()


class Client_state_store(StatesGroup):
    store = State()


class Client_state_data(StatesGroup):
    data = State()


class Client_state_count_d(StatesGroup):
    data_c = State()


class Client_state_count_col(StatesGroup):
    data_c = State()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Привет🖐️! Этот бот создан того чтобы помочь которолировать тебе твои финансы')
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEIhbxkMv6j1wE6DZTtjtsBwDSVoFRLWwACWg8AAsFkiUtoBn1ASv7hiC8E',
                           reply_markup=get_keyboard())


@dp.message_handler(commands=['menu'])
async def start_message(message: types.Message):
    await message.answer('Пожалуйста, выберете область', reply_markup=get_keyboard())


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer(TEXT_HELP,
                         parse_mode='HTML')


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Твое действие отменено',
                        reply_markup=get_keyboard())

    await state.finish()


@dp.message_handler(Text(equals='Начать работу!', ignore_case=True), state=None)  # функция для вывода клавиатуры
async def start_work(message: types.Message):
    await Client_state_group.desc.set()
    await message.answer('Область трат',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='создать области', ignore_case=True), state=None)
async def start_work(message: types.Message):
    await Client_state_table.table.set()
    await message.answer('задать области',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='посмотреть статистику', ignore_case=True),
                    state=None)  # статистика для столбца Client_state_count_col
async def start_work(message: types.Message):
    await Client_state_stat.col.set()
    await message.answer('расчитать статистику (напишите столбец)',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='колличество в области', ignore_case=True), state=None)  # сумма в области
async def start_work(message: types.Message):
    await Client_state_count_col.data_c.set()
    await message.answer('посчитать колличество (напишите столбец)',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='максимум', ignore_case=True), state=None)  # максимум в области
async def start_work(message: types.Message):
    await Client_state_max.name.set()
    await message.answer('узнать максимум (напишите столбец)',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='минимум', ignore_case=True), state=None)  # минимум в области
async def start_work(message: types.Message):
    await Client_state_min.name_2.set()
    await message.answer('узнать минимум (напишите столбец)',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='ограничение', ignore_case=True), state=None)  # сумма на которую
# расчитывает пользователь
async def start_work(message: types.Message):
    await Client_state_store.store.set()
    await message.answer('напишиту сумму в которую вы хотите уложиться',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='остаток', ignore_case=True), state=None)  # остаток от суммы пользователя
async def start_work(message: types.Message):
    await message.answer(f'ваш остаток {store()}',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='отфильтровать по дате', ignore_case=True), state=None)
async def start_work(message: types.Message):
    await Client_state_data.data.set()
    await message.answer(f'напишиту день за который вы хотите посмотреть общую трату дата в формате месяц.день',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='колличество за день', ignore_case=True), state=None)
async def start_work(message: types.Message):
    await Client_state_count_d.data_c.set()
    await message.answer(f'напишиту день за который вы хотите узнать колличество покупок дата в формате месяц.день',
                         reply_markup=get_cancel())


# ПЕРЕЧИСЛЕНЫ ФУНКЦИИ ДЛЯ СОХРАНЕНИЯ ЗНАЧЕНИЯ И ОБРАЩЕНИЕ К SQLITE
@dp.message_handler(state=Client_state_count_d.data_c)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['data_c'] = message.text
    await message.answer(f'колличество покупок за этот день {data_count(message.text)}')
    await state.finish()


@dp.message_handler(state=Client_state_data.data)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['data'] = message.text
    await message.answer(f'общая трата за этот день {data_filter(message.text)}')
    await state.finish()


@dp.message_handler(state=Client_state_store.store)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['store'] = message.text
    store_add(message.text)
    await message.reply('данные получены!')
    await state.finish()


@dp.message_handler(state=Client_state_count_col.data_c)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['data_c'] = message.text
    await message.reply('данные получены!')
    await message.answer(f'колличество покупок {count_column(message.text)}')
    await state.finish()


@dp.message_handler(state=Client_state_min.name_2)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_2'] = message.text
    await message.reply('данные получены')
    await message.answer(text=min_column(message.text))

    await state.finish()


@dp.message_handler(state=Client_state_max.name)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('данные получены')
    await message.answer(text=max_column(message.text))

    await state.finish()


@dp.message_handler(state=Client_state_stat.col)  # выбор колонки для подсчета суммы
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['col'] = message.text
    await message.reply('данные получены')
    await message.answer(text=choose_column(message.text))

    await state.finish()


@dp.message_handler(state=Client_state_table.table)
async def load_value(message: types.Message, state: FSMContext):
    create(message.text.split())
    async with state.proxy() as data:
        data['table'] = message.text
    await message.reply('Все сохранено!')
    await message.answer('Спасибо 🤓!')

    await state.finish()


@dp.message_handler(state=Client_state_group.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text

    await Client_state_group.next()
    await message.reply('Теперь отправьте сумму')


@dp.message_handler(state=Client_state_group.value)
async def load_value(message: types.Message, state: FSMContext):
    flag = True
    async with state.proxy() as data:
        if store() - int(message.text) >= 0:
            store_less(int(message.text))
            data['value'] = message.text
        else:
            flag = False

    if flag:
        await message.reply('Все сохранено')
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=data['desc'])
        async with state.proxy() as data:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=data['value'])
        add_value(data['desc'], data['value'])
        await message.answer('Спасибо!☺️')
    else:
        await message.answer('на счету надостаточно средств(((')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)