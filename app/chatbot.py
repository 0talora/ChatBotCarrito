from graph.conversation_graph import crear_grafo, State

class Chatbot:
    def __init__(self):
        self.state = State()
        self.graph = crear_grafo()

    def run(self):
        print("=== Chatbot Tienda Virtual ===")
        self.graph.run(self.state)
