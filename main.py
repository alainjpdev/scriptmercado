# encoding: UTF-8

'''
Crear una app: http://applications.mercadolibre.com/
Copiar el app id y secret key
Crear usuarios de test: https://www.mercadopago.com.ar/developers/en/solutions/payments/basic-checkout/test/test-users/
Identificarse con el usuario y contraseña de test: https://www.mercadolibre.com
Copiar el client id y el access token
Dar acceso a la app al usuario: https://developers.mercadolibre.com/authentication-and-authorization/
'''

APP_ID = 7629182635292394
APP_SECRET = 'zGtGw7UsQkK8boIcU9eBqv4CBZb9zKwL'
CLIENT_ID = 549818682
CSV_FILE = 'DEMO-matriz-MONTH-YEAR.csv'
LAST_DATE_CLOSED_FILE = 'last_date_closed.txt'
CLIENT_ACCESS_TOKEN_FILE = 'access_token_ARMANDO.txt'
REFRESH_TOKEN_FILE = 'refresh_token.txt'
CLIENT_CODE_FILE = 'client_code.txt'

REDIRECT_URI = 'https://localhost'

TIME_DELTA_TEST = 60 # TIEMPO EN SEGUNDOS CADA CUANTO SE CORRERA EL SCRIPT AUTOMATICAMENTE

import datetime
import os
import sys
import copy
import csv
import time

from timeloop import Timeloop
from datetime import timedelta

from dateutil import parser

from meli_rest import MeliRest
from order import Order
from shipping import Shipping

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

tl = Timeloop()


def generate_csv_line(order):
  # order_item = order.order_items[0]
  csv_lines=[]
  for order_item in order.order_items:
    csv_line = [
      #FORMA DE PAGO
      "MP",
      #ID TIENDA
      "TOO",
      #ID QUIEN PUBLICA
      "TOO",
      #FECHA DE COMPRA
      "",
      order.date_closed.date(),
      #FECHA ENVIO
      "",
      #QUINCENA
      order.week(),
      ##MES
      order.date_closed.month,
      #CLIENTE
      "{} (Recibe: {})".format(order.buyer_name, 
        order.shipping.receiver_name if order.shipping else "No definido"),
      #TELEFONO (Receiver phone)
      order.shipping.receiver_phone if order.shipping else "",
      #EMAIL
      "",
      #LINK 
      "",
      #TRACK
      order.shipping.tracking_number if order.shipping else "",
      #PAQUETERIA(tracking method)
      order.shipping.tracking_method if order.shipping else "",
      #GUIA
      "ME",
      #ITEM
      order_item.title,
      #OBSERVACIONES
      "",
      #LINK 
      "",
      #LINK 
      "",
      #LINK MERCADO LIBRE
      "",
      #CANTIDAD "U"
      order_item.quantity,
      #COSTO UNITARIO USD "V"
      "",
      #COSTO DOLAR 
      "",
      #COSTO 
      "",
      #"Y"
      "",
      #PRIME ONE 
      "",
      #PRIME 
      "",
      #COSTO ENVIO NACIONAL "AB"
      "${}".format(order.shipping_cost),
      #COMISION AG ADUANAL "AC"
      "",
      #COSTO TOTAL DEL ITEM "AD"
      "",
      #PRECIO VENTA SUGERIDO "AE"
      "",
      #PRECIO VENTA CLIENTE AF
      "${}".format(order_item.unit_price * order_item.quantity),
      #ENVIO PAGADO CLIENTE "AG"
      "${}".format(order.shipping.cost if order.shipping else ""),
      #TOTAL COBRADO "AH"
      "",
      #COMISION ML "AI"
      "${}".format(order_item.sale_fee * order_item.quantity),
      #UTILIDAD "AJ"
      "",
      #PORCENTAJE 
      "",
      #PORCENTAJE DE 
      order.shipping_url,
      order_item.id,
      order.id,
      #ENVIO PAGADO TIENDA,
      "${}".format(order.shipping.list_cost if order.shipping else ""),
      #Logistica
      order.shipping.logistic_type if order.shipping else "",
      #ORIGIN
      order.shipping.origin if order.shipping else "",
      #CIUDAD
      order.shipping.receiver_city if order.shipping else "",
      #STATE
      order.shipping.receiver_state if order.shipping else "",
      #SERVICE_ID
      order.shipping.service_id if order.shipping else ""
    ]
    csv_lines.append(csv_line)

  return csv_lines


