# aquí definimos la clase Chatbot que controla todo el flujo de la tienda virtual usando el grafo de conversación.
from graph.conversation_graph import crear_grafo, estado_inicial

class Chatbot:
  def __init__(self):
    self.graph = crear_grafo()
    self.state = estado_inicial()

  def run(self):
    print("=== Chatbot Tienda Virtual ===")
    self.graph.invoke(self.state)