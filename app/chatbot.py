from graph.conversation_graph import crear_grafo, estado_inicial

class Chatbot:
    def __init__(self):
        self.graph = crear_grafo()
        self.state = estado_inicial()

    def run(self):
        print("=== Chatbot Tienda Virtual ===")
        self.graph.invoke(self.state)