@tl.job(interval=timedelta(seconds=TIME_DELTA_TEST))
def get_orders():
  client_access_token = ''
  with open(os.path.join(__location__, CLIENT_ACCESS_TOKEN_FILE), 'r') as file:
    client_access_token = file.read()


  try:
      with open(os.path.join(__location__, REFRESH_TOKEN_FILE), 'r') as file:
          refresh_access_token = file.read()
  except FileNotFoundError:
    refresh_access_token = None


  try:
      with open(os.path.join(__location__, CLIENT_CODE_FILE), 'r') as file:
          client_code = file.read()
  except FileNotFoundError:
    client_code = None



  meli_rest = MeliRest(APP_ID, APP_SECRET, CLIENT_ID, client_access_token,
                      client_code, refresh_access_token, REDIRECT_URI)

  if meli_rest.get_refresh_token():
    with open(os.path.join(__location__, CLIENT_ACCESS_TOKEN_FILE), 'w') as file:
      file.write(meli_rest.client_access_token)
    with open(os.path.join(__location__, REFRESH_TOKEN_FILE), 'w') as file:
      file.write(meli_rest.refresh_token)
  else:
    print("*** TOKEN inválido. Intentando generar nuevo token con los datos guardados")
    if meli_rest.get_token():
      print("*** Nuevo Token generado... Guardando***")
      with open(os.path.join(__location__, CLIENT_ACCESS_TOKEN_FILE),'w') as file:
        file.write(meli_rest.client_access_token)
      with open(os.path.join(__location__, REFRESH_TOKEN_FILE), 'w') as file:
        file.write(meli_rest.refresh_token)
    else:
      print("*** TOKEN inválido. No se pudo generar un nuevo token, deberá generar un nuevo CLIENT_CODE (https://developers.mercadolibre.com.mx/es_ar/autenticacion-y-autorizacion/#Autenticaci%C3%B3n)")
      sys.exit()


  print("*** Leyendo fecha de última orden ***")
  try:
      with open(os.path.join(__location__, LAST_DATE_CLOSED_FILE), 'r') as date_file:
          last_date_closed = parser.parse(date_file.read())
  except (FileNotFoundError, parser.ParserError):
      last_date_closed = datetime.datetime(
          1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
      date_file = open(os.path.join(__location__, LAST_DATE_CLOSED_FILE), 'w')

  print("  - Fecha de última orden: {}".format(last_date_closed))

  csv_orders = []
  page = 1
  orders_exists = True

  while orders_exists:
      
      all_orders = meli_rest.orders(str(last_date_closed), page)
      if len(all_orders) == 0:
          break
      print("*** Trayendo ordenes de la pagina {} ***".format(page))
      filtered_orders = [order for order in all_orders if parser.parse(order['date_closed']) > last_date_closed]
      for order_json in filtered_orders:
          order_attributes = meli_rest.order(order_json['id'])
          print("* Analizando orden {}".format(order_json['id']))

          print("  - Trayendo información")
          order = Order(order_attributes)

          if order.shipping_id is not None:
            print("  - Obteniendo información del shipping {}".format(order.shipping_id))
            shipping = Shipping(meli_rest.shipping(order.shipping_id))
            order.shipping = shipping
          else:
            print("  - Esta orden no tiene shipping asociado")

          print("  - Agregando al array de ordenes")    
          
          csv_orders.append(order)
      
      page +=1

  print("*** Guardando archivos CSV ***")

  csv_orders.sort(key=lambda x: x.date_closed)
  for order in csv_orders:
    filename = copy.deepcopy(CSV_FILE)
    filename = filename.replace("MONTH", str(order.date_closed.month))
    filename = filename.replace("YEAR", str(order.date_closed.year))

    with open(filename, 'a', encoding="utf-8", newline='') as csv_file:
      print("  - Agregando a {} la orden {}".format(filename, order.id))
      writer = csv.writer(csv_file, delimiter=',')
      for line in generate_csv_line(order):
        writer.writerow(line)

  if len(csv_orders) > 0:
    last_date_closed = csv_orders[-1].date_closed

    print( "*** Guardando fecha de última orden {} ***".format(last_date_closed))
    with open(os.path.join(__location__, LAST_DATE_CLOSED_FILE), 'w') as date_file:
      date_file.write(str(last_date_closed))
  else:
    print("*** No hay ordenes nuevas ***")

#EJECUTA  LA PRIMERA VEZ Y LUEGO CORRE LOOP
get_orders()
tl.start(block=True)
