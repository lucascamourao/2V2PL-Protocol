# Gerenciamento de transações (start, commit, abort)class TransactionManager:

class TransactionManager:
    def __init__(self):
        print('A TransactionManager has been created.\n')
        self.active_transactions = {}  # Armazena transações ativas

    def start_transaction(self, transaction_id):
        print(f"Starting transaction {transaction_id}")
        self.active_transactions[transaction_id] = {'status': 'active'}

    def process(self, transaction_id, operation, resource, lock_manager):
        # Aqui, gerencie a lógica para processar cada operação (R, W) em um recurso
        print(f"Processing {operation} on {resource} by {transaction_id}")
        
        # Adquirir o lock necessário
        if operation == 'R':
            return lock_manager.acquire_shared_lock(transaction_id, resource)
        elif operation == 'W':
            return lock_manager.acquire_exclusive_lock(transaction_id, resource)

    def commit_transaction(self, transaction_id):
        print(f"Committing transaction {transaction_id}")
        self.active_transactions.pop(transaction_id, None)

    def abort_transaction(self, transaction_id):
        print(f"Aborting transaction {transaction_id}")
        self.active_transactions.pop(transaction_id, None)
