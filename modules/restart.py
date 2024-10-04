import os
import sys
import asyncio
from pyrogram import filters
from pyrogram.types import Message
import time

def register(client, bot):
    @client.on_message(filters.command("restart", prefixes=bot.prefix) & filters.user(int(bot.owner_id)))
    async def restart_handler(client, message: Message):
        command = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
        start_time = time.perf_counter()

        if command == "now":
            await message.edit_text("🔄 Немедленный перезапуск бота...")
            # Немедленный перезапуск
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await message.edit_text("🔄 Перезапуск бота...")
            # Плавный перезапуск с задержкой
            await asyncio.sleep(2)
            os.execv(sys.executable, ['python'] + sys.argv)

        end_time = time.perf_counter()
        restart_time = end_time - start_time
        await message.edit_text(f"✅ Бот перезапущен за {restart_time:.2f} секунд.")

COMMANDS = ["restart", "restart now"]
ModuleName = "Restart"