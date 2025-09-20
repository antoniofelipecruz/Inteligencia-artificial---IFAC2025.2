from collections import deque  # Importa deque, uma fila de alta performance, útil para BFS

def bfs(grafo, inicio, objetivo):
    visitados = set()  # Conjunto para armazenar nós já visitados e evitar ciclos
    fila = deque([[inicio]])  # Fila que armazena caminhos, começando com o nó inicial

    while fila:  # Enquanto houver caminhos na fila
        caminho = fila.popleft()  # Remove o caminho mais antigo da fila (FIFO)
        no = caminho[-1]  # Pega o último nó do caminho, que é o nó atual

        if no == objetivo:  # Se o nó atual é o objetivo
            return caminho  # Retorna o caminho completo encontrado
        
        if no not in visitados:  # Se o nó ainda não foi visitado
            visitados.add(no)  # Marca o nó como visitado
            for vizinho in grafo.get(no, []):  # Itera sobre os vizinhos do nó atual
                novo_caminho = list(caminho)  # Cria uma cópia do caminho atual
                novo_caminho.append(vizinho)  # Adiciona o vizinho ao novo caminho
                fila.append(novo_caminho)  # Adiciona o novo caminho à fila para exploração futura

    return None  # Retorna None se não encontrar um caminho para o objetivo

# Exemplo de grafo representado como um dicionário
grafo = {
    "A": ["B", "C"],  # A conecta-se a B e C
    "B": ["D", "E"],  # B conecta-se a D e E
    "C": ["F"],       # C conecta-se a F
    "E": ["F"]        # E conecta-se a F
}

# Executa a busca BFS do nó "A" até o nó "F" e imprime o caminho encontrado
print("Busca Cega (BFS):", bfs(grafo, "A", "F"))


'''
Explicação resumida do funcionamento: 

- O algoritmo explora todos os caminhos possíveis em largura, ou seja, nível por nível. 
- Mantém uma fila de caminhos completos para poder reconstruir a solução quando o objetivo é alcançado. 
- Usa um conjunto visitados para evitar explorar o mesmo nó repetidamente, prevenindo loops infinitos.
'''