from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from config import OPENAI_TOKEN
import openai

openai.api_key = OPENAI_TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dialog = []


@dp.message_handler()
async def handler_message(message: types.Message):
    global dialog
    print(message.text)
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

    print(answer+'\n')

    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
