#esta clase se usa para representar productos
class Producto:
  def __init__(self, id, nombre, precio, stock=0, categoria=None, descripcion=None):
    self.id = id
    self.nombre = nombre
    self.precio = precio
    self.stock = stock
    self.categoria = categoria
    self.descripcion = descripcion

  def __repr__(self):
    return f"{self.nombre} ({self.precio:.2f}€)"

  def to_dict(self):
    #convierte el producto a un diccionario para guardarlo en el json
    return {
      "id": self.id,
      "nombre": self.nombre,
      "precio": self.precio,
      "stock": self.stock,
      "categoria": self.categoria,
      "descripcion": self.descripcion
    }
