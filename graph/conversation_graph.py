from langgraph.graph import StateGraph, END
from models.producto import Producto
from models.carrito import Carrito
import json

# --- Cargar catálogo ---
with open("data/catalogo.json", "r") as f:
    CATALOGO = [Producto(**p) for p in json.load(f)]

# --- Estado global ---
class State:
    def __init__(self):
        self.carrito = Carrito()
        self.usuario = None
        self.estado = "inicio"

# --- Nodos ---
def nodo_inicio(state):
    print("👋 ¡Bienvenido a la tienda virtual!")
    return "ver_catalogo"

def nodo_ver_catalogo(state):
    print("\n📦 Catálogo de productos:")
    for p in CATALOGO:
        print(f"{p.id}. {p.nombre} - {p.precio}€")
    accion = input("Añadir / Ver carrito / Finalizar / Salir: ").lower()
    if "añadir" in accion: return "editar_carrito"
    elif "carrito" in accion: return "mostrar_carrito"
    elif "finalizar" in accion: return "confirmar_compra"
    elif "salir" in accion: return END
    return "ver_catalogo"

def nodo_editar_carrito(state):
    try:
        pid = int(input("ID del producto: "))
        cantidad = int(input("Cantidad: "))
        producto = next((p for p in CATALOGO if p.id == pid), None)
        if producto:
            state.carrito.agregar(producto, cantidad)
            print(f"✅ Añadido {cantidad}x {producto.nombre}")
        else:
            print("❌ Producto no encontrado")
    except ValueError:
        print("❌ Datos inválidos")
    return "ver_catalogo"

def nodo_mostrar_carrito(state):
    print(state.carrito.listar())
    accion = input("Quitar / Modificar / Finalizar / Salir: ").lower()
    if "quitar" in accion: return "quitar_carrito"
    elif "modificar" in accion: return "modificar_carrito"
    elif "finalizar" in accion: return "confirmar_compra"
    elif "salir" in accion: return END
    return "ver_catalogo"

def nodo_quitar_carrito(state):
    try:
        pid = int(input("ID del producto a quitar: "))
        state.carrito.quitar(pid)
        print("🗑️ Producto eliminado")
    except ValueError:
        print("❌ ID inválido")
    return "mostrar_carrito"

def nodo_modificar_carrito(state):
    try:
        pid = int(input("ID del producto a modificar: "))
        cantidad = int(input("Nueva cantidad: "))
        state.carrito.modificar(pid, cantidad)
        print("🔁 Cantidad actualizada")
    except ValueError:
        print("❌ Datos inválidos")
    return "mostrar_carrito"

def nodo_confirmar_compra(state):
    print(state.carrito.listar())
    if input("Confirmar compra? (s/n): ").lower() == "s":
        return "datos_envio"
    return "ver_catalogo"

def nodo_datos_envio(state):
    nombre = input("Tu nombre: ")
    ciudad = input("Ciudad de envío: ")
    print(f"✅ Pedido enviado a {ciudad}, gracias {nombre}!")
    return END

# --- Crear grafo ---
def crear_grafo():
    state_schema = {
        "carrito": dict,
        "usuario": (str, type(None)),
        "estado": str
    }

    graph = StateGraph(state_schema=state_schema)

    graph.add_node("inicio", nodo_inicio)
    graph.add_node("ver_catalogo", nodo_ver_catalogo)
    graph.add_node("editar_carrito", nodo_editar_carrito)
    graph.add_node("mostrar_carrito", nodo_mostrar_carrito)
    graph.add_node("quitar_carrito", nodo_quitar_carrito)
    graph.add_node("modificar_carrito", nodo_modificar_carrito)
    graph.add_node("confirmar_compra", nodo_confirmar_compra)
    graph.add_node("datos_envio", nodo_datos_envio)
    graph.set_entry_point("inicio")
    
    return graph

