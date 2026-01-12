class Carrito:
    def __init__(self):
        self.items = {}

    def agregar(self, producto, cantidad):
        if producto.id in self.items:
            self.items[producto.id]["cantidad"] += cantidad
        else:
            self.items[producto.id] = {"producto": producto, "cantidad": cantidad}

    def quitar(self, producto_id):
        if producto_id in self.items:
            del self.items[producto_id]

    def modificar(self, producto_id, cantidad):
        if producto_id in self.items:
            self.items[producto_id]["cantidad"] = cantidad

    def vaciar(self):
        self.items = {}

    def total(self):
        return sum(i["producto"].precio * i["cantidad"] for i in self.items.values())

    def listar(self):
        if not self.items:
            return "Tu carrito está vacío."
        texto = "🛒 Carrito actual:\n"
        for item in self.items.values():
            p = item["producto"]
            c = item["cantidad"]
            texto += f"- {p.nombre} x{c} → {p.precio * c:.2f}€\n"
        texto += f"\nTotal: {self.total():.2f}€"
        return texto
