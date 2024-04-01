class Person:
  def __init__(self, id, addressId):
    self.id = id
    self.addressId = addressId

  def reset(self):
    self.addressId = None
    self.id = None