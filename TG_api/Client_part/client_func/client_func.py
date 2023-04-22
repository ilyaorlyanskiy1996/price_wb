import TG_api
import site_api.utils.site_api_handler
import databases.utils.CRUD
from telebot import types

bot = TG_api.core.bot


def add_url(message):
    if message.text == '/in_home':
        TG_api.Common_part.common.start(message)
    else:
        try:
            url = site_api.utils.site_api_handler.take_url(message.text)
            site_api.utils.site_api_handler.search_json(url)
            data = site_api.utils.site_api_handler.take_data(url)
            original_url = message.text.split('\n')[-1]
            if databases.utils.CRUD.store_data(message.from_user.id, data[0], data[1], data[2], data[3], data[4],
                                               original_url):
                send = bot.send_message(message.chat.id, 'Товар добавлен')
                bot.register_next_step_handler(send, add_url)
            else:
                send = bot.send_message(message.chat.id, 'Товар уже есть')
                bot.register_next_step_handler(send, add_url)
        except:
            printed_info = f'Некорректный ввод'
            bot.send_message(message.chat.id, printed_info)


def delete_order(message):
    if message.text == '/in_home':
        TG_api.Common_part.common.start(message)
    else:
        try:
            databases.utils.CRUD.delete_data(int(message.text), message.from_user.id)
        except:
            printed_info = f'Некорректный ввод'
            sent = bot.send_message(message.chat.id, printed_info)
            bot.register_next_step_handler(sent, delete_order)
        else:
            printed_info = f'Товар удален'
            bot.send_message(message.chat.id, printed_info)
            printed_info = f'Оставшиеся товары:'
            send = bot.send_message(message.chat.id, printed_info)
            sent = databases.utils.CRUD.all_orders(message.from_user.id)
            if len(sent) > 0:
                for i_key, i_value in sent.items():
                    printed_info = f'{i_key}: {sent[i_key][1]}, {sent[i_key][3]} руб.'
                    bot.send_message(message.chat.id, printed_info)
                printed_info = f'Введите номер удаляемого товара'
                bot.send_message(message.chat.id, printed_info)
                bot.register_next_step_handler(send, delete_order)
            else:
                printed_info = f'Список пуст'
                bot.send_message(message.chat.id, printed_info)


def delete_all_orders(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/in_home')
    markup.add(btn1)
    if message.text == 'Да':
        if databases.utils.CRUD.delete_all_data(message.from_user.id):
            bot.send_message(message.chat.id, 'Список очищен', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Товаров в списке нет', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Товары не удалены', reply_markup=markup)
