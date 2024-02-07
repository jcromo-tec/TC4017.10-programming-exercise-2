'''
Programa para calcular la ventas totales en base a una lista de ventas y una
lista de precios.

La lista de precios y la lista de ventas son leidas de sus archivos en format
JSON correspondientes.
'''
import sys
import time
from data_loader import load_price_list, load_sales_list

# Constantes
OK_STATUS = 0
ERROR_STATUS = 9


def get_elapsed_time(started):
    '''
    Funcion para calcular el tiempo de ejecución del programa
    '''
    finished = time.time()
    return f'ELAPSED TIME: {(finished - started):.6f} seconds.\n'


def initialize():
    '''
    Funcion para inicializar variables.
    '''
    return time.time(), 0.


# Logica principal
start_time, total_sales = initialize()

if len(sys.argv) < 3:
    print(
        'Usage:\n',
        'python compute_sales.py <price listfile name> <price listfile name>\n'
    )
    sys.exit(OK_STATUS)
else:
    price_list_file_name = sys.argv[1]
    sales_list_file_name = sys.argv[2]

status_price_list, price_list = load_price_list(price_list_file_name)

status_sales_list, sales_list = load_sales_list(sales_list_file_name)


if status_price_list == 0 and status_sales_list == 0:
    # Calcular el precio total por cada elemento de la lista de ventas
    # sale value = product price * quantity
    for sales_list_item in sales_list:
        # Verificar que elemento de la lista contenga los campos Product y
        #  Quantity
        # Verificar que quantity sea un valor numérico entero o de punto
        # flotante
        if (
            'Product' in sales_list_item and
            'Quantity' in sales_list_item and
            isinstance(sales_list_item['Quantity'], (float, int))
        ):
            # Verificar que el producto vendido exista en la lista de precios.
            # El nombre del producto es la llave del diccionario de la lista
            # de precios
            if sales_list_item['Product'] in price_list:
                total_sales += \
                    price_list[sales_list_item['Product']] \
                    * sales_list_item['Quantity']
            else:
                print(
                    f'Product {sales_list_item["Product"]}',
                    'is not in the price list.\n'
                )

    # Preparando líneas del encabezado y de las ventas totales
    lines = [
        f'PRICE_LIST:  {price_list_file_name}\n',
        f'SALES_LIST:  {sales_list_file_name}\n',
        f'TOTAL SALES: {total_sales:.2f}\n',
    ]

    try:
        # Escribiendo las líneas del encabezado y de las ventas totales a un
        # archivo
        with open('SalesResults.txt', '+wt', encoding='UTF-8') as fd:
            fd.writelines(lines)
        # Desplegando las líneas del encabezado y de las ventas totales en la
        # consola
        for line in lines:
            print(line, end='')
    except OSError as error:
        print(
            '[ERROR] - An exception ocurred while',
            f'processing results file: {error}'
        )
        elapsed_time = get_elapsed_time(start_time)
        print(elapsed_time)
        sys.exit(ERROR_STATUS)

elapsed_time = get_elapsed_time(start_time)

try:
    with open('SalesResults.txt', '+at', encoding='UTF-8') as fd:
        fd.writelines(elapsed_time)
    print(elapsed_time)
except OSError as error:
    print(
        '[ERROR] - An exception ocurred',
        f'while processing results file: {error}'
    )
    print(elapsed_time)
    sys.exit(ERROR_STATUS)

sys.exit(int(status_price_list + status_sales_list))
