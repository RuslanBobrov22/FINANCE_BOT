from aiogram import Dispatcher, Bot, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

TOKEN_API = '5877628371:AAHWG5VgtLHMxKskCOku4xkIPZQDXZwA06U'

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):  # информирования для старта бота
    print('the second bot strated')


class Client_state_question(StatesGroup):  # классы для хранения
    que = State()


class Client_state_offer(StatesGroup):  # классы для хранения
    of = State()


def get_keyboard():  # клавиатура
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('вопрос разработчикам')).add('предложение для улучшения')
    return kb


@dp.message_handler(commands=['start'])
async def starter(message: types.Message):
    await message.answer('вы запустили бота!')
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEIrIFkQtpxIGoOAzxZCHna2ZToFNkIGQACFBIAAnCfSEsTGBPylOhieC8E',
                           reply_markup=get_keyboard())


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await message.reply('Твое действие отменено',
                        reply_markup=get_keyboard())

    await state.finish()


def get_cancel():
    kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
    kb2.add(KeyboardButton('/cancel'))
    return kb2


@dp.message_handler(Text(equals='вопрос разработчикам', ignore_case=True), state=None)  # функция для вопросов
async def start_work(message: types.Message):
    await Client_state_question.que.set()
    await message.answer('Тайное послание разработчику...',
                         reply_markup=get_cancel())


@dp.message_handler(Text(equals='предложение для улучшения', ignore_case=True), state=None)  # функция для - предложение для улучшения
async def start_work(message: types.Message):
    await Client_state_offer.of.set()
    await message.answer('предлжить что-нибудь интересненькое',
                         reply_markup=get_cancel())


@dp.message_handler(state=Client_state_question.que)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['que'] = message.text
    await message.reply('данные получены')

    await state.finish()


@dp.message_handler(state=Client_state_offer.of)
async def load_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['of'] = message.text
    await message.reply('спасибо за предложение')
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEIsE9kRCUDuyOEtaJJUgKDM3UAAXXpWoUAAp4QAAJnVohLA7Ek-tgVL2ovBA')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)