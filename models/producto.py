class Producto:
  def __init__(self, id, nombre, precio, categoria=None, descripcion=None):
    self.id = id
    self.nombre = nombre
    self.precio = precio
    self.categoria = categoria
    self.descripcion = descripcion

  def __repr__(self):
    return f"{self.nombre} ({self.precio:.2f}€)"
