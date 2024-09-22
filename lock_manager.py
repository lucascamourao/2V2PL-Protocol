class LockManager:
    def __init__(self):
        print("A LockManager has been created. \n")
        # Armazena os locks para cada recurso
        self.locks = {}
        # Armazena as tentativas de aquisição de locks
        self.lock_attempts = {}
        # Pega a matriz com as comparações
        self.lock_compatibility_matrix = LockCompatibilityMatrix()

    def acquire_shared_lock(self, transaction_id, resource, deadlock_manager):
        print(
            f"{transaction_id} tentando adquirir lock compartilhado (leitura) em {resource}"
        )
        if not self.is_lock_compatible(transaction_id, "R", resource, deadlock_manager):
            self.add_lock_attempt(transaction_id, "R", resource, success=False)
            return False
        self.add_lock(transaction_id, "R", resource)
        self.add_lock_attempt(transaction_id, "R", resource, success=True)
        return True

    def acquire_exclusive_lock(self, transaction_id, resource, deadlock_manager):
        print(
            f"{transaction_id} tentando adquirir lock exclusivo (escrita) em {resource}"
        )
        if not self.is_lock_compatible(transaction_id, "W", resource, deadlock_manager):
            self.add_lock_attempt(transaction_id, "W", resource, success=False)
            return False
        self.add_lock(transaction_id, "W", resource)
        self.add_lock_attempt(transaction_id, "W", resource, success=True)
        return True

    def acquire_intent_read_lock(self, transaction_id, resource, deadlock_manager):
        print(
            f"{transaction_id} tentando adquirir lock intencional de leitura em {resource}"
        )
        if not self.is_lock_compatible(
            transaction_id, "IR", resource, deadlock_manager
        ):
            self.add_lock_attempt(transaction_id, "IR", resource, success=False)
            return False
        self.add_lock(transaction_id, "IR", resource)
        self.add_lock_attempt(transaction_id, "IR", resource, success=True)
        return True

    def acquire_intent_write_lock(self, transaction_id, resource, deadlock_manager):
        print(
            f"{transaction_id} tentando adquirir lock intencional de escrita em {resource}"
        )
        if not self.is_lock_compatible(
            transaction_id, "IW", resource, deadlock_manager
        ):
            self.add_lock_attempt(transaction_id, "IW", resource, success=False)
            return False
        self.add_lock(transaction_id, "IW", resource)
        self.add_lock_attempt(transaction_id, "IW", resource, success=True)
        return True

    def acquire_update_lock(self, transaction_id, resource, deadlock_manager):
        print(f"{transaction_id} tentando adquirir lock de update em {resource}")
        if not self.is_lock_compatible(transaction_id, "U", resource, deadlock_manager):
            self.add_lock_attempt(transaction_id, "U", resource, success=False)
            return False
        self.add_lock(transaction_id, "U", resource)
        self.add_lock_attempt(transaction_id, "U", resource, success=True)
        return True

    def acquire_certify_lock(self, transaction_id, resource, deadlock_manager):
        print(f"{transaction_id} tentando adquirir lock de certificação em {resource}")
        if not self.is_lock_compatible(transaction_id, "C", resource, deadlock_manager):
            self.add_lock_attempt(transaction_id, "C", resource, success=False)
            return False
        self.add_lock(transaction_id, "C", resource)
        self.add_lock_attempt(transaction_id, "C", resource, success=True)
        return True

    def acquire_intent_update_lock(self, transaction_id, resource, deadlock_manager):
        print(
            f"{transaction_id} tentando adquirir lock intencional de update em {resource}"
        )
        if not self.is_lock_compatible(
            transaction_id, "IU", resource, deadlock_manager
        ):
            self.add_lock_attempt(transaction_id, "IU", resource, success=False)
            return False
        self.add_lock(transaction_id, "IU", resource)
        self.add_lock_attempt(transaction_id, "IU", resource, success=True)
        return True

    def acquire_intent_certify_lock(self, transaction_id, resource, deadlock_manager):
        print(
            f"{transaction_id} tentando adquirir lock intencional de Certify em {resource}"
        )
        if not self.is_lock_compatible(
            transaction_id, "IC", resource, deadlock_manager
        ):
            self.add_lock_attempt(transaction_id, "IC", resource, success=False)
            return False
        self.add_lock(transaction_id, "IC", resource)
        self.add_lock_attempt(transaction_id, "IC", resource, success=True)
        return True

    def add_lock(self, transaction_id, lock_type, resource):
        """Adiciona o lock ao recurso no formato (transaction_id, lock_type)"""
        if resource not in self.locks:
            self.locks[resource] = []
        self.locks[resource].append((transaction_id, lock_type))
        print(
            f"Lock {lock_type} adquirido pela Transacao {transaction_id} no recurso {resource}"
        )
        print(
            f"--------------------------------------------------------------------------------"
        )

    def is_lock_compatible(
        self, transaction_id, new_lock_type, resource, deadlock_manager
    ):
        """Verifica se o lock que está sendo requisitado é compatível com os locks existentes"""
        existing_locks = self.locks.get(resource, [])
        for lock in existing_locks:
            existing_transaction_id, existing_lock_type = lock

            # Exceção: Não verificar conflito se a mesma transação está tentando adquirir o lock
            if existing_transaction_id == transaction_id:
                continue

            if not self.lock_compatibility_matrix.is_compatible(
                new_lock_type, existing_lock_type
            ):
                print(
                    f"Lock {new_lock_type} nao eh compativel com {existing_lock_type} no recurso {resource}"
                )
                print(
                    f"-------------------------------------------------------------------------------------"
                )

                # Chama a função add_wait passando as transações em conflito
                deadlock_manager.add_wait(existing_transaction_id, transaction_id)
                if deadlock_manager.detect_deadlock(existing_transaction_id, deadlock_manager.wait_grafo[existing_transaction_id], []):
                    deadlock_manager.recent_transaction()
                return False

        return True

    def add_lock_attempt(self, transaction_id, lock_type, resource, success):
        """Registra a tentativa de aquisição de um lock, com o resultado (1 para sucesso, 2 para falha)"""
        if resource not in self.lock_attempts:
            self.lock_attempts[resource] = []

        status = 1 if success else 2
        self.lock_attempts[resource].append((transaction_id, lock_type, status))

    def plot_lock_attempts(self, resource):
        """Exibe a lista de tentativas de bloqueios de um recurso específico"""
        attempts = self.lock_attempts.get(resource, [])
        if not attempts:
            print(
                f"Não há tentativas de bloqueio registradas para o recurso {resource}."
            )
            return

        print(f"Tentativas de bloqueio para o recurso {resource}:")
        for attempt in attempts:
            transaction_id, lock_type, status = attempt
            status_str = "Sucesso" if status == 1 else "Falha"
            print(f"Transacao {transaction_id} tentou {lock_type} -> {status_str}")

    def display_locks(self):
        """Exibe todos os locks atualmente adquiridos em cada recurso"""
        if not self.locks:
            print("Nenhum lock foi adquirido.")
        else:
            print("Locks adquiridos:")
            for resource, lock_list in self.locks.items():
                print(f"Recurso {resource}:")
                for transaction_id, lock_type in lock_list:
                    print(f"  Transacao {transaction_id} -> Tipo de lock: {lock_type}")

    def display_lock_attempts(self):
        """Exibe todas as tentativas de aquisição de locks para todos os recursos"""
        if not self.lock_attempts:
            print("Nenhuma tentativa de lock foi registrada.")
        else:
            print("Tentativas de lock registradas:")
            for resource, attempts in self.lock_attempts.items():
                print(f"Recurso {resource}:")
                for attempt in attempts:
                    transaction_id, lock_type, status = attempt
                    status_str = "Sucesso" if status == 1 else "Falha"
                    print(
                        f"  Transacao {transaction_id} tentou {lock_type} -> {status_str}"
                    )


