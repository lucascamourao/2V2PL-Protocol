from transaction_manager import TransactionManager
from lock_manager import LockManager
from deadlock_detection import detect_deadlock

# Iniciar o gerenciador de transações e locks
transaction_manager = TransactionManager()
lock_manager = LockManager()

def main():
    # Exemplo de escalonamento: T1: R(A), W(A), T2: R(B), W(B), ...
    schedule = [
        ['T1', 'R', 'A'], 
        ['T1', 'W', 'A'], 
        ['T2', 'R', 'B'], 
        ['T2', 'W', 'B'], 
        ['T3', 'R', 'A'], 
        ['T3', 'W', 'B']
    ]

    # Processar o escalonamento
    for transaction, operation, resource in schedule:
        if not transaction_manager.process(transaction, operation, resource, lock_manager):
            print(f"Deadlock detected during {transaction}'s operation on {resource}.")
            detect_deadlock()
            break

if __name__ == '__main__':
    main()
