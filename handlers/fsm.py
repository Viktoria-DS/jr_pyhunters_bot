from aiogram.fsm.state import State, StatesGroup

class GPTRequest(StatesGroup):
    wait_for_request = State()


class CelebrityTalk(StatesGroup):
    dialog = State()


class Quiz(StatesGroup):
    game = State()

class Translator(StatesGroup):
    translate = State()

class GPTVoice(StatesGroup):
    wait_for_voice = State()

class GPTImage(StatesGroup):
    wait_for_image = State()