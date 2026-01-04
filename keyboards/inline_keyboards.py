from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from collections import namedtuple
from .callback_data import CallbackMenu, CallbackTalk, CallbackQuiz
Button = namedtuple('Button', ['text', 'callback'])
import os
from utils.enum_path import Path
from utils import file_manager, FileManager


def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button('Random fact', 'random'),
        Button('Ask GPT', 'gpt'),
        Button('Talk with a celebrity', 'talk'),
        Button('Quiz', 'quiz'),
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
        Button('I want another fact', 'random'),
        Button('Finish', 'start'),
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
        Button('Another request', 'gpt'),
        Button('Finish', 'start'),
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
        text = 'Cancel',
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
        text = 'In the main menu',
        callback_data = CallbackMenu(button = 'start'),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_talk_back():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text = 'Finish',
        callback_data=CallbackMenu(button = 'start'),
    )
    return keyboard.as_markup()

def ikb_quiz_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        Button ('Programming', 'quiz_prog'),
        Button ('Mathematics', 'quiz_math'),
        Button ('Biology', 'quiz_biology'),
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
        text='In the main menu',
        callback_data=CallbackMenu(button='start'),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()

def ikb_quiz_navigation():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Another question',
        callback_data=CallbackQuiz(
            button='quiz',
            subject = 'quiz_more'),
    )
    keyboard.button(
        text='Change topic',
        callback_data=CallbackMenu(button='quiz'),
    )
    keyboard.button(
        text='In the main menu',
        callback_data=CallbackMenu(button='start'),
        )
    return keyboard.as_markup()

