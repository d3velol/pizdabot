import time
from datetime import datetime, timezone
from pyrogram import filters
from pyrogram.types import Message

BOT_NAME = "piZdaBot"

def register(client, bot):
    @client.on_message(filters.command("info", prefixes=bot.prefix) & filters.user(int(bot.owner_id)))
    async def info_handler(client, message: Message):
        try:
            # Измерение пинга вручную
            start_time = time.perf_counter()
            await client.get_me()
            end_time = time.perf_counter()
            ping_ms = (end_time - start_time) * 1000  # Пинг в миллисекундах

            # Расчет аптайма
            current_time = datetime.now(timezone.utc)
            uptime_delta = current_time - bot.start_time
            uptime = str(uptime_delta).split('.')[0]  # Убираем микросекунды

            # Составление сообщения с информацией о боте
            info_message = (
                f"🤖 {BOT_NAME} \n"
                f"⏱ Аптайм: {uptime}\n"
                f"📦 Количество модулей: {len(bot.modules_loaded)}\n"
                f"📡 Пинг: {ping_ms:.2f} ms\n"
            )

            # Редактирование сообщения с командой
            await message.edit_text(info_message)

        except Exception as e:
            error_message = f"❌ Произошла ошибка: {e}"
            await message.edit_text(error_message)

COMMANDS = ["info"]
ModuleName = "Info"