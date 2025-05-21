class AgenteBase:
    def __init__(self, llm):
        self.llm = llm

    def responder(self, mensaje):
        return self.llm.responder(mensaje)