class LockCompatibilityMatrix:
    def __init__(self):
        self.matrix = {
            "R": {
                "R": True,
                "W": True,
                "C": False,
                "U": False,
                "IR": True,
                "IW": True,
                "IU": False,
                "IC": False,
            },
            "W": {
                "R": True,
                "W": False,
                "C": False,
                "U": False,
                "IR": True,
                "IW": False,
                "IU": False,
                "IC": False,
            },
            "C": {
                "R": False,
                "W": False,
                "C": False,
                "U": False,
                "IR": False,
                "IW": False,
                "IU": False,
                "IC": False,
            },
            "U": {
                "R": True,
                "W": False,
                "C": False,
                "U": False,
                "IR": True,
                "IW": False,
                "IU": False,
                "IC": False,
            },
            "IR": {
                "R": True,
                "W": True,
                "C": False,
                "U": False,
                "IR": True,
                "IW": True,
                "IU": True,
                "IC": True,
            },
            "IW": {
                "R": True,
                "W": False,
                "C": False,
                "U": False,
                "IR": True,
                "IW": True,
                "IU": True,
                "IC": True,
            },
            "IU": {
                "R": True,
                "W": False,
                "C": False,
                "U": False,
                "IR": True,
                "IW": True,
                "IU": True,
                "IC": True,
            },
            "IC": {
                "R": False,
                "W": False,
                "C": False,
                "U": False,
                "IR": True,
                "IW": True,
                "IU": True,
                "IC": True,
            },
        }

    def is_compatible(self, new_lock, existing_lock):
        return self.matrix[new_lock].get(existing_lock, False)
