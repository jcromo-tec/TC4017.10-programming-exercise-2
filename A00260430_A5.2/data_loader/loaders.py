'''
Modulo para leer archivos con las lista de precios por artículo. Las listas
están en formato JSON.

La lista de precios por articulo tiene el formato:
[{
  "title": "Brown eggs",
  "type": "dairy",
  "description": "Raw organic brown eggs in a basket",
  "filename": "0.jpg",
  "height": 600,
  "width": 400,
  "price": 28.1,
  "rating": 4
  }, {
  "title": "Sweet fresh stawberry",
  "type": "fruit",
  "description": "Sweet fresh stawberry on the wooden table",
  "filename": "1.jpg",
  "height": 450,
  "width": 299,
  "price": 29.45,
  "rating": 4
  },... {
    ...
  }]

La lista de ventas tiene el formato:
[
  {
    "SALE_ID": 1,
    "SALE_Date": "01/12/23",
    "Product": "Rustic breakfast",
    "Quantity": 1
  },
  {
    "SALE_ID": 1,
    "SALE_Date": "01/12/23",
    "Product": "Sandwich with salad",
    "Quantity": 2
  },...
  {
    ...
  }
]
'''
import json

OK_STATUS = 0
ERROR_STATUS = 9
EMPTY_LIST_STATUS = 1


def _parse_price_list(interim_price_list):
    '''
    Función para preparar un diccionario simple con las listas de precios.
    Solo se usarán los atributos de title como la llave y precio como valor
    si pasan la siguientes validaciones:
     - title no debe ser un valor nulo o un string vacío
     - price debe de ser un número entero o de punto flotante mayor a cero
    '''
    simple_price_list = {}
    for price_item in interim_price_list:
        product = None
        price = 0.
        if (
            'title' in price_item and
            price_item['title'] is not None and
            len(price_item['title']) > 0
        ):
            product = price_item['title']
            if (
                'price' in price_item and
                isinstance(price_item['price'], (int, float))
            ):
                price = price_item['price']
            if product is not None and price > 0:
                simple_price_list[product] = price

    return simple_price_list


def load_price_list(file_name):
    '''
    Función para leer listas de precios por artículo en formato JSON.

    La función genera un diccionario simple con todos los productos y sus
    precios.
    '''
    status = OK_STATUS
    parsed_price_list = None

    try:
        with open(file_name, 'r', encoding='UTF-8') as fd:
            staging_price_list = json.load(fd)
            parsed_price_list = _parse_price_list(staging_price_list)
    except OSError as error:
        print(
            '[ERROR] - An exception ocurred',
            f'while processing price list file: {error}'
        )
        status = ERROR_STATUS

    if parsed_price_list is None or len(parsed_price_list) == 0:
        status = EMPTY_LIST_STATUS

    return status, parsed_price_list


def load_sales_list(file_name):
    '''
    Función para leer archivo con listas de ventas en formato JSON.
    '''
    status = OK_STATUS
    parsed_sales_list = None

    try:
        with open(file_name, 'r', encoding='UTF-8') as fd:
            parsed_sales_list = json.load(fd)
    except OSError as error:
        print(
            '[ERROR] - An exception ocurred',
            f'while processing sales list file: {error}'
        )
        status = ERROR_STATUS

    if parsed_sales_list is None or len(parsed_sales_list) < 1:
        status = EMPTY_LIST_STATUS

    return status, parsed_sales_list
