from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from random import randint
from BotGPT.management.commands.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

win = 0
num1 = 0
num2 = 0

button_1 = KeyboardButton('Привет!')
button_2 = KeyboardButton('Как дела?')
button_3 = KeyboardButton('Помоги!')
repl_mark = ReplyKeyboardMarkup()
repl_mark.add(button_1, button_2, button_3)


@dp.message_handler(commands='game')
async def game_bot(message: types.Message):
    global win, num1, num2

    win = randint(1, 100)
    num1 = randint(1, 100)
    num2 = randint(1, 100)

    button_1G = KeyboardButton(f' {num1}')
    button_2G = KeyboardButton(f' {num2}')
    button_3G = KeyboardButton(f'{win}')

    repl_mark2 = ReplyKeyboardMarkup()
    repl_mark2.add(button_1G, button_2G, button_3G)
    await message.reply('Угадай моё число!', reply_markup=repl_mark2)


@dp.message_handler(commands='inline')
async def start_bot(message: types.Message):
    inline_btn_1 = InlineKeyboardButton('Первая кнопка', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('Вторая кнопка', callback_data='button2')

    inline_km_1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)


    await message.reply('Привет, я бот!', reply_markup=inline_km_1)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Первая кнопка нажата!')


@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вторая кнопка нажата!')


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    await message.reply('Привет, я бот!', reply_markup=repl_mark)


@dp.message_handler(content_types="text")
async def echo_bot(message: types.Message):
    global num1
    global num2
    global win

    if message.text.lower() == 'привет' or message.text.lower() == 'привет!':
        await message.answer('Ты дурак')
    elif message.text.lower() == 'как дела' or message.text.lower() == 'как дела?':
        await message.answer('Хорошо, кот умер.')
    elif message.text.lower() == 'помоги' or message.text.lower() == 'помоги!':
        await message.answer('Не')
    elif message.text.lower() == 'ты дурак':
        await message.answer('Сам дурак!')
    elif message.text == str(win):
        await message.answer('Урааа! Я умнее чем компьютер!')
    elif message.text == str(num1):
        await message.answer('Хаха. У меня памяти 16 Мега байт!')
    elif message.text == str(num2):
        await message.answer('Хаха. У меня памяти 16 Мега байт!')
    else:
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
