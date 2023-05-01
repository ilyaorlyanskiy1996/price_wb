import databases.utils.CRUD
import databases.common.models
import TG_api.core
import TG_api.Admin_part.Admin
import TG_api.Client_part.client
import TG_api.Common_part.common
import site_api.utils.site_api_handler
import time
from typing import Callable
import functools
from threading import Thread


def slowdown(func: Callable) -> Callable:
    """
        Декоратор, задерживающий вызов декорируемой функции на 25 сек
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        func(*args, **kwargs)
        print("Замедление на 25 секунд...")
        time.sleep(25)

    return wrapped_func


@slowdown
def check_order(order: databases.common.models.Orders):
    """
        Функция, проверяющая актуальную цену товара.
        В случае изменения цены товара выводим сообщение в телеграмм для конкретного пользователя
    """
    act_user = order.user_id
    site_api.utils.site_api_handler.search_json(order.url)
    data = site_api.utils.site_api_handler.take_data(order.url)
    print(data, order.original_url)
    if data[3] != int(order.price):
        TG_api.Client_part.client.create_message(act_user, data[0], data[1], data[2], order.price, data[3], data[4],
                                                 order.original_url)
        databases.utils.CRUD.delete_data(int(order.id), act_user)
        databases.utils.CRUD.store_data(act_user, data[0], data[1], data[2], data[3], data[4], order.original_url)


def schedule_loop():
    """
        Каждые 5 часов проходим по каждому товару в БД циклом.
    """
    try:
        while True:
            orders = [x for x in databases.common.models.Orders.select()]
            for i_order in orders:
                check_order(i_order)
            print("Замедление на 5 часов...")
            time.sleep(5*60*60)
    except Exception as exc:
        print(str(exc))
        TG_api.Admin_part.Admin.create_message_exeption(exc)
        TG_api.Admin_part.Admin.create_message_error()
        TG_api.core.bot.polling(none_stop=False)
        raise Exception


if __name__ == "__main__":
    try:
        Thread(target=schedule_loop).start()
        TG_api.core.bot.polling(none_stop=True)
    except Exception as exc:
        print(str(exc))
        TG_api.Admin_part.Admin.create_message_exeption(exc)
else:
    print(f'Импортируется {__name__}')
