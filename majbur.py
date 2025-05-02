from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from data.check_sub import check
from data.config import CHANNELS
from loader import bot

matn = "Botimizdan foydalanish uchun rasmiy kanalimizga <b>obuna bo'ling</b> va <b>Tekshirish</b> tugmasini bosing."

class Asosiy(BaseMiddleware):
    async def on_pre_process_update(self,xabar:types.Update,data:dict):
        if xabar.message:
            user_id = xabar.message.from_user.id
        elif xabar.callback_query:
            user_id = xabar.callback_query.from_user.id
        else:
            return
        buttons = InlineKeyboardMarkup(row_width=1)
        dastlabki = True
        for k in CHANNELS:
            holat = await check(user_id=user_id,kanal_id=k)
            if holat==1:
                channels = await bot.get_chat(k)
                buttons.insert(InlineKeyboardButton(text=f"✅ {channels.title}", url=f"{await channels.export_invite_link()}"))
            elif holat==0:
                channels = await bot.get_chat(k)
                buttons.insert(InlineKeyboardButton(text=f"❌ {channels.title}", url=f"{await channels.export_invite_link()}"))
            dastlabki *= holat
        if not dastlabki:
            buttons.insert(InlineKeyboardButton(text="🔄 Tekshirish",callback_data="check_subsciption"))
            await bot.send_message(chat_id=user_id,text=matn,disable_web_page_preview=True,
                                    reply_markup=buttons)
            raise CancelHandler()
