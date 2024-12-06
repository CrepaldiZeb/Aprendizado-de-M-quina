import numpy as np
from queue import PriorityQueue

# Estado inicial
initial_state = np.array([[2, 8, 1],
                          [0, 4, 3],
                          [7, 6, 5]], dtype=np.int8)

# Estado-alvo (objetivo)
target_state = np.array([[1, 2, 3],
                         [8, 0, 4],
                         [7, 6, 5]], dtype=np.int8)

# Outros estados para testes

teste1 = np.array([[1, 2, 3],
                   [0, 4, 5],
                   [7, 8, 6]], dtype=np.int8)
target_teste1 = np.array([[1, 2, 3],
                          [4, 5, 0],
                          [7, 8, 6]], dtype=np.int8)

teste2 = np.array([[1, 2, 3],
                   [0, 4, 5],
                   [7, 8, 6]], dtype=np.int8)
target_teste2 = np.array([[1, 2, 3],
                          [4, 5, 0],
                          [7, 8, 6]], dtype=np.int8)

teste3 = np.array([[1, 0, 2],
                   [4, 5, 3],
                   [7, 8, 6]], dtype=np.int8)
target_teste3 = np.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 0]], dtype=np.int8)


# Definição da classe Estado
class State:
    def __init__(self, matrix, parent, action, cost=0):
        self.matrix = matrix  # Matriz desse estado
        self.parent = parent  # Estado anterior
        self.action = action  # Movimento que resultou no estado
        self.cost = cost  # Custo desse estado


# Retorna a posição de um número na matriz
def find_number(matrix, number):
    for row in range(3):
        for col in range(3):
            if matrix[row][col] == number:
                return row, col


# Verifica se as matrizes são iguais
def are_matrices_equal(m1, m2):
    return np.array_equal(m1, m2)


# Calcula a distância de Manhattan entre a matriz atual e o objetivo
def compute_manhattan_distance(matrix, goal):
    cost = 0
    for num in range(1, 9):  # Ignorando o espaço em branco (0)
        row1, col1 = find_number(matrix, num)
        row2, col2 = find_number(goal, num)
        cost += abs(row1 - row2) + abs(col1 - col2)
    return cost


# Move o pivot para uma posição específica, caso seja possível
def move(matrix, action):
    row, col = find_number(matrix, 0)  # Encontrar o espaço em branco
    new_matrix = matrix.copy()

    # Verificar a ação e se é possível, e então fazer a troca
    if action == 'DIREITA' and col < 2:
        new_matrix[row][col], new_matrix[row][col + 1] = new_matrix[row][col + 1], new_matrix[row][col]
    elif action == 'ESQUERDA' and col > 0:
        new_matrix[row][col], new_matrix[row][col - 1] = new_matrix[row][col - 1], new_matrix[row][col]
    elif action == 'CIMA' and row > 0:
        new_matrix[row][col], new_matrix[row - 1][col] = new_matrix[row - 1][col], new_matrix[row][col]
    elif action == 'BAIXO' and row < 2:
        new_matrix[row][col], new_matrix[row + 1][col] = new_matrix[row + 1][col], new_matrix[row][col]

    return new_matrix


# Gera uma lista com todos os movimentos possíveis
def get_possible_actions(matrix):
    row, col = find_number(matrix, 0)
    actions = []

    if col < 2: actions.append('DIREITA')
    if col > 0: actions.append('ESQUERDA')
    if row > 0: actions.append('CIMA')
    if row < 2: actions.append('BAIXO')

    return actions


# Resolver o quebra-cabeça
def solve_puzzle(initial, goal):
    visited = []  # Lista para armazenar os estados já visitados
    queue = PriorityQueue()  # Fila de prioridade para armazenar os estados e seus custos
    count = 0  # Contador para ajudar na ordenação da fila
    queue.put((0, count, State(initial, None, None, 0)))  # Adicionando o estado inicial à fila

    # Continuar até que a fila esteja vazia
    while not queue.empty():
        _, _, current_state = queue.get()  # Obter o estado com o menor custo
        current_matrix = current_state.matrix

        # Verificar se o objetivo foi alcançado
        if are_matrices_equal(current_matrix, goal):
            print("Achou solução")
            path = []
            # Rastrear o caminho de volta ao estado inicial
            while current_state.action is not None:
                path.append(current_state.action)
                current_state = current_state.parent
                # Imprime o caminho contrário
            print("Caminho:", path[::-1])
            return

        # Verifica se já visitou o estado ou não
        if any(are_matrices_equal(current_matrix, visited_matrix) for visited_matrix in visited):
            continue

        visited.append(current_matrix)  # Marca o estado atual como visitado
        possible_actions = get_possible_actions(current_matrix)  # Movimentos possíveis

        # Para cada ação possível, mover, calcular o custo e adicionar o novo estado à fila
        for action in possible_actions:
            new_matrix = move(current_matrix, action)
            cost = compute_manhattan_distance(new_matrix, goal) + current_state.cost + 1
            count += 1  # Incrementa o contador
            new_state = State(new_matrix, current_state, action, cost)
            queue.put((cost, count, new_state))


# Testes da função

solve_puzzle(initial_state, target_state)
print('\nTeste 1 concluído')
solve_puzzle(teste1, target_teste1)
print('\nTeste 2 conclúido')
solve_puzzle(teste2, target_teste2)
print('\nTeste 3 concluído')
solve_puzzle(teste3, target_teste3)
print('\nTeste 4 concluído')
