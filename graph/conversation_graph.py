#grafo de conversación
#contiene todos los nodos y transiciones para el chatbot de la tienda virtual
from langgraph.graph import StateGraph, END
from models.producto import Producto
from models.carrito import Carrito
import json
from typing import TypedDict

# --- Cargar catálogo ---
# Abrimos el JSON con los productos y los convertimos a objetos Producto

with open("data/catalogo.json", "r", encoding="utf-8") as f:
  CATALOGO = [Producto(**p) for p in json.load(f)]

# --- Estado inicial ---
def estado_inicial():
  return {
    "carrito": {},       #aquí guardaremos {producto_id: {"producto": Producto, "cantidad": int}}
    "step": "inicio",
    "user_data": {}      #para datos de usuario como nombre y ciudad
  }

#función para mapear palabras clave a pasos, comprueba lo que ha escrito el usuario y devuelve el siguiente paso
def interpretar_accion(accion: str, mapa: dict):
    """
    Devuelve la clave del mapa correspondiente a la acción ingresada por el usuario.
    - accion: texto ingresado por el usuario
    - mapa: diccionario {nombre_del_paso: [palabras_clave]}
    """
    accion = accion.lower()
    for key, palabras in mapa.items():
        if any(p in accion for p in palabras):
            return key
    return None

#nodo que se ejecuta al inicio de la conversación
def nodo_inicio(state):
  print("👋 ¡Bienvenido a la tienda virtual!")
  state["step"] = "ver_catalogo"
  return state

#nodo que muestra el cataloho de productos
def nodo_ver_catalogo(state):
  print("\n📦 Catálogo de productos:")
  for p in CATALOGO:
    print(f"{p.id}. {p.nombre} - {p.precio}€")

  accion = input("Añadir / Ver carrito / Finalizar / Salir: ")

  mapa_ver_catalogo = {
    "editar_carrito": ["añadir", "agregar", "poner", "comprar"],
    "mostrar_carrito": ["carrito", "carro", "ver carrito", "mi carrito", "mostrar carrito"],
    "confirmar_compra": ["finalizar", "terminar", "comprar", "checkout"],
  "salir": ["salir", "cerrar", "adiós", "terminar sesión"]
}

  step = interpretar_accion(accion, mapa_ver_catalogo)
  if step:
    state["step"] = step
  else:
    print("❓ No te entendí")
    state["step"] = "ver_catalogo"

  return state

#nodo para añadir productos al carrito
def nodo_editar_carrito(state):
  try:
    pid = int(input("ID del producto: "))
    cantidad = int(input("Cantidad: "))

    # Buscar producto
    producto = next((p for p in CATALOGO if p.id == pid), None)
    if not producto:
      print("❌ Producto no encontrado")
      state["step"] = "ver_catalogo"
      return state

    # Comprobar stock disponible
    carrito = Carrito()
    carrito.items = state["carrito"]
    cantidad_actual_en_carrito = carrito.items.get(pid, {}).get("cantidad", 0)
    if cantidad + cantidad_actual_en_carrito > producto.stock:
      print(f"❌ No hay suficiente stock. Disponible: {producto.stock - cantidad_actual_en_carrito}")
      state["step"] = "ver_catalogo"
      return state

    # Agregar al carrito
    carrito.agregar(producto, cantidad)
    state["carrito"] = carrito.items
    print(f"✅ Añadido {cantidad}x {producto.nombre}")

  except ValueError:
    print("❌ Datos inválidos")

  # Volver al catálogo después de añadir
  state["step"] = "ver_catalogo"
  return state

#nodo para mostrar el carrito
def nodo_mostrar_carrito(state):
	carrito = Carrito()
	carrito.items = state["carrito"]
	print(carrito.listar())

	accion = input("Quitar / Modificar / Finalizar / Volver: ")

	mapa_carrito = {
		"quitar_carrito": ["quitar", "eliminar", "borrar"],
		"modificar_carrito": ["modificar", "cambiar", "actualizar"],
		"confirmar_compra": ["finalizar", "terminar", "comprar", "checkout"],
		"ver_catalogo": ["volver", "atrás", "regresar"]
	}

	step = interpretar_accion(accion, mapa_carrito)
	if step:
		state["step"] = step
	else:
		print("❓ No te entendí")
		state["step"] = "mostrar_carrito"

	return state

