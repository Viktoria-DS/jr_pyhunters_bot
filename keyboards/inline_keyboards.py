from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from collections import namedtuple
from .callback_data import CallbackMenu, CallbackTalk, CallbackQuiz, CallbackTranslate
Button = namedtuple('Button', ['text', 'callback'])
import os
from utils.enum_path import Path
from utils import file_manager, FileManager


def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Рандомный факт', 'random'),
        Button('Разговор с ChatGPT', 'gpt'),
        Button('Диалог с известной личностью', 'talk'),
        Button('Квиз', 'quiz'),
        Button('Переводчик', 'translate'),
        Button('Голосовой разговор с ChatGPT', 'voice'),
        Button('Picture recognition', 'picture')
    ]

    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback)
        )
    keyboard.adjust(2,2)
    return keyboard.as_markup()

def ikb_random():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Подобрать другой интересный факт', 'random'),
        Button('Закончить', 'start'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback),
        )
    return keyboard.as_markup()


def ikb_gpt_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Сделать ещё один запрос', 'gpt'),
        Button('Закончить', 'start'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback),
        )
    return keyboard.as_markup()

def ikb_cancel_gpt():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = 'Отменить',
        callback_data = CallbackMenu(button = 'start'),
        )
    return keyboard.as_markup()

def ikb_talk_menu():
    keyboard = InlineKeyboardBuilder()
    celebrity = [file.rsplit('.', 1)[0] for file in os.listdir(Path.IMAGES_DIR.value) if file.startswith('talk_')]
    for item in celebrity:
        text_button = FileManager.read_txt(Path.PROMPTS, item).split(',', 1)[0].split(' - ')[-1]
        keyboard.button(
            text = text_button,
            callback_data = CallbackTalk(
                button = 'talk',
                celebrity = item,
            )
        )
    keyboard.button(
        text = 'Вернуться в главное меню',
        callback_data = CallbackMenu(button = 'start'),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_talk_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = 'Закончить',
        callback_data=CallbackMenu(button = 'start'),
    )
    return keyboard.as_markup()

def ikb_quiz_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button ('Программирование', 'quiz_prog'),
        Button ('Математика', 'quiz_math'),
        Button ('Биология', 'quiz_biology'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackQuiz(
                button = 'quiz',
                subject = button.callback,
            )
        )
    keyboard.button(
        text='Вернуться в главное меню',
        callback_data=CallbackMenu(button='start'),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_quiz_navigation():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Ещё вопрос',
        callback_data=CallbackQuiz(
            button='quiz',
            subject = 'quiz_more'),
    )
    keyboard.button(
        text='Поменять тему игры',
        callback_data=CallbackMenu(button='quiz'),
    )
    keyboard.button(
        text='Вернуться в главное меню',
        callback_data=CallbackMenu(button='start'),
        )
    return keyboard.as_markup()

def ikb_translate_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button ('Английский', 'translate_en'),
        Button ('Немецкий', 'translate_de'),
        Button ('Испанский', 'translate_es'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackTranslate(
                button = 'translate',
                language = button.callback,
            )
        )
    keyboard.button(
        text='Вернуться в главное меню',
        callback_data=CallbackMenu(button='start'),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_translate_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = 'Закончить',
        callback_data=CallbackMenu(button = 'translate'),
    )
    return keyboard.as_markup()

def ikb_voice_gpt_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Ещё запрос', 'voice'),
        Button('Закончить', 'start'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback)
        )
    return keyboard.as_markup()


def ikb_picture_gpt_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('One more picture', 'picture'),
        Button('Закончить', 'start'),
    ]
    for button in buttons:
        keyboard.button(
            text = button.text,
            callback_data = CallbackMenu(button = button.callback)
        )
    return keyboard.as_markup()
