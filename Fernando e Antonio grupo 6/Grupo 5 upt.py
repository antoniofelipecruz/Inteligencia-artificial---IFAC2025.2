import random
from collections import deque
import time
import os

# --- Configurações do Jogo (Dificultado) ---
GRID_SIZE = 25 # Aumento do tamanho do labirinto (antes era 15)
MAZE_DENSITY = 0.3 # 30% de chance de uma célula ser parede
DELAI_PASSO = 0.25 # Tempo de espera reduzido (antes era 0.5)

# --- Símbolos do Labirinto ---
PATH = 0 # Caminho Livre (célula vazia no código)
WALL = 1 # Parede
PLAYER = 'J'
TREASURE = 'T'
ENEMY = 'E1' # Inimigo 1
ENEMY2 = 'E2' # NOVO: Inimigo 2
VISITED_PATH = '.' # Caminho percorrido pelo jogador
SHORTEST_PATH = '*' # O caminho mais curto (opcional na visualização)

# --- Funções de Ajuda ---

def clear_screen():
    """Limpa a tela do console para a animação."""
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_maze(size, density):
    """Gera um labirinto aleatório e posiciona J, T e os Es."""
    
    # 1. Gera a grade base
    maze = [[PATH] * size for _ in range(size)]
    
    # 2. Adiciona as paredes
    for r in range(size):
        for c in range(size):
            # Garante bordas de parede e distribui paredes aleatórias no interior
            if r == 0 or r == size - 1 or c == 0 or c == size - 1 or random.random() < density:
                maze[r][c] = WALL

    # 3. Encontra posições válidas para J, T, E1 e E2 (caminho livre)
    free_cells = [(r, c) for r in range(size) for c in range(size) if maze[r][c] == PATH]
    
    # NOVO: Precisa de 4 células livres
    if len(free_cells) < 4:
        return None, None, None, None, None

    # Seleciona 4 posições únicas aleatórias
    random.shuffle(free_cells)
    
    # Posições de Player (J), Treasure (T) e Inimigos (E1, E2)
    pos_player = free_cells.pop()
    pos_treasure = free_cells.pop()
    pos_enemy1 = free_cells.pop()
    pos_enemy2 = free_cells.pop() # NOVO
    
    # Atualiza o labirinto
    r_j, c_j = pos_player
    r_t, c_t = pos_treasure
    r_e1, c_e1 = pos_enemy1
    r_e2, c_e2 = pos_enemy2 # NOVO
    
    maze[r_j][c_j] = PLAYER
    maze[r_t][c_t] = TREASURE
    maze[r_e1][c_e1] = ENEMY
    maze[r_e2][c_e2] = ENEMY2 # NOVO
    
    # Retorna a posição do novo inimigo
    return maze, pos_player, pos_treasure, pos_enemy1, pos_enemy2

def print_maze(maze, step, status):
    """Imprime o labirinto no console."""
    clear_screen()
    
    size = len(maze)
    print("--- CAÇA AO TESOURO BFS (NÍVEL DIFÍCIL) ---")
    print(f"Passo: {step}")
    print(f"Status: {status}\n")
    
    for r in range(size):
        row_display = []
        for c in range(size):
            cell = maze[r][c]
            if cell == WALL:
                row_display.append('#') # Caractere para Parede
            elif cell == PLAYER:
                row_display.append('\033[92mJ\033[0m') # Verde para Jogador
            elif cell == TREASURE:
                row_display.append('\033[93mT\033[0m') # Amarelo para Tesouro
            elif cell == ENEMY or cell == ENEMY2: # Ambos os inimigos em vermelho
                row_display.append('\033[91mE\033[0m') # Vermelho para Inimigos
            elif cell == VISITED_PATH:
                row_display.append('.') # Caminho visitado (deixa claro que não é PATH)
            else:
                row_display.append(' ') # Caminho Livre
        print(' '.join(row_display))
    print("---------------------------\n")


def bfs_shortest_path(maze, start, end):
    """
    Implementação do BFS para encontrar o caminho mais curto.
    Retorna o caminho como uma lista de coordenadas [(r1, c1), (r2, c2), ...].
    """
    rows, cols = len(maze), len(maze[0])
    # Fila: armazena tuplas (posição, caminho_ate_aqui)
    queue = deque([(start, [start])])
    # Conjunto para rastrear células visitadas (evita loops e reexploração)
    visited = {start}
    
    # Movimentos possíveis (Cima, Baixo, Esquerda, Direita)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # dr, dc

    while queue:
        (r, c), path = queue.popleft()

        # Se o destino for encontrado
        if (r, c) == end:
            return path[1:] # Retorna o caminho sem a posição inicial

        # Explora vizinhos
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Verifica se o vizinho é válido (dentro da grade)
            if 0 <= nr < rows and 0 <= nc < cols:
                next_pos = (nr, nc)
                cell_content = maze[nr][nc]
                
                is_valid_move = False
                if cell_content == PATH:
                    is_valid_move = True
                elif next_pos == end:
                    is_valid_move = True
                # O PLAYER ('J') também deve poder andar sobre o caminho visitado ('.') no labirinto
                elif cell_content == VISITED_PATH:
                    is_valid_move = True
                
                if is_valid_move and next_pos not in visited:
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append((next_pos, new_path))
    
    return None # Nenhum caminho encontrado

# --- Lógica Principal do Jogo ---

