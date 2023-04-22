import TG_api.core

bot = TG_api.core.bot
os = TG_api.core.os


def create_message_error():
    printed_info = f'Ошибка в боте, выключаюсь!'
    bot.send_message(os.getenv('admin_id'), printed_info)

def create_message_exeption(message):
    printed_info = f'{message}'
    bot.send_message(os.getenv('admin_id'), printed_info)


if __name__ == "__main__":
    print(f'Запущено {__name__}')
else:
    print(f'Импортируется {__name__}')
