# A busca em largura (BFS) é usada para encontrar o **menor caminho** até a saída de um labirinto.

from collections import deque  # Importa deque para implementar uma fila eficiente (FIFO)

def bfs_labirinto(labirinto, inicio, objetivo):
    linhas, colunas = len(labirinto), len(labirinto[0])  # Dimensões do labirinto
    fila = deque([(inicio, [inicio])])  # Fila que armazena tuplas (posição atual, caminho percorrido)
    visitados = set([inicio])  # Conjunto de posições já visitadas para evitar ciclos

    while fila:  # Enquanto houver posições a explorar
        (x, y), caminho = fila.popleft()  # Remove a posição mais antiga da fila

        if (x, y) == objetivo:  # Se a posição atual é a saída
            return caminho  # Retorna o caminho completo até a saída

        # Movimentos possíveis: cima, baixo, esquerda, direita
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x + dx, y + dy  # Calcula a nova posição
            # Verifica se a nova posição está dentro dos limites do labirinto,
            # se é um caminho livre (0) e se ainda não foi visitada
            if 0 <= nx < linhas and 0 <= ny < colunas and labirinto[nx][ny] == 0 and (nx, ny) not in visitados:
                fila.append(((nx, ny), caminho + [(nx, ny)]))  # Adiciona a nova posição e caminho à fila
                visitados.add((nx, ny))  # Marca a posição como visitada
    return None  # Retorna None se não houver caminho até a saída

# Função para exibir o labirinto
def exibir_labirinto(labirinto, caminho=None):
    caminho = caminho or []  # Se nenhum caminho for fornecido, mantém vazio
    for i, linha in enumerate(labirinto):
        linha_exibida = ""
        for j, celula in enumerate(linha):
            if (i, j) in caminho:
                linha_exibida += "*"  # Marca o caminho percorrido
            elif celula == 1:
                linha_exibida += "#"  # Parede
            else:
                linha_exibida += " "  # Caminho livre
        print(linha_exibida)

# Representação do labirinto
# 0 = caminho livre
# 1 = parede
labirinto = [
    [0,1,0,0,0],
    [0,1,0,1,0],
    [0,0,0,1,0],
    [1,1,0,0,0]
]

# Executa a BFS do ponto inicial (0,0) até a saída (3,4)
caminho = bfs_labirinto(labirinto, (0,0), (3,4))
print("Caminho encontrado (BFS):", caminho)

# Exibe o labirinto com o caminho encontrado
print("\nLabirinto com o caminho:")
exibir_labirinto(labirinto, caminho)

'''
Explicação resumida do funcionamento:

- BFS explora todos os caminhos nível por nível.
- Mantém uma fila de posições com o caminho percorrido para reconstruir a solução.
- Usa um conjunto visitados para não visitar a mesma posição duas vezes, evitando loops.
- Retorna o caminho mais curto do início até a saída.
- A função exibir_labirinto mostra o labirinto com paredes (#), caminhos livres ( ) e o caminho encontrado (*).
'''
