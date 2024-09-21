class LockManager:
    def __init__(self):
        print("A LockManager has been created. \n")
        # Armazena os locks para cada recurso
        self.locks = {}
        # Armazena as tentativas de aquisição de locks
        self.lock_attempts = {}
        self.lock_compatibility_matrix = LockCompatibilityMatrix()

    def acquire_shared_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock compartilhado (leitura) em {resource}")
        if not self.is_lock_compatible(transaction_id, 'rlj', resource):
            self.add_lock_attempt(transaction_id, 'rlj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'rlj', resource)
        self.add_lock_attempt(transaction_id, 'rlj', resource, success=True)
        return True

    def acquire_exclusive_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock exclusivo (escrita) em {resource}")
        if not self.is_lock_compatible(transaction_id, 'wlj', resource):
            self.add_lock_attempt(transaction_id, 'wlj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'wlj', resource)
        self.add_lock_attempt(transaction_id, 'wlj', resource, success=True)
        return True

    def acquire_intent_read_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock intencional de leitura em {resource}")
        if not self.is_lock_compatible(transaction_id, 'irlj', resource):
            self.add_lock_attempt(transaction_id, 'irlj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'irlj', resource)
        self.add_lock_attempt(transaction_id, 'irlj', resource, success=True)
        return True

    def acquire_intent_write_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock intencional de escrita em {resource}")
        if not self.is_lock_compatible(transaction_id, 'iwlj', resource):
            self.add_lock_attempt(transaction_id, 'iwlj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'iwlj', resource)
        self.add_lock_attempt(transaction_id, 'iwlj', resource, success=True)
        return True

    def acquire_update_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock de update em {resource}")
        if not self.is_lock_compatible(transaction_id, 'ulj', resource):
            self.add_lock_attempt(transaction_id, 'ulj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'ulj', resource)
        self.add_lock_attempt(transaction_id, 'ulj', resource, success=True)
        return True

    def acquire_certify_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock de certificação em {resource}")
        if not self.is_lock_compatible(transaction_id, 'clj', resource):
            self.add_lock_attempt(transaction_id, 'clj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'clj', resource)
        self.add_lock_attempt(transaction_id, 'clj', resource, success=True)
        return True

    def acquire_intent_update_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock intencional de update em {resource}")
        if not self.is_lock_compatible(transaction_id, 'iulj', resource):
            self.add_lock_attempt(transaction_id, 'iulj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'iulj', resource)
        self.add_lock_attempt(transaction_id, 'iulj', resource, success=True)
        return True

    def acquire_intent_certify_lock(self, transaction_id, resource):
        print(f"{transaction_id} tentando adquirir lock intencional de Certify em {resource}")
        if not self.is_lock_compatible(transaction_id, 'iclj', resource):
            self.add_lock_attempt(transaction_id, 'iclj', resource, success=False)
            return False
        self.add_lock(transaction_id, 'iclj', resource)
        self.add_lock_attempt(transaction_id, 'iclj', resource, success=True)
        return True

    def add_lock(self, transaction_id, lock_type, resource):
        """ Adiciona o lock ao recurso """
        if resource not in self.locks:
            self.locks[resource] = []
        self.locks[resource].append({'transaction_id': transaction_id, 'type': lock_type})
        print(f"Lock {lock_type} adquirido pela transação {transaction_id} no recurso {resource}")

    def is_lock_compatible(self, transaction_id, new_lock_type, resource):
        """ Verifica se o lock que está sendo requisitado é compatível com os locks existentes """
        existing_locks = self.locks.get(resource, [])
        for lock in existing_locks:
            if not self.lock_compatibility_matrix.is_compatible(new_lock_type, lock['type']):
                print(f"Lock {new_lock_type} não é compatível com {lock['type']} no recurso {resource}")
                return False
        return True

    def add_lock_attempt(self, transaction_id, lock_type, resource, success):
        """ Registra a tentativa de aquisição de um lock, com o resultado (1 para sucesso, 2 para falha) """
        if resource not in self.lock_attempts:
            self.lock_attempts[resource] = []

        if success:
            status = 1
        else:
            status = 2

        self.lock_attempts[resource].append((transaction_id, lock_type, status))

    def plot_lock_attempts(self, resource):
        """ Exibe a lista de tentativas de bloqueios de um recurso específico """
        attempts = self.lock_attempts.get(resource, [])
        if not attempts:
            print(f"Não há tentativas de bloqueio registradas para o recurso {resource}.")
            return
        
        print(f"Tentativas de bloqueio para o recurso {resource}:")
        for attempt in attempts:
            transaction_id, lock_type, status = attempt
            status_str = 'Sucesso' if status == 1 else 'Falha'
            print(f"Transação {transaction_id} tentou {lock_type} -> {status_str}")

class LockCompatibilityMatrix:
    def __init__(self):
        self.matrix = {
            'rlj': {'rli': True, 'wli': True, 'cli': False, 'uli': False, 'irli': True, 'iwli': True, 'iuli': False, 'icli': False},
            'wlj': {'rli': True, 'wli': False, 'cli': False, 'uli': False, 'irli': True, 'iwli': False, 'iuli': False, 'icli': False},
            'clj': {'rli': False, 'wli': False, 'cli': False, 'uli': False, 'irli': False, 'iwli': False, 'iuli': False, 'icli': False},
            'ulj': {'rli': True, 'wli': False, 'cli': False, 'uli': False, 'irli': True, 'iwli': False, 'iuli': False, 'icli': False},
            'irlj': {'rli': True, 'wli': True, 'cli': False, 'uli': False, 'irli': True, 'iwli': True, 'iuli': True, 'icli': True},
            'iwlj': {'rli': True, 'wli': False, 'cli': False, 'uli': False, 'irli': True, 'iwli': True, 'iuli': True, 'icli': True},
            'iulj': {'rli': True, 'wli': False, 'cli': False, 'uli': False, 'irli': True, 'iwli': True, 'iuli': True, 'icli': True},
            'iclj': {'rli': False, 'wli': False, 'cli': False, 'uli': False, 'irli': True, 'iwli': True, 'iuli': True, 'icli': True}
        }

    def is_compatible(self, new_lock, existing_lock):
        return self.matrix[new_lock].get(existing_lock, False)