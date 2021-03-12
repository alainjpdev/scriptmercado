
class Shipping():

  COMPANIES = {
    '181': 'DHL',
    '791': 'DHL',
    '521': 'FedEx',
    '511': 'FedEx'
  }

  def __init__(self, json):
    self.id = json['id']
    #TODO repasar esto!!
    self.tracking_number = "" if json.get(
        'tracking_number') is None else json['tracking_number']
    self.tracking_method = "" if json.get(
        'tracking_method') is None else json['tracking_method']
    self.service_id = "" if json.get(
        'service_id') is None else json['service_id']

    self.receiver_city = "" if json.get(
        'receiver_address') is None else json['receiver_address']['city']['name']
    
    self.receiver_state = "" if json.get(
        'receiver_address') is None else json['receiver_address']['state']['name']
        
    self.receiver_phone = "" if json.get(
        'receiver_address') is None else json['receiver_address']['receiver_phone']

    self.receiver_name = "" if json.get(
        'receiver_address') is None else json['receiver_address']['receiver_name']


    shipping_options = json.get('shipping_option')
    if shipping_options:
        
      self.list_cost = "" if shipping_options.get(
          'list_cost') is None else shipping_options.get(
          'list_cost')

      self.cost = "" if shipping_options.get(
          'cost') is None else shipping_options.get(
          'cost')

      self.logistic_type = "" if shipping_options.get(
          'logistic_type') is None else shipping_options.get(
          'logistic_type')

      self.origin = "" if shipping_options.get(
          'origin') is None else shipping_options.get(
          'origin')
    else:
      self.list_cost = self.cost = self.logistic_type = self.origin = ""

  def url(self):
    return "https://myaccount.mercadolibre.com.mx/sales/shipments/printShipmentsLabels?ids={}".format(self.id)

