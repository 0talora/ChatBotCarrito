from models.carrito import Carrito
from models.producto import Producto
import pytest


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


def test_agregar_mismo_producto_suma_cantidades():
  c = Carrito()
  p = Producto(4, "Gorra", 5)
  c.agregar(p, 1)
  c.agregar(p, 2)
  assert c.items[p.id]["cantidad"] == 3


def test_modificar_a_cero_elimina_producto():
  c = Carrito()
  p = Producto(5, "Calcetines", 3)
  c.agregar(p, 2)
  c.modificar(p.id, 0)
  assert p.id not in c.items


def test_quitar_producto_inexistente_no_rompe():
  c = Carrito()
  p = Producto(6, "Mochila", 40)
  c.agregar(p, 1)
  c.quitar(999)
  assert c.total() == 40


def test_total_con_varios_productos():
  c = Carrito()
  p1 = Producto(7, "Sudadera", 35)
  p2 = Producto(8, "Cinturón", 20)
  c.agregar(p1, 1)
  c.agregar(p2, 2)
  assert c.total() == 75


def test_listar_carrito_vacio():
  c = Carrito()
  texto = c.listar()
  assert "vacío" in texto.lower()


def test_listar_carrito_muestra_cantidad_y_precio():
  c = Carrito()
  p = Producto(9, "Chaqueta", 80)
  c.agregar(p, 2)
  texto = c.listar()
  assert "Chaqueta" in texto
  assert "x2" in texto
  assert "160" in texto


def test_total_carrito_vacio_es_cero():
  c = Carrito()
  assert c.total() == 0


def test_agregar_cantidad_negativa_lanza_error():
  c = Carrito()
  p = Producto(10, "Bufanda", 15)
  with pytest.raises(ValueError):
    c.agregar(p, -1)


def test_agregar_cantidad_cero_lanza_error():
  c = Carrito()
  p = Producto(11, "Guantes", 10)
  with pytest.raises(ValueError):
    c.agregar(p, 0)


def test_modificar_producto_inexistente_no_hace_nada():
  c = Carrito()
  p = Producto(12, "Sombrero", 22)
  c.agregar(p, 1)
  c.modificar(999, 3)
  assert c.total() == 22


def test_agregar_varios_productos_distintos():
  c = Carrito()
  p1 = Producto(13, "Cartera", 35)
  p2 = Producto(14, "Pijama", 25)
  c.agregar(p1, 1)
  c.agregar(p2, 1)
  assert len(c.items) == 2
  assert c.total() == 60
