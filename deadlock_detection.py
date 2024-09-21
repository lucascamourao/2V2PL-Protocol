# Funções para detecção de deadlocks (grafo de espera) 

class DeadlockDetection:
    def __init__(self):
        self.wait_grafo = {} #'T1': ['T2', 'T3', 'T4'] == T1->T2, T1->T3, T1->T4
        self.past = []

    def add_wait(self, espera, esperado):
        print("")

    def detect_deadlock(self, no, prox):
        # Implementar a lógica de construção do grafo de espera
        # e detecção de ciclos para identificar deadlocks
        print("Detecting deadlock...")
    
        # Verificar se existe ciclo no grafo de espera
        # Se existir, retornar a transação a ser abortada
        return None
