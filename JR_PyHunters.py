from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import Command
from aiogram.types import Message
import config

bot = Bot(token = config.BOT_TOKEN)

dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message):
    print(message)


@dp.message()
async def all_messages(message: Message, bot: Bot):
    msg_text = f'User {message.from_user.full_name} wrote: \n{message.text} '
    await bot.send_message(
        chat_id = 483413434,
        # chat_id = message.chat.id,
        text = msg_text
    )


async def start_bot():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())


