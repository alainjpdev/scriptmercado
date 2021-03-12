from dateutil import parser

from order_item import OrderItem
from shipping import Shipping

class Order():

  def __init__(self, _json):
    self.id = _json['id']
    
    #TODO: CHECK this
    # self.date_created = DateTime.parse(json[:date_created])
    # self.date_closed = DateTime.parse(json[:date_closed])
    self.date_created = parser.parse(_json['date_created'])
    self.date_closed =parser.parse(_json['date_closed'])

    buyer = _json['buyer']
    self.buyer_name = "{} {}".format(buyer['first_name'], buyer['last_name'])

    self.shipping_cost = 0
    if _json.get('payments', None):
      for payment in _json['payments']:
        self.shipping_cost += payment['shipping_cost']

    self.order_items = []
    
    for order_item_json in _json['order_items']:
        self.order_items.append(OrderItem(order_item_json))

    self.shipping_id = _json.get('shipping').get('id', "")
    if self.shipping_id is not None:
      self.shipping_url = "https://myaccount.mercadolibre.com.mx/sales/shipments/printShipmentsLabels?ids={}".format(self.shipping_id)
      
    else:
      self.shipping_url = ""

  def week(self):
    return 1 if self.date_closed.day <= 15 else 2

  def __getattr__(self, item):
    return None
