from django.http import JsonResponse
from firebase_admin import db, credentials, initialize_app
from collections import defaultdict
import datetime
import re
import os
print(os.getcwd())

# Fetch the service account key JSON file contents
cred = credentials.Certificate('gas/serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
initialize_app(cred, {
    'databaseURL': 'https://pruebaweb-a8d37-default-rtdb.firebaseio.com'
})

def get_purchases():
    ref = db.reference('/compras')
    return ref.get()


# ---------------------------------- Promedio de Reabastecimientos por Mes por distribuidor----------------------------------


def distributor_data(request, distributor_id):
    all_purchases = get_purchases()
    purchases = []

    # Filtrar las compras por el distribuidor
    if all_purchases is not None:
        for purchase in all_purchases.values():
            if purchase is not None and purchase['distributor_id'] == str(distributor_id):
                purchases.append(purchase)

    # Calcular el número de reabastecimientos por mes por cliente
    replenishments = defaultdict(lambda: defaultdict(int))
    for purchase in purchases:
        date = datetime.datetime.strptime(purchase['date'], '%Y-%m-%d')
        user = purchase['user_id']
        replenishments[date.month][user] += 1

    # Calcular el promedio de reabastecimientos por mes
    averages = {month: sum(counts.values()) / len(counts) for month, counts in replenishments.items()}

    # Nombres de los meses en español
    month_names_spanish = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    # Convertir los números de los meses a nombres de los meses en español
    averages_with_names = {month_names_spanish[month]: average for month, average in averages.items()}

    return JsonResponse(averages_with_names)


# ---------------------------------- Porcentaje de compras por Distrito por Distribuidor ----------------------------------

def get_district_from_address(address, district_list):
    # Convertir la dirección a minúsculas para comparación insensible a mayúsculas
    address_lower = address.lower()

    # Buscar cada distrito en la lista
    for district in district_list:
        if re.search(r'\b' + re.escape(district.lower()) + r'\b', address_lower):
            return district
    return None

def consumption_data(request, distributor_id):
    all_purchases = get_purchases()
    purchases = []

    # Filtrar las compras por el distribuidor
    if all_purchases is not None:
        for purchase in all_purchases.values():
            if purchase is not None and purchase['distributor_id'] == str(distributor_id):
                purchases.append(purchase)

    # Lista de distritos conocidos
    district_list = [
        "Alto Selva Alegre", 
        "Arequipa", 
        "Cayma", 
        "Cerro Colorado", 
        "Characato",
        "Chiguata", 
        "Jacobo Hunter", 
        "José Luis Bustamante y Rivero",
        "La Joya",
        "Mariano Melgar", 
        "Miraflores",
        "Mollebaya",
        "Paucarpata",
        "Pocsi",
        "Polobaya",
        "Quequeña",
        "Sabandia",
        "Sachaca",
        "San Juan de Siguas",
        "San Juan de Tarucani",
        "Santa Isabel de Siguas",
        "Santa Rita de Siguas",
        "Socabaya",
        "Tiabaya",
        "Uchumayo",
        "Vitor",
        "Yanahuara",
        "Yarabamba",
        "Yura"
    ]

    # Calcular el consumo total por distrito
    consumption = defaultdict(int)
    for purchase in purchases:
        if 'direccion' in purchase:
            address = purchase['direccion']
            district = get_district_from_address(address, district_list)
            if district:
                consumption[district] += 1

    # Calcular el total de compras
    total_purchases = sum(consumption.values())

    # Calcular el porcentaje de compras por distrito
    consumption_percentage = {district: round((count / total_purchases) * 100, 1) for district, count in consumption.items()}

    return JsonResponse(consumption_percentage)



# ---------------------------------- Ventas por Mes por Tipo de Válvula por Distribuidor ----------------------------------
def sales_data(request, distributor_id):
    all_purchases = get_purchases()
    purchases = []

    # Filtrar las compras por el distribuidor
    if all_purchases is not None:
        for purchase in all_purchases.values():
            if purchase is not None and purchase['distributor_id'] == str(distributor_id):
                purchases.append(purchase)

    # Nombres de los meses en español
    month_names_spanish = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    # Agrupar las compras por mes y contar las ventas de cada tipo de válvula
    sales_by_month = defaultdict(lambda: defaultdict(int))
    for purchase in purchases:
        date = datetime.datetime.strptime(purchase['date'], '%Y-%m-%d')
        month = month_names_spanish[date.month]  # Nombre del mes en español
        valve_type = purchase['valvula_balon']
        sales_by_month[month][valve_type] += 1

    # Convertir el defaultdict a un dict normal para poder serializarlo a JSON
    sales_by_month = {month: dict(valve_types) for month, valve_types in sales_by_month.items()}

    return JsonResponse(sales_by_month)



# ---------------------------------- Ventas por Mes por Peso de Balón por Distribuidor ----------------------------------
def weight_data(request, distributor_id):
    all_purchases = get_purchases()
    purchases = []

    # Filtrar las compras por el distribuidor
    if all_purchases is not None:
        for purchase in all_purchases.values():
            if purchase is not None and purchase['distributor_id'] == str(distributor_id):
                purchases.append(purchase)

    # Nombres de los meses en español
    month_names_spanish = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }

    # Agrupar las compras por mes y contar las ventas de cada peso de balón
    sales_by_month_and_weight = defaultdict(lambda: defaultdict(int))
    for purchase in purchases:
        date = datetime.datetime.strptime(purchase['date'], '%Y-%m-%d')
        month = month_names_spanish[date.month]  # Nombre del mes en español
        balloon_weight = purchase['peso_balon']
        sales_by_month_and_weight[month][balloon_weight] += 1

    # Convertir el defaultdict a un dict normal para poder serializarlo a JSON
    sales_by_month_and_weight = {month: dict(weights) for month, weights in sales_by_month_and_weight.items()}

    return JsonResponse(sales_by_month_and_weight)