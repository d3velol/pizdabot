import os
import json
import importlib
from pyrogram import Client, filters
from datetime import datetime, timezone
from loguru import logger
from colorama import init, Fore, Style

class Userbot:
    def __init__(self):
        init(autoreset=True)  # Инициализация colorama
        self.data_path = 'data'
        self.config_file = os.path.join(self.data_path, 'config.json')
        self.api_id, self.api_hash, self.owner_id, self.first_run = self.load_config()
        self.prefix = '.'
        self.client = Client("data/account", api_id=self.api_id, api_hash=self.api_hash)
        self.start_time = datetime.now(timezone.utc)
        self.modules_loaded = []
        self.load_modules()

        # Настройка логирования
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        logger.add(os.path.join(self.data_path, "bot.log"), rotation="1 MB")

    def load_config(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        if not os.path.exists(self.config_file):
            print("Конфигурационный файл не найден. Необходимо ввести API ID, API Hash и ваш Telegram ID (owner_id).")
            api_id = input("Введите ваш API ID: ")
            api_hash = input("Введите ваш API Hash: ")
            owner_id = input("Введите ваш Telegram ID (owner_id): ")
            config = {
                "api_id": api_id,
                "api_hash": api_hash,
                "owner_id": owner_id,
                "first_run": True
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            logger.info(f"Конфигурация сохранена в {self.config_file}.")
            return api_id, api_hash, owner_id, True
        else:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            api_id = config.get("api_id")
            api_hash = config.get("api_hash")
            owner_id = config.get("owner_id")
            first_run = config.get("first_run", False)
            if not all([api_id, api_hash, owner_id]):
                raise ValueError("Конфигурационный файл должен содержать api_id, api_hash и owner_id.")
            return api_id, api_hash, owner_id, first_run

    def save_config(self):
        config = {
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "owner_id": self.owner_id,
            "first_run": self.first_run
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info("Конфигурация обновлена и сохранена.")

    def load_modules(self):
        modules_path = 'modules'
        if not os.path.exists(modules_path):
            logger.warning(f"Папка с модулями '{modules_path}' не найдена.")
            return

        for filename in os.listdir(modules_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{modules_path}.{module_name}")
                    if hasattr(module, 'register'):
                        module.register(self.client, self)
                        self.modules_loaded.append(module_name)
                        logger.info(f"Модуль {module_name} загружен")
                except Exception as e:
                    logger.error(f"Не удалось загрузить модуль {module_name}: {e}")

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка консоли
        print(Fore.CYAN + Style.BRIGHT + r"""
  _______ _________ _______  ______   _______ 
 (  ____ )\__   __// ___   )(  __  \ (  ___  )
 | (    )|   ) (   \/   )  || (  \  )| (   ) |
 | (____)|   | |       /   )| |   ) || (___) |
 |  _____)   | |      /   / | |   | ||  ___  |
 | (         | |     /   /  | |   ) || (   ) |
 | )      ___) (___ /   (_/\| (__/  )| )   ( |
 |/       \_______/(_______/(______/ |/     \|
                                             
""")
        print(Fore.WHITE + "Бот запущен\n")
        self.client.run()

if __name__ == "__main__":
    bot = Userbot()
    bot.run()