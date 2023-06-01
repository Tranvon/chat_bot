from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from .config import TOKEN, OPENAI_TOKEN
from django.core.management.base import BaseCommand
from django.conf import settings
import openai

openai.api_key = OPENAI_TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dialog = []


class Command(BaseCommand):
    help = 'Telegram bot setup command'

    def handle(self, *args, **options):
        executor.start_polling(dp)


@dp.message_handler()
async def handler_message(message: types.Message):
    global dialog
    print('Пользователь: '+message.text + '\n')
    user_input = message.text

    dialog.append({'role': 'user', 'content': user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *dialog
        ]
    )
    answer = response.choices[0].message.content

    dialog.append({'role': 'assistant', 'content': answer})

    print('Ответ: '+answer + '\n')

    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