#nodo para quitar un producto del carro
def nodo_quitar_carrito(state):
  carrito = Carrito()
  carrito.items = state["carrito"]
  try:
    pid = int(input("ID del producto a quitar: "))
    carrito.quitar(pid)
    state["carrito"] = carrito.items
    print("🗑️ Producto eliminado")
  except ValueError:
    print("❌ ID inválido")
  state["step"] = "mostrar_carrito"
  return state

#nodo para modificar la cantidad de un producto en el carro
def nodo_modificar_carrito(state):
  carrito = Carrito()
  carrito.items = state["carrito"]
  try:
    pid = int(input("ID del producto a modificar: "))
    cantidad = int(input("Nueva cantidad: "))
    carrito.modificar(pid, cantidad)
    state["carrito"] = carrito.items
    print("🔁 Cantidad actualizada")
  except ValueError:
    print("❌ Datos inválidos")
  state["step"] = "mostrar_carrito"
  return state

#nodo para confirmar la compra
def nodo_confirmar_compra(state):
  carrito = Carrito()
  carrito.items = state["carrito"]
  print(carrito.listar())

  #preguntamos si confirma la compra
  if input("¿Confirmar compra? (s/n): ").lower() != "s":
    state["step"] = "ver_catalogo"
    return state

  #leemos el json para comprobar que el stock sigue correcto, así evitamos errores si el stock ha cambiado mientras el usuario navegaba
  with open("data/catalogo.json", "r", encoding="utf-8") as f:
    catalogo_actual = [Producto(**p) for p in json.load(f)]
	#se convierte a diccionario para acceder rápido por id
  catalogo_dict = {p.id: p for p in catalogo_actual}

  #comprobamos producto por producto que haya stock suficiente antes de continuar
  for pid, item in carrito.items.items():
    prod_json = catalogo_dict.get(pid)

    if not prod_json or item["cantidad"] > prod_json.stock:
      print(f"❌ No hay suficiente stock de {item['producto'].nombre}. Disponible: {prod_json.stock if prod_json else 0}")
      state["step"] = "ver_catalogo"
      return state # Volvemos al catálogo si no hay suficiente stock de algún producto

  #Si todo esta bien descontamos el stock de los productos comprados y guardamos el json
  for item in carrito.items.values():
    prod_json = catalogo_dict[item["producto"].id]
    prod_json.stock -= item["cantidad"]

	#guardamos el json
  with open("data/catalogo.json", "w", encoding="utf-8") as f:
    json.dump([p.to_dict() for p in catalogo_actual], f, ensure_ascii=False, indent=2)

  print("✅ Compra confirmada")
  state["step"] = "datos_envio"
  return state

#nodo para pedir los datos del envío
def nodo_datos_envio(state):
  nombre = input("Tu nombre: ")
  ciudad = input("Ciudad de envío: ")
  print(f"✅ Pedido enviado a {ciudad}, gracias {nombre}!")
  state["user_data"]["nombre"] = nombre
  state["user_data"]["ciudad"] = ciudad
  state["step"] = "salir"
  return state

#schema del estado
class StateSchema(TypedDict):
  carrito: dict
  step: str
  user_data: dict

#funcion para crear el grafo
def crear_grafo():
  graph = StateGraph(state_schema=StateSchema)

  #añadir nodos
  graph.add_node("inicio", nodo_inicio)
  graph.add_node("ver_catalogo", nodo_ver_catalogo)
  graph.add_node("editar_carrito", nodo_editar_carrito)
  graph.add_node("mostrar_carrito", nodo_mostrar_carrito)
  graph.add_node("quitar_carrito", nodo_quitar_carrito)
  graph.add_node("modificar_carrito", nodo_modificar_carrito)
  graph.add_node("confirmar_compra", nodo_confirmar_compra)
  graph.add_node("datos_envio", nodo_datos_envio)

  #punto de entrada
  graph.set_entry_point("inicio")

  #añadir transiciones basadas en "step"
  steps = [
    "inicio", "ver_catalogo", "editar_carrito", "mostrar_carrito",
    "quitar_carrito", "modificar_carrito", "confirmar_compra",
    "datos_envio"
  ]

  for n in steps:
    graph.add_conditional_edges(n,lambda s: s["step"],
    	{
        "inicio": "inicio",
        "ver_catalogo": "ver_catalogo",
        "editar_carrito": "editar_carrito",
        "mostrar_carrito": "mostrar_carrito",
        "quitar_carrito": "quitar_carrito",
        "modificar_carrito": "modificar_carrito",
        "confirmar_compra": "confirmar_compra",
        "datos_envio": "datos_envio",
        "salir": END
      }
    )

  # Compilar grafo
  return graph.compile()
