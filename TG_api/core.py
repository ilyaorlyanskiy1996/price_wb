import telebot
import os
from dotenv import load_dotenv

load_dotenv()
token_telebot = os.getenv('token_telebot')
bot = telebot.TeleBot(token_telebot)
my_reg_exp = str()

if __name__ == "__main__":
    print(f'Запущено {__name__}')
else:
    print(f'Импортируется {__name__}')
