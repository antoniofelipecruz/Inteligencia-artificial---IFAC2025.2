import heapq  # Importa heapq, usado para implementar uma fila de prioridade (min-heap)

def a_star(grafo, heuristica, inicio, objetivo):
    # Fila de prioridade inicial: tupla (f = g + h, g, caminho)
    # f = custo total estimado (g + h)
    # g = custo real do caminho até o nó atual
    # caminho = lista de nós visitados até o momento
    fila = [(0 + heuristica[inicio], 0, [inicio])]
    visitados = set()  # Conjunto para armazenar nós já visitados e evitar ciclos

    while fila:  # Enquanto houver nós para explorar
        f, g, caminho = heapq.heappop(fila)  # Remove o nó com menor f (mais promissor)
        no = caminho[-1]  # Pega o último nó do caminho (nó atual)

        # Debug opcional: imprime o estado atual da fila e do caminho
        # print(f"Explorando nó: {no}, caminho: {caminho}, f: {f}, g: {g}")

        if no == objetivo:  # Se chegou ao objetivo
            return caminho  # Retorna o caminho completo encontrado

        if no not in visitados:  # Se o nó ainda não foi visitado
            visitados.add(no)  # Marca o nó como visitado
            for vizinho, custo in grafo.get(no, []):  # Itera sobre os vizinhos e seus custos
                novo_g = g + custo  # Atualiza o custo real até o vizinho
                novo_f = novo_g + heuristica[vizinho]  # Calcula f = g + h para o vizinho
                # Adiciona o novo caminho à fila de prioridade
                heapq.heappush(fila, (novo_f, novo_g, caminho + [vizinho]))

    return None  # Retorna None se não encontrar caminho até o objetivo

# Grafo com custos para cada aresta
grafo = {
    "A": [("B", 1), ("C", 3)],  # A conecta-se a B (custo 1) e C (custo 3)
    "B": [("D", 1), ("E", 5)],  # B conecta-se a D (1) e E (5)
    "C": [("F", 2)],             # C conecta-se a F (2)
    "D": [("G", 2)],             # D conecta-se a G (2)
    "E": [("G", 1)],             # E conecta-se a G (1)
    "F": [("G", 5)]              # F conecta-se a G (5)
}

# Heurística: estimativa de distância até o objetivo "G"
heuristica = {
    "A": 7, "B": 6, "C": 2,
    "D": 1, "E": 1, "F": 2, "G": 0
}

# Executa a busca A* do nó "A" até o nó "G" e imprime o caminho encontrado
print("Busca Heurística (A*):", a_star(grafo, heuristica, "A", "G"))


'''
Explicação resumida do funcionamento:

- A* combina custo real do caminho (g) com estimativa até o objetivo (h) para priorizar caminhos mais promissores.
- Usa uma fila de prioridade (min-heap) para sempre explorar o nó com menor f = g + h.
- Mantém um conjunto visitados para evitar ciclos.
- Retorna o caminho ótimo do início até o objetivo, considerando tanto os custos reais quanto a heurística.
'''
