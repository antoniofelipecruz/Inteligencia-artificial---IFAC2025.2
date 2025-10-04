import heapq

def calcular_menor_caminho(graph, no_inicial, no_final):
    """
    Encontra o menor caminho e o custo usando o algoritmo de Dijkstra.
    O algoritmo é ideal para grafos com custos não-negativos.
    """
    # Dicionário para armazenar o menor custo conhecido para cada nó
    custos = {no: float('infinity') for no in graph}
    custos[no_inicial] = 0
    
    # Dicionário para reconstruir o trajeto final
    antecessores = {no: None for no in graph}
    
    # Fila de prioridade para sempre visitar o nó de menor custo primeiro
    fila_prioridade = [(0, no_inicial)] # (custo, nó)
    
    while fila_prioridade:
        custo_atual, no_atual = heapq.heappop(fila_prioridade)
        
        # Se já encontramos um caminho mais curto, pulamos a iteração
        if custo_atual > custos[no_atual]:
            continue
            
        # Se chegamos ao destino, podemos parar (otimização)
        if no_atual == no_final:
            break
            
        # Explora os vizinhos do nó atual
        for vizinho, peso in graph[no_atual]:
            novo_custo = custo_atual + peso
            
            # Se um caminho mais curto para o vizinho for encontrado, atualiza
            if novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                antecessores[vizinho] = no_atual
                heapq.heappush(fila_prioridade, (novo_custo, vizinho))
                
    # Se não foi possível chegar ao destino
    if custos[no_final] == float('infinity'):
        return None, float('infinity')
        
    # Reconstrói o caminho do final para o início
    caminho = []
    no = no_final
    while no is not None:
        caminho.append(no)
        no = antecessores[no]
    caminho.reverse() # Inverte para ter a ordem correta (início -> fim)
    
    return caminho, custos[no_final]

# --- Definição do Grafo com Custos Corretos ---
# A fórmula de custo utilizada é: Custo = distância + 2 * pedágios 
graph = {
    'A': [], 'B': [], 'C': [], 'D': [], 'E': []
}

# Conexões bidirecionais [cite: 5]
# A <-> C: 11km, 0 pedágios -> Custo = 11 + (2*0) = 11 [cite: 10]
graph['A'].append(('C', 11)); graph['C'].append(('A', 11))
# B <-> D: 4km, 0 pedágios -> Custo = 4 + (2*0) = 4 [cite: 12]
graph['B'].append(('D', 4));  graph['D'].append(('B', 4))
# C <-> D: 3km, 1 pedágio -> Custo = 3 + (2*1) = 5 [cite: 13]
graph['C'].append(('D', 5));  graph['D'].append(('C', 5))
# D <-> E: 9km, 0 pedágios -> Custo = 9 + (2*0) = 9 [cite: 14]
graph['D'].append(('E', 9));  graph['E'].append(('D', 9))

# Conexões de mão única [cite: 5]
# A -> B: 2km, 1 pedágio -> Custo = 2 + (2*1) = 4 [cite: 11]
graph['A'].append(('B', 4))
# C -> E: 10km, 1 pedágio -> Custo = 10 + (2*1) = 12 [cite: 15]
graph['C'].append(('E', 12))
# B -> C: 8km, 0 pedágios -> Custo = 8 + (2*0) = 8 [cite: 16]
graph['B'].append(('C', 8))
# D -> A: 7km, 0 pedágios -> Custo = 7 + (2*0) = 7 [cite: 17]
graph['D'].append(('A', 7))


# --- Resolvendo o problema em etapas, conforme a ordem obrigatória A -> C -> E -> B ---
# 1. Menor caminho de A para C
caminho_ac, custo_ac = calcular_menor_caminho(graph, 'A', 'C')
# 2. Menor caminho de C para E
caminho_ce, custo_ce = calcular_menor_caminho(graph, 'C', 'E')
# 3. Menor caminho de E para B
caminho_eb, custo_eb = calcular_menor_caminho(graph, 'E', 'B')


# --- Apresentando o resultado final ---
if caminho_ac and caminho_ce and caminho_eb:
    # Une os trajetos, removendo os nós de junção duplicados
    trajeto_completo = caminho_ac + caminho_ce[1:] + caminho_eb[1:]
    custo_total = custo_ac + custo_ce + custo_eb
    
    print("--- Solução Final Baseada no Documento ---")
    print(f"O menor custo total do trajeto é: {custo_total}")
    print(f"Trajeto (lista de vértices): {' -> '.join(trajeto_completo)}")
    print("\n--- Detalhamento por Trecho ---")
    print(f"1. De A para C: {' -> '.join(caminho_ac)} (Custo: {custo_ac})")
    print(f"2. De C para E: {' -> '.join(caminho_ce)} (Custo: {custo_ce})")
    print(f"3. De E para B: {' -> '.join(caminho_eb)} (Custo: {custo_eb})")
else:
    print("Não foi possível encontrar um caminho que satisfaça a ordem A -> C -> E -> B.")