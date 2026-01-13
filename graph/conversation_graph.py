from langgraph.graph import StateGraph, END
from models.producto import Producto
from models.carrito import Carrito
import json
from typing import TypedDict

# --- Cargar catálogo ---
with open("data/catalogo.json", "r", encoding="utf-8") as f:
  CATALOGO = [Producto(**p) for p in json.load(f)]

# --- Estado inicial ---
def estado_inicial():
  return {
    "carrito": {},       # Aquí guardaremos {producto_id: {"producto": Producto, "cantidad": int}}
    "step": "inicio",
    "user_data": {}      # Para datos de usuario como nombre y ciudad
  }

# --- Función para mapear palabras clave a pasos ---
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

# --- Nodos ---
def nodo_inicio(state):
  print("👋 ¡Bienvenido a la tienda virtual!")
  state["step"] = "ver_catalogo"
  return state

def nodo_ver_catalogo(state):
  print("\n📦 Catálogo de productos:")
  for p in CATALOGO:
    print(f"{p.id}. {p.nombre} - {p.precio}€")

  accion = input("Añadir / Ver carrito / Finalizar / Salir: ")

  mapa_ver_catalogo = {
    "editar_carrito": ["añadir", "agregar", "poner", "comprar"],
    "mostrar_carrito": ["carrito", "ver carrito", "mi carrito", "mostrar carrito"],
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

def nodo_editar_carrito(state):
  try:
    pid = int(input("ID del producto: "))
    cantidad = int(input("Cantidad: "))
    producto = next((p for p in CATALOGO if p.id == pid), None)
    if producto and cantidad > 0:
      carrito = Carrito()
      carrito.items = state["carrito"]
      carrito.agregar(producto, cantidad)
      state["carrito"] = carrito.items
      print(f"✅ Añadido {cantidad}x {producto.nombre}")
    else:
      print("❌ Producto o cantidad inválidos")
  except ValueError:
    print("❌ Datos inválidos")
  state["step"] = "ver_catalogo"
  return state

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

def nodo_confirmar_compra(state):
  carrito = Carrito()
  carrito.items = state["carrito"]
  print(carrito.listar())
  if input("¿Confirmar compra? (s/n): ").lower() == "s":
    state["step"] = "datos_envio"
  else:
    state["step"] = "ver_catalogo"
  return state

def nodo_datos_envio(state):
  nombre = input("Tu nombre: ")
  ciudad = input("Ciudad de envío: ")
  print(f"✅ Pedido enviado a {ciudad}, gracias {nombre}!")
  state["user_data"]["nombre"] = nombre
  state["user_data"]["ciudad"] = ciudad
  state["step"] = "salir"
  return state

# --- Definir schema del estado ---
class StateSchema(TypedDict):
  carrito: dict
  step: str
  user_data: dict

# --- Crear grafo ---
def crear_grafo():
  graph = StateGraph(state_schema=StateSchema)

  # Añadir nodos
  graph.add_node("inicio", nodo_inicio)
  graph.add_node("ver_catalogo", nodo_ver_catalogo)
  graph.add_node("editar_carrito", nodo_editar_carrito)
  graph.add_node("mostrar_carrito", nodo_mostrar_carrito)
  graph.add_node("quitar_carrito", nodo_quitar_carrito)
  graph.add_node("modificar_carrito", nodo_modificar_carrito)
  graph.add_node("confirmar_compra", nodo_confirmar_compra)
  graph.add_node("datos_envio", nodo_datos_envio)

  # Punto de entrada
  graph.set_entry_point("inicio")

  # Añadir transiciones basadas en "step"
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
