def minimax(no, profundidade, maximizando, alfa, beta):
    # Caso base: chegamos à profundidade 0 ou nó folha (valor numérico)
    if profundidade == 0 or isinstance(no, int):
        return no  # Retorna o valor do nó
    
    if maximizando:  # Turno do jogador que quer **maximizar** o valor
        valor = float('-inf')  # Inicializa com o menor valor possível
        for filho in no:  # Itera sobre todos os filhos do nó
            # Chamada recursiva para o nó filho, alternando para minimizador
            valor = max(valor, minimax(filho, profundidade-1, False, alfa, beta))
            alfa = max(alfa, valor)  # Atualiza alfa (melhor valor para maximizador até agora)
            if beta <= alfa:  # Condição de poda alfa-beta
                break  # Não é necessário explorar outros filhos
        return valor  # Retorna o melhor valor encontrado para o maximizador
    else:  # Turno do jogador que quer **minimizar** o valor
        valor = float('inf')  # Inicializa com o maior valor possível
        for filho in no:  # Itera sobre todos os filhos do nó
            # Chamada recursiva para o nó filho, alternando para maximizador
            valor = min(valor, minimax(filho, profundidade-1, True, alfa, beta))
            beta = min(beta, valor)  # Atualiza beta (melhor valor para minimizador até agora)
            if beta <= alfa:  # Condição de poda alfa-beta
                break  # Não é necessário explorar outros filhos
        return valor  # Retorna o melhor valor encontrado para o minimizador

# Árvore de jogo representada como listas aninhadas
# Cada lista interna representa os possíveis movimentos futuros
# Folhas são valores finais do jogo (pontuação)
arvore = [
    [3, 5, 6],       # primeiro ramo
    [2, 9, -1],      # segundo ramo
    [0, -2, 4]       # terceiro ramo
]

# Executa o Minimax com poda alfa-beta
# profundidade=2 (considera filhos imediatos), maximizando=True (começa maximizador)
# alfa=-inf, beta=inf (valores iniciais de poda)
print("Busca Competitiva (Minimax c/ Alfa-Beta):", minimax(arvore, 2, True, float('-inf'), float('inf')))


'''
Explicação resumida do funcionamento

- Minimax é usado em jogos competitivos de dois jogadores (maximizador vs minimizador).

- Recursão: Cada nível da árvore alterna entre maximizador e minimizador. Folhas contêm valores do jogo (pontuações finais).

- Alfa-beta: 
alfa = melhor valor encontrado até agora para o maximizador
beta = melhor valor encontrado até agora para o minimizador
Se beta <= alfa, o ramo pode ser podado, economizando cálculo.

Retorna o valor ótimo do jogo a partir da raiz, considerando decisões de ambos os jogadores.
'''