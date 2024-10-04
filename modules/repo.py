import os
import importlib
import requests
from pyrogram import filters
from pyrogram.types import Message

MODULES_PATH = 'modules'
GITHUB_REPO = 'https://api.github.com/repos/d3velol/pizdarepo/contents/modules'

def register(client, bot):
    @client.on_message(filters.command("m", prefixes=bot.prefix) & filters.user(int(bot.owner_id)))
    async def module_handler(client, message: Message):
        args = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

        if not args:
            await list_modules(message)
            return

        command, *module_name = args.split()
        module_name = module_name[0] if module_name else None

        if command == "install" and module_name:
            await install_module(message, module_name)
        elif command == "uninstall" and module_name:
            await uninstall_module(message, module_name)
        elif command == "search" and module_name:
            await search_module(message, module_name)
        else:
            await message.edit_text("⚠️ Неверная команда. Используйте `.help` для спис��а команд.")

    @client.on_message(filters.command("help", prefixes=bot.prefix) & filters.user(int(bot.owner_id)))
    async def help_handler(client, message: Message):
        await list_commands(message)

async def list_modules(message: Message):
    modules = [f[:-3] for f in os.listdir(MODULES_PATH) if f.endswith('.py') and not f.startswith('__')]
    await message.edit_text(f"📦 Установленные модули: {', '.join(modules)}")
    
async def install_module(message: Message, module_name: str):
    try:
        response = requests.get(f"{GITHUB_REPO}/{module_name}.py")
        if response.status_code == 200:
            file_info = response.json()
            download_url = file_info.get('download_url')
            if download_url:
                file_content = requests.get(download_url).text
                with open(os.path.join(MODULES_PATH, f"{module_name}.py"), 'w') as f:
                    f.write(file_content)
                await message.edit_text(f"✅ Модуль `{module_name}` успешно установлен.")
            else:
                await message.edit_text(f"❌ Не удалось получить URL для скачивания модуля `{module_name}`.")
        else:
            await message.edit_text(f"❌ Модуль `{module_name}` не найден в репозитории.")
    except Exception as e:
        await message.edit_text(f"❌ Ошибка при установке модуля `{module_name}`: {str(e)}")

async def uninstall_module(message: Message, module_name: str):
    try:
        module_path = os.path.join(MODULES_PATH, f"{module_name}.py")
        if os.path.exists(module_path):
            os.remove(module_path)
            await message.edit_text(f"✅ Модуль `{module_name}` успешно удалён.")
        else:
            await message.edit_text(f"❌ Модуль `{module_name}` не найден.")
    except Exception as e:
        await message.edit_text(f"❌ Ошибка при удалении модуля `{module_name}`: {str(e)}")

async def search_module(message: Message, module_name: str):
    try:
        response = requests.get(GITHUB_REPO)
        if response.status_code == 200:
            modules = [item['name'][:-3] for item in response.json() if item['name'].endswith('.py')]
            if module_name in modules:
                await message.edit_text(f"🔍 Модуль `{module_name}` найден в репозитории.")
            else:
                await message.edit_text(f"🔍 Модуль `{module_name}` не найден в репозитории.")
        else:
            await message.edit_text("❌ Ошибка при поиске в репозитории.")
    except Exception as e:
        await message.edit_text(f"❌ Ошибка при поиске модуля `{module_name}`: {str(e)}")

async def list_commands(message: Message):
    commands = []
    for filename in os.listdir(MODULES_PATH):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"{MODULES_PATH}.{module_name}")
                if hasattr(module, 'COMMANDS'):
                    formatted_commands = ', '.join(f"`{cmd}`" for cmd in module.COMMANDS)
                    commands.append(f"{module.ModuleName}: {formatted_commands}")
            except Exception as e:
                continue
    await message.edit_text("🛠 Команды модулей:\n" + "\n".join(commands))

COMMANDS = ["m install {module}", "m uninstall {module}", "m search {module}", "help"]
ModuleName = "ModuleManager"
