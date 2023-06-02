from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from .config import TOKEN, OPENAI_TOKEN
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from django.conf import settings
from BotGPT.models import Dialog, Message
import openai

openai.api_key = OPENAI_TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dialog = []


class Command(BaseCommand):
    help = 'Telegram bot setup command'

    def handle(self, *args, **options):
        sync_to_async(executor.start_polling(dp))


@dp.message_handler(commands=['delete_dialog'])
async def delete_dialog(message: types.Message):
    dialog_str = f"{message.from_user.username}"

    dialogs = await sync_to_async(Dialog.objects.filter)(username=dialog_str)

    dialogs = await sync_to_async(list)(dialogs)

    for dialog in dialogs:
        await sync_to_async(dialog.delete)()

    messages = await sync_to_async(Message.object.filter)(dialog_username=dialog_str)

    messages = await sync_to_async(list)(messages)

    for message in messages:
        await sync_to_async(message.delete)()

    await message.reply("Диалог с ассистентом удалён.")


@sync_to_async
def save_user_message(dialog, user_input):
    role_user = 'user'
    dialog_obj, _ = Dialog.object.get_or_create(username=f"{dialog}", role=role_user)
    user_message = Message(dialog=dialog_obj, role=role_user, content=user_input)
    user_message.save()


@sync_to_async
def save_assistant_message(dialog, answer):
    role_assistant = 'assistant'
    dialog_obj, _ = Dialog.objects.get_or_create(username=f"{dialog}", role=role_assistant)
    assistant_message = Message(dialog=dialog_obj, role=role_assistant, content=answer)
    assistant_message.save()


@dp.message_handler()
async def handler_message(message: types.Message):
    if message.text == "/delete_dialog":
        await delete_dialog(message)

    user_input = message.text

    dialog_str = f"{message.from_user.username}"

    await save_user_message(dialog_str, user_input)

    dialog_objs = await sync_to_async(Dialog.objects.filter)(username=f"{dialog_str}")
    previous_message = await sync_to_async(Message.objects.flter)(dialog__in=dialog_objs)

    messages = await sync_to_async(
        lambda: [
                    {"role": "system", "content": "You are a helpful assistant"},
                ] + [
                    {"role": message.role, "content": message.content}
                    for message in previous_message
                ] + [
                    {"role": "user", "content": user_input}
                ]
    )()

    response = await sync_to_async(openai.ChatCompletion.create)(
        model='gpt-3.5-turbo-0301',
        messages=messages
    )

    answer = response.choices[0].message.content

    await save_assistant_message(dialog_str, answer)

    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
