# Manipulação de locks, criação de locks de múltipla granularidade

class LockManager:
    def __init__(self):
        print("A LockManager has been created. \n")
        # Armazena os locks para cada recurso
        self.locks = {}

    def acquire_shared_lock(self, transaction_id, resource):
        # Implementar lógica para lock compartilhado (leitura)
        print(f"{transaction_id} tentando adquirir lock compartilhado em {resource}")
        # Verifica e adquire o lock compartilhado
        # Retorna True se conseguiu, False se tiver que esperar
        return True

    def acquire_exclusive_lock(self, transaction_id, resource):
        # Implementar lógica para lock exclusivo (escrita)
        print(f"{transaction_id} tentando adquirir lock exclusivo em {resource}")
        # Verifica e adquire o lock exclusivo
        # Retorna True se conseguiu, False se tiver que esperar
        return True
