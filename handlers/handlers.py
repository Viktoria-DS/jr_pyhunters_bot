from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from keyboards import ikb_main_menu, ikb_random
import config
from utils import FileManager
from utils.enum_path import Path
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from aiogram.enums.chat_action import ChatAction


command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject):
    # keyboard = None
    # if command.command == 'start':
    #     keyboard = ikb_main_menu()
    await message.answer_photo(
        photo=FSInputFile(Path.IMAGES.value.format(file=command.command)),
        caption=FileManager.read_txt(Path.MESSAGES, command.command),
        reply_markup=ikb_main_menu(),
    )
    print(message.from_user.id)


@command_router.message()
async def all_messages(message: Message, bot: Bot):
    msg_text = f'User {message.from_user.full_name} wrote: \n{message.text} '
    await bot.send_message(
        chat_id=config.ADMIN_ID,
        # chat_id = message.chat.id,
        text=msg_text
    )
