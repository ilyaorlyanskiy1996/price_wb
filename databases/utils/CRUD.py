from databases.common.models import *


def store_data(user_id: str, order_brand: str, order_name: str, order_id: str, price: str, url: str,
               original_url: str) -> bool:
    """
        Функция для сохранения выбранного товара. Если в базе такого товара нет (у определенного пользователя), то добавляем в БД и возвращвем True.
        Если пользователем товар уже был добавлен, то выводим False.
    """
    set_order = set(x for x in Orders.select().where(Orders.order_id == order_id))
    set_user = set(x for x in Orders.select().where(Orders.user_id == user_id))
    if not (set_order & set_user):
        Orders.create(
            user_id=user_id,
            order_name=order_name,
            order_id=order_id,
            price=price,
            order_brand=order_brand,
            url=url,
            original_url=original_url
        ).save()
        return True
    else:
        return False


def delete_data(id_order: int, this_user_id: str):
    """
        Функция для удаления товара из БД
    """
    deleted_position = Orders.get(id=id_order)
    if deleted_position.user_id == str(this_user_id):
        deleted_position.delete_instance()
    else:
        raise Exception


def delete_all_data(this_user_id: str) -> bool:
    """
        Функция для удаления всех товаров из БД, добавленные конкретным пользователем.
        Если у пользователя были товары в БД, то функция возвращает True, если не было, то False.
    """
    users_orders = [x for x in Orders.select().where(Orders.user_id == this_user_id)]
    if len(users_orders) > 0:
        for i_order in users_orders:
            i_order.delete_instance()
        return True
    else:
        return False


def all_orders(this_user_id: str) -> dict:
    """
        Функция возвращающая все товары, добавленные ранее пользователем в БД.
    """
    orders = [x for x in Orders.select().where(Orders.user_id == this_user_id)]
    data = dict()
    for i_order in orders:
        buffer = Orders.get(id=i_order)
        data[buffer.id] = (buffer.order_brand, buffer.order_name, buffer.order_id, buffer.price, buffer.original_url)
    return data


if __name__ == "__main__":
    store_data()
    delete_data()
    delete_all_data()
    all_orders()
else:
    print(f'Импортируется {__name__}')
