# Funções utilitárias


# supondo que cada transação tem 3 operações
def parse_schedule(input_str):
    parsed_schedule = []

    for element in range(0, len(input_str), 3):
        line = [input_str[element], input_str[element + 1], input_str[element + 2]]

        parse_schedule.append(line)

    # Função para converter uma string de entrada de transações em uma lista estruturada
    # Exemplo de input: "T1: R(A), W(A); T2: R(B), W(B)"
    # Saída: [('T1', 'R', 'A'), ('T1', 'W', 'A'), ('T2', 'R', 'B'), ('T2', 'W', 'B')]
    return parsed_schedule


"""
Seja S uma string, 

S[0] é a transação. Ex: 'T1'

S[1] é a operação. Ex: 'R'.

S[2] é o recurso (onde será aplicada a operação). Ex: 'A'.

"""
