import base64
import io

import httpx
import openai
from aiogram import Bot

import config
from .enums import GPTModel
from .messages import GPTMessage


class GPTService:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, model: GPTModel = GPTModel.GPT_4_TURBO):
        self._gpt_token = config.OPENAI_API_KEY
        self._proxy = config.PROXY
        self._client = self._create_client()
        self._model = model.value


    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._gpt_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
            )
        )
        return gpt_client


    async def request(self, message_list: GPTMessage, bot: Bot) -> str:
        try:
            response = await self._client.chat.completions.create(
                messages=message_list.message_list,
                model=self._model,
                )
            return response.choices[0].message.content
        except Exception as e:
            await bot.send_message(
                chat_id=config.ADMIN_ID,
                text=str(e),
        )

    async def voice_to_text (self,ogg_bytes, bot: Bot):
        try:
            audio_buf = io.BytesIO(ogg_bytes)
            audio_buf.name = 'voice.ogg'
            audio_buf.seek(0)

            response = await self._client.audio.transcriptions.create(
                model = "whisper-1",
                file = audio_buf,
            )
            return response.text or ""
        except Exception as e:
            await bot.send_message(
                chat_id = config.ADMIN_ID,
                text = str(e)
            )

    async def text_to_voice(self, response: str, voice: str, response_format: str, bot: Bot) -> bytes:
        try:
            resp = await self._client.audio.speech.create(
                    model = "gpt-4o-mini-tts",
                    voice = voice,
                    input = response,
                    response_format= response_format,
            )
            if hasattr(resp, 'read'):
                return resp.read()
            if hasattr(resp, 'content'):
                return resp.content
            return bytes(resp)
        except Exception as e:
            await bot.send_message(
                chat_id = config.ADMIN_ID,
                text = str(e)
            )
            return b""
    async def image_to_text (self, image_bytes: bytes, instruction: str,  bot: Bot) -> str:
        try:
            picture_bytes = base64.b64encode(image_bytes).decode("utf-8")
            data_url = f"data:image/jpg;base64,{picture_bytes}"
            resp = await self._client.responses.create(
                model = "gpt-4-turbo",
                messages = [{
                    "role": "user",
                    "content": [{
                        "type": "text", "text": instruction,
                        "type": "image_url", "image_url": data_url
                    }],
                }],
            )
            return resp.choices[0].message.content
        except Exception as e:
            await bot.send_message(
                chat_id = config.ADMIN_ID,
                text = str(e)
            )

