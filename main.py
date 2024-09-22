from transaction_manager import TransactionManager
from lock_manager import LockManager
from deadlock_manager import DeadlockDetection

# Iniciar o gerenciador de transações e locks
transaction_manager = TransactionManager()
lock_manager = LockManager()
deadlock_manager = DeadlockDetection()


def main():
    # Exemplo de escalonamento: T1: R(A), W(A), T2: R(B), W(B), ...
    schedule = [
        ["T1", "R", "A"],
        ["T1", "W", "A"],
        ["T2", "R", "B"],
        ["T3", "W", "B"],
        ["T3", "R", "A"],
        ["T2", "W", "B"],
        ["T2", "W", "C"],
        ["T1", "W", "C"],
        ["T3", "W", "A"],
    ]

    deadlock_manager.start_grafo(schedule)

    # Processar o escalonamento
    transaction_manager.start_processing(schedule, lock_manager, deadlock_manager)

    lock_manager.display_locks()
    lock_manager.display_lock_attempts()

    # if deadlock_manager.detect_deadlock('T1', deadlock_manager.wait_grafo['T1'], []):
    # print(deadlock_manager.recent_transaction())


if __name__ == "__main__":
    main()
