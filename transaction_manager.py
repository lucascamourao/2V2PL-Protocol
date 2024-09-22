# Gerenciamento de transações (start, commit, abort)class TransactionManager:

class TransactionManager:
    def __init__(self):
        print("A TransactionManager has been created.\n")
        self.active_transactions = {}  # Armazena transações ativas

    def start_transaction(self, transaction_id):
        print(f"Starting transaction {transaction_id}")
        self.active_transactions[transaction_id] = {"status": "active"}

    def start_processing(self, schedule, lock_manager, deadlock_manager):
        print(schedule)

        for element in schedule:
            if element != "Transação abortada":
                # [transaction_id, operation, resource]
                transaction_id = element[0]
                operation = element[1]
                resource = element[2]
                self.process(
                    transaction_id,
                    operation,
                    resource,
                    lock_manager,
                    deadlock_manager,
                    schedule,
                )

    def process(
        self,
        transaction_id,
        operation,
        resource,
        lock_manager,
        deadlock_manager,
        schedule,
    ):
        # Aqui, gerencie a lógica para processar cada operação (R, W, U, C, IR, IW, IU, IC) em um recurso
        print(f"Processing {operation} on {resource} by {transaction_id}")
        # Adquirir o lock necessário
        if operation == "R":
            return lock_manager.acquire_shared_lock(
                transaction_id,
                resource,
                deadlock_manager,
                self,
                schedule,
            )
        elif operation == "W":
            return lock_manager.acquire_exclusive_lock(
                transaction_id,
                resource,
                deadlock_manager,
                self,
                schedule,
            )
        elif operation == "U":
            return lock_manager.acquire_update_lock(
                transaction_id, resource, deadlock_manager
            )
        elif operation == "C":
            return lock_manager.acquire_certify_lock(
                transaction_id, resource, deadlock_manager
            )
        elif operation == "IR":
            return lock_manager.acquire_intent_read_lock(
                transaction_id, resource, deadlock_manager
            )
        elif operation == "IW":
            return lock_manager.acquire_intent_write_lock(
                transaction_id, resource, deadlock_manager
            )
        elif operation == "IU":
            return lock_manager.acquire_intent_update_lock(
                transaction_id, resource, deadlock_manager
            )
        elif operation == "IC":
            return lock_manager.acquire_intent_certify_lock(
                transaction_id, resource, deadlock_manager
            )

    def commit_transaction(self, transaction_id):
        print(f"Committing transaction {transaction_id}")
        self.active_transactions.pop(transaction_id, None)

    def abort_transaction(self, transaction_id, schedule):
        print(f"Aborting transaction {transaction_id}")
        self.active_transactions.pop(transaction_id, None)

        for i in range(len(schedule)):
            if schedule[i][0] == transaction_id:
                schedule[i] = "Transação abortada"

        new_schedule = [op for op in schedule if op is not None]

        return new_schedule