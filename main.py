from transaction_manager import TransactionManager
from lock_manager import LockManager
from deadlock_manager import DeadlockDetection
from utils import create_environment

# Iniciar o gerenciador de transações e locks
transaction_manager = TransactionManager()
lock_manager = LockManager()
deadlock_manager = DeadlockDetection()
BD = create_environment()

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

    deadlock_manager.start_grafo(schedule)

    # Processar o escalonamento
    transaction_manager.start_processing(schedule, lock_manager, deadlock_manager)

if __name__ == '__main__':
    main()
