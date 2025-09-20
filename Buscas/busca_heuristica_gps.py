# Exemplo de busca A* aplicada a um "mapa", semelhante a um GPS
# Encontrar a melhor rota (menor custo) do ponto inicial até o destino

import heapq  # Importa heapq para implementar uma fila de prioridade (min-heap)

def a_star_mapa(grafo, heuristica, inicio, objetivo):
    # Fila de prioridade inicial: tupla (f, g, caminho)
    # f = custo total estimado (g + h)
    # g = custo real do caminho percorrido até o nó atual
    # caminho = lista de nós visitados até o momento
    fila = [(0 + heuristica[inicio], 0, [inicio])]
    visitados = set()  # Conjunto de nós visitados para evitar ciclos

    while fila:  # Enquanto houver nós para explorar
        f, g, caminho = heapq.heappop(fila)  # Remove o nó com menor f (mais promissor)
        no = caminho[-1]  # Pega o último nó do caminho (nó atual)

        if no == objetivo:  # Se chegou ao destino
            return caminho  # Retorna o caminho completo encontrado

        if no not in visitados:  # Se o nó ainda não foi visitado
            visitados.add(no)  # Marca o nó como visitado
            for vizinho, custo in grafo.get(no, []):  # Itera sobre vizinhos e seus custos
                novo_g = g + custo  # Atualiza o custo real até o vizinho
                novo_f = novo_g + heuristica[vizinho]  # Calcula f = g + h
                heapq.heappush(fila, (novo_f, novo_g, caminho + [vizinho]))

    return None  # Retorna None se não houver caminho até o destino

# Função para exibir o mapa das cidades com as conexões e distâncias
def exibir_mapa(grafo):
    print("\nMapa das cidades e conexões:")
    for cidade, vizinhos in grafo.items():
        conexoes = ", ".join([f"{v}({c})" for v, c in vizinhos])
        print(f"{cidade} -> {conexoes}")

# Função para desenhar o mapa visualmente como no comentário
def desenhar_mapa():
    print("""
       5          4
   A ------ B ------ D
   |         \\
   |2         2
   |           \\
   C --------- E
       7         \\
                  1
                   \\
                    G
   F
   |
   2
   G
""")

# Grafo representando cidades e distâncias entre elas
grafo = {
    "A": [("B", 5), ("C", 2)],
    "B": [("D", 4), ("E", 2)],
    "C": [("F", 7)],
    "D": [("G", 3)],
    "E": [("G", 1)],
    "F": [("G", 2)]
}

# Heurística: distância em linha reta até a cidade G (objetivo)
heuristica = {"A": 7, "B": 6, "C": 4, "D": 2, "E": 1, "F": 3, "G": 0}

# Exibe o mapa textual
exibir_mapa(grafo)

# Exibe o mapa desenhado
desenhar_mapa()

# Executa a busca A* do ponto A até G e imprime o caminho encontrado
print("Caminho encontrado pelo A*:", a_star_mapa(grafo, heuristica, "A", "G"))

'''
Resumo do funcionamento:

- O grafo representa cidades (nós) e distâncias (arestas).
- A* busca o caminho de menor custo do início ao destino, combinando:
g: custo real percorrido
h: estimativa até o objetivo
f = g + h: prioridade na exploração
- Usa fila de prioridade e evita ciclos com um conjunto de visitados.
- Ao chegar no destino, retorna o caminho ótimo.
- exibir_mapa() e desenhar_mapa() mostram conexões e o mapa visual.
'''