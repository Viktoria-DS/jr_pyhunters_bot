from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InputMediaPhoto, BufferedInputFile
from aiogram.types.input_file import FSInputFile
from keyboards import ikb_main_menu, ikb_random, ikb_gpt_menu, ikb_talk_back, ikb_quiz_navigation, ikb_translate_back, ikb_voice_gpt_menu, ikb_picture_gpt_menu
import config, io
from utils import FileManager
from utils.enum_path import Path
from ai_open import chat_gpt
from ai_open.messages import GPTMessage
from aiogram.enums.chat_action import ChatAction
from keyboards.callback_data import CallbackMenu
from aiogram.fsm.context import FSMContext
from .fsm import GPTRequest, CelebrityTalk, Quiz, Translator, GPTVoice, GPTImage
from ai_open.enums import GPTRole
fsm_router = Router()

@fsm_router.message(GPTRequest.wait_for_request)
async def wait_for_user_request(message: Message, state: FSMContext, bot: Bot):
    user_request = message.text
    msg_list = GPTMessage('gpt')
    msg_list.update(GPTRole.USER, message.text)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )
    response = await chat_gpt.request(msg_list, bot)
    # print(msg_list.message_list)
    message_id = await state.get_value('message_id')
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file= 'gpt')),
            caption=response,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup = ikb_gpt_menu()
    )

@fsm_router.message(CelebrityTalk.dialog)
async def user_dialog_with_celebrity(message: Message, state: FSMContext, bot: Bot):
    message_list = await state.get_value('messages')
    celebrity = await state.get_value('celebrity')
    message_list.update(GPTRole.USER, message.text)
    response = await chat_gpt.request(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages = message_list)
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=FSInputFile(Path.IMAGES.value.format(file = celebrity)),
        caption=response,
        reply_markup = ikb_talk_back()
    )

@fsm_router.message(Quiz.game)
async def user_answer(message: Message, state: FSMContext, bot: Bot):
    message_list = await state.get_value('messages')
    message_id = await state.get_value('message_id')
    score = await state.get_value('score')
    message_list.update(GPTRole.USER, message.text)
    response = await chat_gpt.request(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages=message_list)
    if response == 'Правильно!':
        score += 1
        await state.update_data(score=score)
    response += f'\n\n Ваш счет {score} очков.'
    await bot.delete_message(
        chat_id = message.from_user.id,
        message_id = message.message_id
    )
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file='quiz')),
            caption=response,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=ikb_quiz_navigation()
    )

@fsm_router.message(Translator.translate)
async def user_translation(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    lang = data.get('language')
    edit_msg_id = data.get("edit_msg_id")
    message_list = await state.get_value('messages')
    if not message_list:
        message_list = GPTMessage('translate')
    message_list.update(GPTRole.USER, f"Перевод на {lang} язык:\n{message.text}")
    response = await chat_gpt.request(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages=message_list)
    await bot.edit_message_caption(

        caption=response,
        chat_id=message.from_user.id,
        message_id=edit_msg_id,
        reply_markup=ikb_translate_back()
    )

@fsm_router.message(GPTVoice.wait_for_voice)
async def wait_for_user_request(message: Message, state: FSMContext, bot: Bot):
    audio_id = message.voice.file_id
    tg_file = await bot.get_file(audio_id)
    buf = io.BytesIO()
    await bot.download_file(tg_file.file_path, destination = buf)
    buf.seek(0)
    ogg_bytes = buf.getvalue()
    if not ogg_bytes:
        await message.answer("I could not download your message")
        return
    recognized_text = await chat_gpt.voice_to_text(ogg_bytes, bot)
    if not recognized_text:
        await message.answer("I could not recognize your message")
        return
    msg_list = GPTMessage('gpt')
    msg_list.update(GPTRole.USER, recognized_text)
    gpt_response = await chat_gpt.request(msg_list, bot)
    if not gpt_response:
        await message.answer("I could not generate a response")
        return
    audio_bytes = await chat_gpt.text_to_voice(gpt_response, "coral", "opus", bot)
    if audio_bytes:
        voice_response = BufferedInputFile(audio_bytes, filename = "gpt_answer.ogg")
        await bot.send_voice(
            chat_id=message.from_user.id,
            voice=voice_response,
        )
    message_id = await state.get_value('message_id')
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file= 'gpt')),
            # caption=gpt_response,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup = ikb_voice_gpt_menu()
    )

@fsm_router.message(GPTImage.wait_for_image, F.photo)
async def wait_for_user_request(message: Message, state: FSMContext, bot: Bot):
    instruction = "Describe the image"
    file_id = message.photo[-1].file_id
    tg_file = await bot.get_file(file_id)
    buf = io.BytesIO()
    await bot.download_file(tg_file.file_path, destination = buf)
    buf.seek(0)
    image_bytes = buf.getvalue()
    result = await chat_gpt.image_to_text(image_bytes, instruction, bot)
    if not result:
        await message.answer("I could not recognize your image")
        return
    message_id = await state.get_value('message_id')
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file= 'gpt')),
            caption=result,
        ),
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup = ikb_picture_gpt_menu()
    )