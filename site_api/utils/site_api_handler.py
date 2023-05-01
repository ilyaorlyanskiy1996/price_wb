import requests
import json


def take_url(in_data: str) -> str:
    """
        Функция возвращающая URL для запроса JSON файла.
    """
    id = in_data.split('/')[-2]
    url = f'https://card.wb.ru/cards/detail?&nm={id}'
    return url


def search_json(url: str):
    """
        Функция запрашивает JSON файл и записывает его в файл.
    """
    headers = {'Accept': "*/*", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    # opener = AppURLopener()
    # response = opener.open(url)

    data = response.json()
    with open('wb_catalogs_data.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        # print(f'Данные сохранены в wb_catalogs_data.json')


def take_data(url: str) -> (str, str, str, int, str):
    """
        Функция вытаскивающая из JSON файла необходимые нам данные.
        :return = брэнд, наименование, артикул, цена и URL для дальнейших запросов.
    """
    with open('wb_catalogs_data.json', 'r', encoding='UTF-8') as file:
        data_file = file.read()
        my_loads = json.loads(data_file)
        data_brand = my_loads["data"]['products'][0]["brand"]
        data_name = my_loads["data"]['products'][0]['name']
        data_id = my_loads["data"]['products'][0]['id']
        data_price = int(my_loads["data"]['products'][0]['salePriceU']) // 100
        data_url = url
        return data_brand, data_name, data_id, data_price, data_url


if __name__ == "main":
    take_url()
    search_json()
    take_data()
else:
    print(f'Импортируется {__name__}')
