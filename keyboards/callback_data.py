from aiogram.filters.callback_data import CallbackData

class CallbackMenu(CallbackData, prefix = 'CM'):
    button: str

class CallbackTalk(CallbackData, prefix = 'CT'):
    button: str
    celebrity: str


class CallbackQuiz(CallbackData, prefix = 'CQ'):
    button: str
    subject: str

class CallbackTranslate(CallbackData, prefix = 'CQ'):
    button: str
    language: str