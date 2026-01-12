from models.carrito import Carrito
from models.producto import Producto

def test_agregar_y_total():
    c = Carrito()
    p1 = Producto(1, "Camiseta", 10)
    c.agregar(p1, 2)
    assert c.total() == 20

def test_quitar():
    c = Carrito()
    p = Producto(2, "Pantalón", 30)
    c.agregar(p, 1)
    c.quitar(p.id)
    assert c.total() == 0

def test_modificar():
    c = Carrito()
    p = Producto(3, "Zapatos", 50)
    c.agregar(p, 1)
    c.modificar(p.id, 3)
    assert c.total() == 150
