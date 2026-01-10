from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from keyboards import ikb_main_menu, ikb_random, ikb_cancel_gpt, ikb_talk_menu, ikb_talk_back, ikb_quiz_menu, ikb_translate_menu, ikb_translate_back
import config
from utils import FileManager
from utils.enum_path import Path
from ai_open import chat_gpt
from ai_open.messages import GPTMessage, GPTRole
from aiogram.enums.chat_action import ChatAction
from keyboards.callback_data import CallbackMenu, CallbackTalk, CallbackQuiz, CallbackTranslate
from aiogram.fsm.context import FSMContext
from .fsm import GPTRequest, CelebrityTalk, Quiz, Translator, GPTVoice, GPTImage

inline_router = Router()

@inline_router.callback_query(CallbackMenu.filter(F.button == 'start'))
@inline_router.callback_query(CallbackMenu.filter(F.button == 'main'))
async def main_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_main_menu()
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'random'))
async def random_handler(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot):
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
    )
    await bot.send_chat_action(
        chat_id = callback.from_user.id,
        action = ChatAction.TYPING,
    )
    response = await chat_gpt.request(GPTMessage('random'), bot)
    await bot.edit_message_media(
        media = InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_random(),

    )


@inline_router.callback_query(CallbackMenu.filter(F.button == 'gpt'))
async def gpt_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.set_state(GPTRequest.wait_for_request)
    await state.update_data(
        message_id=callback.message.message_id,
    )
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_cancel_gpt(),
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'talk'))
async def talk_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_talk_menu(),
    )

@inline_router.callback_query(CallbackTalk.filter(F.button == 'talk'))
async def talk_with_celebrity(callback: CallbackQuery, callback_data: CallbackTalk, state: FSMContext, bot: Bot):
    await state.set_state(CelebrityTalk.dialog)
    message_list = GPTMessage(callback_data.celebrity)
    response = await chat_gpt.request(message_list, bot)
    message_list.update(GPTRole.CHAT, response)
    await state.update_data(messages = message_list, celebrity = callback_data.celebrity)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.celebrity)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_talk_back(),
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'quiz'))
async def quiz_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.set_state(Quiz.game)
    messages = await state.get_value('messages')
    if not messages:
        await state.update_data(score = 0, messages = None, message_id = callback.message.message_id)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_quiz_menu(),
    )

@inline_router.callback_query(CallbackQuiz.filter(F.button == 'quiz'))
async def select_subject(callback: CallbackQuery, callback_data: CallbackQuiz, state: FSMContext, bot: Bot):
    message_list = await state.get_value('messages')
    if not message_list:
        message_list = GPTMessage('quiz')
    message_list.update(GPTRole.USER, callback_data.subject)
    response = await chat_gpt.request(message_list, bot)
    await state.update_data(messages = message_list)
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=response,
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_talk_back(),
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'translate'))
async def translate_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.clear()
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption=FileManager.read_txt(Path.MESSAGES, callback_data.button),
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_translate_menu(),
    )

@inline_router.callback_query(CallbackTranslate.filter(F.button == 'translate'))
async def select_language(callback: CallbackQuery, callback_data: CallbackTranslate, state: FSMContext, bot: Bot):
    await callback.answer()
    await state.set_state(Translator.translate)
    await state.update_data(
        language = callback_data.language,
        edit_chat_id = callback.from_user.id,
        edit_msg_id = callback.message.message_id,
    )

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file=callback_data.button)),
            caption='Пожалуйста, пришли мне текст для перевода',
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_translate_back(),
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'voice'))
async def gpt_voice_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.set_state(GPTVoice.wait_for_voice)
    await state.update_data(
        chat_id = callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file='gpt')),
            caption = 'Пожалуйста, пришли мне голосовое сообщение',
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_cancel_gpt(),
    )

@inline_router.callback_query(CallbackMenu.filter(F.button == 'picture'))
async def gpt_voice_menu(callback: CallbackQuery, callback_data: CallbackMenu, state: FSMContext, bot: Bot):
    await state.set_state(GPTImage.wait_for_image)
    await state.update_data(
        chat_id = callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=FSInputFile(Path.IMAGES.value.format(file='gpt')),
            caption = 'Пожалуйста, пришли мне картинку для описания',
        ),
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup = ikb_cancel_gpt(),
    )