class LockManager:
    def __init__(self):
        print("A LockManager has been created. \n")
        # Armazena os locks para cada recurso
        self.locks = {}
        # Armazena as tentativas de aquisição de locks
        self.lock_attempts = {}
        self.locks_approved = []
        self.transactions_waiting = []
        # Pega a matriz com as comparações
        self.lock_compatibility_matrix = LockCompatibilityMatrix()
        #sempre que um objeto especifico

    def acquire_shared_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
        if not self.is_lock_compatible(transaction_id, 'R', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'R', resource, success=False)
            return False
        self.add_lock(transaction_id, 'R', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'R', resource, success=True)
        return True

    def acquire_exclusive_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
        if not self.is_lock_compatible(transaction_id, 'W', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'W', resource, success=False)
            return False
        self.add_lock(transaction_id, 'W', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'W', resource, success=True)
        return True

    def acquire_intent_read_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
        if not self.is_lock_compatible(transaction_id, 'IR', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'IR', resource, success=False)
            return False
        self.add_lock(transaction_id, 'IR', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'IR', resource, success=True)
        return True

    def acquire_intent_write_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):

        if not self.is_lock_compatible(transaction_id, 'IW', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'IW', resource, success=False)
            return False
        self.add_lock(transaction_id, 'IW', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'IW', resource, success=True)
        return True

    def acquire_update_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):

        if not self.is_lock_compatible(transaction_id, 'U', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'U', resource, success=False)
            return False
        self.add_lock(transaction_id, 'U', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'U', resource, success=True)
        return True

    def acquire_certify_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):

        if not self.is_lock_compatible(transaction_id, 'C', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'C', resource, success=False)
            return False
        self.add_lock(transaction_id, 'C', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'C', resource, success=True)
        return True

    def acquire_intent_update_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):

        if not self.is_lock_compatible(transaction_id, 'IU', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'IU', resource, success=False)
            return False
        self.add_lock(transaction_id, 'IU', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'IU', resource, success=True)
        return True

    def acquire_intent_certify_lock(self, transaction_id, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):

        if not self.is_lock_compatible(transaction_id, 'IC', resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
            self.add_lock_attempt(transaction_id, 'IC', resource, success=False)
            return False
        self.add_lock(transaction_id, 'IC', resource_original, resource)
        self.add_lock_attempt(transaction_id, 'IC', resource, success=True)
        return True

    def add_lock(self, transaction_id, lock_type, resource_original, resource):
        """ Adiciona o lock ao recurso no formato (transaction_id, lock_type) """
        if resource not in self.locks:
            self.locks[resource] = []
        self.locks[resource].append((transaction_id, lock_type))
        if (resource_original == resource):
            if [transaction_id, lock_type, resource_original, 'Passou'] not in  self.locks_approved:
                self.locks_approved.append([transaction_id, lock_type, resource, 'Passou'])

    def is_lock_compatible(self, transaction_id, new_lock_type, resource_original, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
        """ Verifica se o lock que está sendo requisitado é compatível com os locks existentes """
        existing_locks = self.locks.get(resource, [])
        for lock in existing_locks:
            existing_transaction_id, existing_lock_type = lock
            
            # Exceção: Não verificar conflito se a mesma transação está tentando adquirir o lock
            if existing_transaction_id == transaction_id:
                continue
            
            if not self.lock_compatibility_matrix.is_compatible(new_lock_type, existing_lock_type):
                
                # Chama a função add_wait passando as transações em conflito
                deadlock_manager.add_wait(existing_transaction_id, transaction_id)
                if deadlock_manager.detect_deadlock(existing_transaction_id, deadlock_manager.wait_grafo[existing_transaction_id], []):
                    recent = deadlock_manager.recent_transaction()
                    new_schedule = transaction_manager.abort_transaction(recent, schedule)
                    deadlock_manager.apagar_grafo(new_schedule)
                    self.reset_locks()
                    transaction_manager.start_processing(new_schedule, lock_manager, deadlock_manager, BD)
                    lock_manager.display_locks_approved()
                    lock_manager.display_waiting_transactions()
                    exit()

                if(resource_original == resource):
                    if [transaction_id, new_lock_type, resource] not in self.transactions_waiting:
                        self.add_waiting_transaction(transaction_id, new_lock_type, resource)
                    
                return False
            
        return True

    def add_waiting_transaction(self, transaction_id, lock_type, resource):
        """ Adiciona a transacao em espera a lista transactions_waiting """
        self.transactions_waiting.append([transaction_id, lock_type, resource])
    
    def display_locks_approved(self):
        """ Exibe todas as transações em espera de lock """
        if not self.locks_approved:
            print("Nenhuma transação aguardando lock.")
        else:
            print("Transações que passaram:")
            for transaction_id, lock_type, resource, status in self.locks_approved:
                print(f"Transacao {transaction_id} -> Tipo de lock: {lock_type} no recurso {resource} com status de {status}")

    def display_locks(self):
        """ Exibe todos os locks concedidos """
        if not self.locks:
            print("Nenhum lock foi adquirido.")
        else:
            print("Locks adquiridos:")
            for transaction_id, lock_type, resource in self.locks:
                print(f"Transacao {transaction_id} -> Tipo de lock: {lock_type} no recurso {resource}")

    def display_waiting_transactions(self):
        """ Exibe todas as transações em espera de lock """
        if not self.transactions_waiting:
            print("Nenhuma transação aguardando lock.")
        else:
            print("Transacoes aguardando liberação de outros bloqueios:")
            for transaction_id, lock_type, resource in self.transactions_waiting:
                print(f"Transacao {transaction_id} -> Tipo de lock: {lock_type} no recurso {resource}")

    def add_lock_attempt(self, transaction_id, lock_type, resource, success):
        """ Registra a tentativa de aquisição de um lock, com o resultado (1 para sucesso, 2 para falha) """
        if resource not in self.lock_attempts:
            self.lock_attempts[resource] = []

        status = 1 if success else 2
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
            print(f"Transacao {transaction_id} tentou {lock_type} -> {status_str}")

    def display_locks(self):
        """ Exibe todos os locks atualmente adquiridos em cada recurso """
        if not self.locks:
            print("Nenhum lock foi adquirido.")
        else:
            print("Locks adquiridos:")
            for resource, lock_list in self.locks.items():
                print(f"Recurso {resource}:")
                for transaction_id, lock_type in lock_list:
                    print(f"  Transacao {transaction_id} -> Tipo de lock: {lock_type}")

    def display_lock_attempts(self):
        """ Exibe todas as tentativas de aquisição de locks para todos os recursos """
        if not self.lock_attempts:
            print("Nenhuma tentativa de lock foi registrada.")
        else:
            print("Tentativas de lock registradas:")
            for resource, attempts in self.lock_attempts.items():
                print(f"Recurso {resource}:")
                for attempt in attempts:
                    transaction_id, lock_type, status = attempt
                    status_str = 'Sucesso' if status == 1 else 'Falha'
                    print(f"  Transacao {transaction_id} tentou {lock_type} -> {status_str}")

    def reset_locks(self):
        self.locks = {}
        self.lock_attempts = {}
        self.locks_approved = []
        self.transactions_waiting = []

    def commit_transaction(self, transaction_id, resource, deadlock_manager, transaction_manager, schedule, lock_manager, BD):
        print(f"Committing transaction {transaction_id}")
        # liberar todos os bloqueios
        self.release_locks(transaction_id, deadlock_manager)
        
        for element in self.transactions_waiting:
            transaction_id = element[0]
            operation = element[1]
            resource_original = element[2]
            print("---------------------------------")
            print(self.transactions_waiting)
            self.transactions_waiting = [
                el for el in self.transactions_waiting
                if not (el[0] == transaction_id and el[1] == operation and el[2] == resource_original)
            ]
            print(self.transactions_waiting)
            print("---------------------------------")
            print("transacoes que estão aguardando", resource_original)

            for aux in self.locks_approved:
                # [transaction_id, operation, resource]
                transaction_id2 = aux[0]
                operation2 = aux[1]
                resource_original2 = aux[2]
                status = aux[3]
                lock_manager.display_locks_approved()
                lock_manager.display_waiting_transactions()
                if (status == "Liberado") and transaction_id != transaction_id2 and [transaction_id, operation, resource_original, 'Passou'] not in  self.locks_approved:
                    if operation == 'C':
                        transaction_manager.process(transaction_id, operation, resource_original, resource_original2, lock_manager, deadlock_manager, schedule, BD)

                    elif transaction_manager.process(transaction_id, operation, resource_original, resource_original, lock_manager, deadlock_manager, schedule, BD):
                        childrens = BD.search_parent(resource_original).all_children()
                        parents = BD.search_parent(resource_original).all_parents()
                        for parent in parents:
                            transaction_manager.process(transaction_id, "I"+operation, resource_original, parent, lock_manager, deadlock_manager, schedule, BD)
                        for children in childrens:
                            transaction_manager.process(transaction_id, operation, resource_original, children, lock_manager, deadlock_manager, schedule, BD)
                elif (status=="Passou") and [transaction_id, operation, resource_original] not in self.transactions_waiting and [transaction_id, operation, resource_original, 'Passou'] not in self.locks_approved:
                    self.add_waiting_transaction(transaction_id, operation, resource_original)
                    break
    def release_locks(self, transaction_id, deadlock_manager):
        # Libera todos os locks associados à transação
        
        for element in self.transactions_waiting:
            # self.transactions_waiting =!= []
            if transaction_id == element[0]:
                print("Há transações esperando, liberar os locks pode não ser imediato.")
                self.add_waiting_transaction(transaction_id, 'C', '')
                break

        for resource, locks in list(self.locks.items()): 
            # Filtra apenas os locks que pertencem à transação atual
            new_locks = [lock for lock in locks if lock[0] != transaction_id]
            # Se havia locks da transação atual, liberá-los
            if len(new_locks) != len(locks):
                print(f"Liberando locks da Transação {transaction_id} no recurso {resource}")
                
                # Atualiza os locks do recurso com a lista filtrada
                if new_locks:
                    self.locks[resource] = new_locks
                else:
                    del self.locks[resource]  # Remove o recurso se não houver mais locks

                # Atualiza o status em locks_approved
                for lock in locks:
                    if lock[0] == transaction_id:
                        lock_type = lock[1]
                        # Registra a liberação no histórico de locks aprovados
                        #self.locks_approved -> (transaction_id, lock_type, resource, "Liberado")
                        for i in self.locks_approved:
                            if (i[0] == transaction_id) and (i[1] == lock_type) and (i[2] == resource):
                                i[3] = "Liberado"

        deadlock_manager.liberar_transacao(transaction_id)
        print(self.locks)
        print(f"Todos os locks da Transação {transaction_id} foram liberados.")

class LockCompatibilityMatrix:
    def __init__(self):
        self.matrix = {
            'R': {'R': True, 'W': True, 'C': False, 'U': False, 'IR': True, 'IW': True, 'IU': False, 'IC': False},
            'W': {'R': True, 'W': False, 'C': False, 'U': False, 'IR': True, 'IW': False, 'IU': False, 'IC': False},
            'C': {'R': False, 'W': False, 'C': False, 'U': False, 'IR': False, 'IW': False, 'IU': False, 'IC': False},
            'U': {'R': True, 'W': False, 'C': False, 'U': False, 'IR': True, 'IW': False, 'IU': False, 'IC': False},
            'IR': {'R': True, 'W': True, 'C': False, 'U': False, 'IR': True, 'IW': True, 'IU': True, 'IC': True},
            'IW': {'R': True, 'W': False, 'C': False, 'U': False, 'IR': True, 'IW': True, 'IU': True, 'IC': True},
            'IU': {'R': True, 'W': False, 'C': False, 'U': False, 'IR': True, 'IW': True, 'IU': True, 'IC': True},
            'IC': {'R': False, 'W': False, 'C': False, 'U': False, 'IR': True, 'IW': True, 'IU': True, 'IC': True}
        }

    def is_compatible(self, new_lock, existing_lock):
        return self.matrix[new_lock].get(existing_lock, False)