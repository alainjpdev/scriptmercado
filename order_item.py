class OrderItem():

  def __init__(self, json):
    self.id = json['item']['id']
    self.title = json['item']['title']
    self.unit_price = json['unit_price']
    self.quantity = json['quantity']
    self.sale_fee = json['sale_fee']
  