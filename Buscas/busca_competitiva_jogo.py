import math  # Importa math para usar infinito (inf) na inicialização dos valores extremos

# Função para imprimir o tabuleiro de forma legível
def imprimir_tabuleiro(tabuleiro):
    print("\nTabuleiro:")  
    for i, linha in enumerate(tabuleiro):
        print(" | ".join(linha))  # Junta as células da linha com "|"
        if i < len(tabuleiro) - 1:
            print("-" * 9)  # Separador entre linhas para visualização

# Função que verifica se há um vencedor
def verificar_vencedor(tabuleiro):
    # Combina linhas e colunas (zip(*tabuleiro) transpõe o tabuleiro)
    linhas = tabuleiro + list(map(list, zip(*tabuleiro)))
    # Diagonais principais
    diagonais = [[tabuleiro[i][i] for i in range(3)], [tabuleiro[i][2-i] for i in range(3)]]
    for trio in linhas + diagonais:
        if trio.count("X") == 3: return "X"  # X venceu
        if trio.count("O") == 3: return "O"  # O venceu
    return None  # Nenhum vencedor ainda

# Retorna todas as posições livres no tabuleiro
def movimentos_possiveis(tabuleiro):
    return [(i,j) for i in range(3) for j in range(3) if tabuleiro[i][j] == " "]

# Função Minimax recursiva
def minimax(tabuleiro, profundidade, maximizando):
    vencedor = verificar_vencedor(tabuleiro)  # Verifica se há vencedor
    if vencedor == "X": return 1      # Vitória do maximizador
    if vencedor == "O": return -1     # Vitória do minimizador
    if not movimentos_possiveis(tabuleiro): return 0  # Empate

    if maximizando:  # Turno de X (maximizar)
        melhor = -math.inf  # Inicializa com menor valor possível
        for i, j in movimentos_possiveis(tabuleiro):
            tabuleiro[i][j] = "X"  # Testa jogada
            valor = minimax(tabuleiro, profundidade+1, False)  # Avalia jogada recursivamente
            tabuleiro[i][j] = " "  # Desfaz jogada
            melhor = max(melhor, valor)  # Atualiza melhor valor
        return melhor
    else:  # Turno de O (minimizar)
        melhor = math.inf  # Inicializa com maior valor possível
        for i, j in movimentos_possiveis(tabuleiro):
            tabuleiro[i][j] = "O"  # Testa jogada
            valor = minimax(tabuleiro, profundidade+1, True)  # Avalia jogada recursivamente
            tabuleiro[i][j] = " "  # Desfaz jogada
            melhor = min(melhor, valor)  # Atualiza menor valor
        return melhor

# Função que calcula a melhor jogada para X usando Minimax
def melhor_jogada(tabuleiro):
    melhor_valor = -math.inf  # Inicializa com menor valor possível
    jogada = None
    for i, j in movimentos_possiveis(tabuleiro):
        tabuleiro[i][j] = "X"  # Testa jogada
        valor = minimax(tabuleiro, 0, False)  # Avalia jogada
        tabuleiro[i][j] = " "  # Desfaz jogada
        if valor > melhor_valor:  # Se a jogada for melhor que a atual
            melhor_valor = valor
            jogada = (i, j)  # Atualiza a melhor jogada
    return jogada

# Estado parcial do jogo
tabuleiro = [
    ["X","O","X"],
    ["O","X"," "],
    [" "," ","O"]
]

# Imprime o tabuleiro antes da jogada
imprimir_tabuleiro(tabuleiro)

# Calcula a melhor jogada para X
jogada = melhor_jogada(tabuleiro)
print("\nMelhor jogada para X:", jogada)

# Marca a jogada no tabuleiro
if jogada:
    i, j = jogada
    tabuleiro[i][j] = "X"

# Imprime o tabuleiro após a jogada
imprimir_tabuleiro(tabuleiro)

'''
Resumo do funcionamento:

- Minimax explora todas as jogadas possíveis recursivamente:
X → maximizador, quer maximizar o valor
O → minimizador, quer minimizar o valor
- Função melhor_jogada: testa cada movimento de X e escolhe o que leva ao maior valor possível.
- Função imprimir_tabuleiro: mostra o tabuleiro antes e depois da jogada, facilitando visualização.
- Retorna a posição ótima para X e atualiza o tabuleiro com essa jogada.
'''