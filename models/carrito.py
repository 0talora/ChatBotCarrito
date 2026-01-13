class Carrito:
  def __init__(self):
    self.items = {}

  def agregar(self, producto, cantidad):
    if cantidad <= 0:
      raise ValueError("Cantidad inválida")
    if producto.id in self.items:
      self.items[producto.id]["cantidad"] += cantidad
    else:
      self.items[producto.id] = {"producto": producto, "cantidad": cantidad}

  def quitar(self, producto_id):
        self.items.pop(producto_id, None)

  def modificar(self, producto_id, cantidad):
    if producto_id in self.items:
      if cantidad <= 0:
        self.quitar(producto_id)
      else:
        self.items[producto_id]["cantidad"] = cantidad

  def total(self):
    return sum(
      item["producto"].precio * item["cantidad"]
        for item in self.items.values()
      )

  def listar(self):
    if not self.items:
      return "🛒 Tu carrito está vacío."
    texto = "🛒 Carrito actual:\n"
    for item in self.items.values():
      p = item["producto"]
      c = item["cantidad"]
      texto += f"- {p.nombre} x{c} → {p.precio * c:.2f}€\n"
    texto += f"\nTotal: {self.total():.2f}€"
    return texto