def main_game_loop():
    # 1. Inicializa o Labirinto
    # A função generate_maze agora retorna 5 valores
    maze, pos_j, pos_t, pos_e1, pos_e2 = generate_maze(GRID_SIZE, MAZE_DENSITY)
    if not maze:
        print("Erro: Não foi possível gerar o labirinto com células livres suficientes.")
        return

    step_count = 0
    game_over = False
    
    # 2. Inicia o Loop do Jogo
    while not game_over:
        step_count += 1
        
        # --- Lógica do Jogador (J) ---
        
        # A. Encontra o caminho mais curto de J até T
        path_j_to_t = bfs_shortest_path(maze, pos_j, pos_t)

        status = "Em jogo. J moveu para o Tesouro. E1 e E2 movem para J."
        
        if path_j_to_t:
            # Pega o próximo passo do caminho mais curto
            next_move_j = path_j_to_t[0]
            r_next_j, c_next_j = next_move_j
            
            # 1. Marca a posição atual do Jogador como Caminho Visitado
            r_j, c_j = pos_j
            if maze[r_j][c_j] == PLAYER:
                maze[r_j][c_j] = VISITED_PATH
            
            # 2. Move o Jogador
            pos_j = next_move_j
            r_j, c_j = pos_j

            # 3. Verifica Condição de Vitória
            if maze[r_j][c_j] == TREASURE:
                maze[r_j][c_j] = PLAYER # Posiciona J no T
                print_maze(maze, step_count, "\033[92mVITÓRIA!\033[0m O jogador encontrou o Tesouro!")
                game_over = True
                break
            
            # 4. Atualiza a nova posição no mapa
            maze[r_j][c_j] = PLAYER
        
        else:
            # Se J não consegue mais encontrar T (está preso)
            print_maze(maze, step_count, "\033[93mFIM DE JOGO.\033[0m O jogador está preso e não consegue alcançar o Tesouro.")
            game_over = True
            break
            
        # --- Lógica do Inimigo 1 (E1) ---
        
        # B1. Encontra o caminho mais curto de E1 até J (perseguição)
        path_e1_to_j = bfs_shortest_path(maze, pos_e1, pos_j)

        if path_e1_to_j:
            next_move_e1 = path_e1_to_j[0]
            
            # 1. Marca a posição atual de E1
            r_e1, c_e1 = pos_e1
            if maze[r_e1][c_e1] == ENEMY:
                # Restaura para VISITED_PATH se foi um caminho visitado, senão PATH
                maze[r_e1][c_e1] = VISITED_PATH if (r_e1, c_e1) in [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if maze[r][c] == VISITED_PATH] else PATH
            
            # 2. Move o Inimigo 1
            pos_e1 = next_move_e1
            r_e1, c_e1 = pos_e1
            
            # 3. Verifica Condição de Derrota
            if pos_e1 == pos_j:
                maze[r_e1][c_e1] = ENEMY
                print_maze(maze, step_count, "\033[91mDERROTA!\033[0m O Inimigo 1 atacou o Jogador.")
                game_over = True
                break
            
            # 4. Atualiza a nova posição no mapa
            maze[r_e1][c_e1] = ENEMY

        # --- Lógica do Inimigo 2 (E2) ---
        
        # B2. Encontra o caminho mais curto de E2 até J (perseguição)
        if not game_over:
            path_e2_to_j = bfs_shortest_path(maze, pos_e2, pos_j)

            if path_e2_to_j:
                next_move_e2 = path_e2_to_j[0]
                
                # 1. Marca a posição atual de E2
                r_e2, c_e2 = pos_e2
                if maze[r_e2][c_e2] == ENEMY2:
                    # Restaura para VISITED_PATH se foi um caminho visitado, senão PATH
                    maze[r_e2][c_e2] = VISITED_PATH if (r_e2, c_e2) in [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if maze[r][c] == VISITED_PATH] else PATH
                
                # 2. Move o Inimigo 2
                pos_e2 = next_move_e2
                r_e2, c_e2 = pos_e2
                
                # 3. Verifica Condição de Derrota
                if pos_e2 == pos_j:
                    maze[r_e2][c_e2] = ENEMY2
                    print_maze(maze, step_count, "\033[91mDERROTA!\033[0m O Inimigo 2 atacou o Jogador.")
                    game_over = True
                    break
                
                # 4. Atualiza a nova posição no mapa
                # Se E2 não caiu em J, atualiza (E1 tem prioridade na exibição se estiver na mesma célula)
                if pos_e2 != pos_e1 and pos_e2 != pos_j:
                    maze[r_e2][c_e2] = ENEMY2
            
            # 3. Imprime e Espera
            if not game_over:
                
                # Garante que Tesouro (T) e Inimigo 1 (E1) não sejam sobrescritos
                r_t, c_t = pos_t
                if maze[r_t][c_t] != PLAYER:
                    maze[r_t][c_t] = TREASURE
                
                # Garante que o Inimigo 1 não seja sobrescrito (se for o caso de E2 ter caído em E1)
                if maze[pos_e1[0]][pos_e1[1]] != PLAYER:
                    maze[pos_e1[0]][pos_e1[1]] = ENEMY

                print_maze(maze, step_count, status)
                time.sleep(DELAI_PASSO)


# Executa o Jogo
if __name__ == "__main__":
    try:
        main_game_loop()
    except KeyboardInterrupt:
        print("\nJogo encerrado pelo usuário.")