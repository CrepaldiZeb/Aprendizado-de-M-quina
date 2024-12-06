import random
import time


def aleatorio(x, range_inicial, range_final):
    numeros = set()
    while len(numeros) < x:
        num = random.randint(range_inicial, range_final)
        numeros.add(num)
    return list(numeros)


def mover_robo(robo, move, qnt_sala):
    if (move == 'direita') and ((robo + 1) <= qnt_sala - 1):
        return robo + 1
    elif (move == 'esquerda') and ((robo - 1) >= 0):
        return robo - 1
    else:
        return robo


def print_salas(modo, salas, robo):
    if modo == "Full":
        interface = [chr(i + 65) for i in range(len(salas))]
        int_robo = ['-' for _ in range(len(salas))]
        int_robo[robo] = 'X'
        print(interface)
        print(salas)
        print(int_robo)
        print("\n")


def limpa(sala):
    return all(i == '0' for i in sala)


def gulo_oni(sala, robo):
    lixo = [i for i in range(len(sala)) if sala[i] == '1']
    lixo_mais_proximo = None
    distancia_minima = float('inf')  # Infinito

    for l in lixo:
        distancia = abs(l - robo)  # Diferença absoluta entre as posições
        if distancia < distancia_minima:
            distancia_minima = distancia
            lixo_mais_proximo = l

    aux = robo - lixo_mais_proximo
    comandos = []

    if aux < 0:  # Direita
        comandos.extend(['direita'] * abs(aux))
    elif aux > 0:  # Esquerda
        comandos.extend(['esquerda'] * aux)
    else:
        comandos.append("limpar")

    return comandos


def modo_guloso(sala, robo, qnt_salas):
    print_salas("Full", sala, robo)

    while not limpa(sala):
        hold = robo
        comandos = gulo_oni(sala, robo)
        counter = 0

        while counter < len(comandos):
            comando_atual = comandos[counter]
            if comando_atual == "limpar":
                sala[robo] = '0'
                break
            elif comando_atual in ['esquerda', 'direita']:
                robo = mover_robo(robo, comando_atual, qnt_salas)

            counter += 1
            print_salas("Full", sala, robo)
            time.sleep(1)

    print("limpou")


def modo_manual_parcialmente(sala, robo, qnt_salas):
    mist = ['?' for _ in range(qnt_salas)]
    mist[robo] = sala[robo]
    print_salas("Full", mist, robo)

    while True:  # Remove a condição de verificação da limpeza
        hold = robo
        comando = input("Qual lado ele vai (digite 'sair' para terminar): ")
        if comando == "limpar":
            sala[hold] = '0'
            mist[hold] = '0'
        elif comando in ['esquerda', 'direita']:
            robo = mover_robo(robo, comando, qnt_salas)
            mist[robo] = sala[robo]
        elif comando == 'sair':
            break

        print_salas("Full", mist, robo)

    print("Jogo terminado pelo usuário.")


def modo_manual_oni(sala, robo, qnt_salas):
    print_salas("Full", sala, robo)

    while not limpa(sala):
        hold = robo
        comando = input("Qual lado ele vai: ")
        if comando == "limpar":
            sala[hold] = '0'
        elif comando in ['esquerda', 'direita']:
            robo = mover_robo(robo, comando, qnt_salas)
        elif comando == 'sair':
            break

        print_salas("Full", sala, robo)

    if limpa(sala):
        print("limpou")


def guloso_parcial(sala, robo, qnt_salas):
    mist = ['?' for _ in range(qnt_salas)]
    mist[robo] = sala[robo]
    salas_visitadas = [False] * qnt_salas
    salas_visitadas[robo] = True
    print_salas("Full", mist, robo)

    direcao = 'esquerda'  # Direção inicial

    while not all(salas_visitadas):  # Enquanto não visitar todas as salas
        hold = robo
        if sala[robo] == '1':
            sala[robo] = '0'
            mist[robo] = '0'  # Limpa e atualiza a memória
            print_salas("Full", mist, robo)
            time.sleep(1)  # Pausa pra visualizar a interface
            continue

        # Checa se chegou no lado mais esquerdo (posição 0).
        novo_robo = mover_robo(robo, direcao, qnt_salas)
        if novo_robo != robo:
            robo = novo_robo
            mist[robo] = sala[robo]  # Atualiza a memória
            salas_visitadas[robo] = True
        else:
            # Vai pra direita caso não seja possível ir à esquerda.
            direcao = 'direita'
            robo = mover_robo(robo, direcao, qnt_salas)
            mist[robo] = sala[robo]  # Atualiza memória
            salas_visitadas[robo] = True

        print_salas("Full", mist, robo)
        time.sleep(1)  # Pausa para visualizar

    print("Todas as salas foram visitadas e estão limpas.")


# Etapa de INICIALIZAÇÃO
while True:
    qnt_salas = int(input("Quantas salas? (máximo 10) "))
    if 1 <= qnt_salas <= 10:
        break
    print("Número inválido de salas. Por favor, escolha entre 1 e 10.")

while True:
    qnt_sujeira = int(input("Quantas sujas? (não mais que o número de salas) "))
    if 1 <= qnt_sujeira <= qnt_salas:
        break
    print("Número inválido de sujeira. Por favor, escolha entre 1 e o número de salas.")

sala = ['0' for _ in range(qnt_salas)]
aux = aleatorio(qnt_sujeira, 0, qnt_salas - 1)

# Inicializa SUJEIRA
for i in aux:
    sala[i] = '1'

# Inicializa O ROBO
robo = random.randint(0, qnt_salas - 1)

# Escolha do Modo
modo = input("Escolha o modo (guloso, guloso_parcial, manual_parcial, manual_oni): ")

if modo == 'guloso':
    modo_guloso(sala, robo, qnt_salas)
elif modo == 'guloso_parcial':
    guloso_parcial(sala, robo, qnt_salas)
elif modo == 'manual_parcial':
    modo_manual_parcialmente(sala, robo, qnt_salas)
elif modo == 'manual_oni':
    modo_manual_oni(sala, robo, qnt_salas)
else:
    print("Modo inválido.")
