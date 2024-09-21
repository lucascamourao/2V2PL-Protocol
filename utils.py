# Funções utilitárias

# supondo que cada transação tem 3 operações
def parse_schedule(input_str):
    parsed_schedule = []

    for element in range(0, len(input_str), 3):
        tuple = (input_str[element], input_str[element+1], input_str[element+2])

        parse_schedule.append(tuple)

    # Função para converter uma string de entrada de transações em uma lista estruturada
    # Exemplo de input: "T1: R(A), W(A); T2: R(B), W(B)"
    # Saída: [('T1', 'R', 'A'), ('T1', 'W', 'A'), ('T2', 'R', 'B'), ('T2', 'W', 'B')]
    return parsed_schedule
