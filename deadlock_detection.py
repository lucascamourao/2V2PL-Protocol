# Funções para detecção de deadlocks (grafo de espera) 

class DeadlockDetection:
    def __init__(self, schedule):
        self.wait_grafo = {} #'T1': ['T2', 'T3', 'T4'] == T1->T2, T1->T3, T1->T4
        self.past = []

        for transaction in schedule:
            self.wait_grafo[transaction[0]] = []

    def add_wait(self, espera, esperado):
        aux = self.wait_grafo[espera]
        if esperado not in aux:
            aux.append(esperado)
        self.wait_grafo[espera] = aux

    def detect_deadlock(self, no, prox, past):
        print("Detecting deadlock...")
        if no in past:
            self.past = past
            return True
        past.append(no)
        for i in prox:
            if self.detect_deadlock(i, self.wait_grafo[i], past):
                return True
        return False
    
# Se existir, retornar a transação a ser abortada
