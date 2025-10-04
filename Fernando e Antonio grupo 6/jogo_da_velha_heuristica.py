def print_tabuleiro(tab):
    for i in range(3):
        print(" | ".join(tab[i]))
        if i < 2:
            print("-" * 5)

def checa_vencedor(tab, jogador):
    # Linhas
    for linha in tab:
        if all(s == jogador for s in linha):
            return True
    # Colunas
    for c in range(3):
        if all(tab[l][c] == jogador for l in range(3)):
            return True
    # Diagonais
    if all(tab[i][i] == jogador for i in range(3)):
        return True
    if all(tab[i][2 - i] == jogador for i in range(3)):
        return True
    return False

def computador_joga(tab, computador):
    # Tenta completar linha, coluna ou diagonal onde já tem 2 peças e 1 vazia
    # 1. Linhas
    for i in range(3):
        linha = tab[i]
        if linha.count(computador) == 2 and linha.count(" ") == 1:
            j = linha.index(" ")
            tab[i][j] = computador
            return

    # 2. Colunas
    for j in range(3):
        coluna = [tab[i][j] for i in range(3)]
        if coluna.count(computador) == 2 and coluna.count(" ") == 1:
            i = coluna.index(" ")
            tab[i][j] = computador
            return

    # 3. Diagonal principal
    diag_principal = [tab[i][i] for i in range(3)]
    if diag_principal.count(computador) == 2 and diag_principal.count(" ") == 1:
        i = diag_principal.index(" ")
        tab[i][i] = computador
        return

    # 4. Diagonal secundária
    diag_sec = [tab[i][2 - i] for i in range(3)]
    if diag_sec.count(computador) == 2 and diag_sec.count(" ") == 1:
        i = diag_sec.index(" ")
        tab[i][2 - i] = computador
        return

    # Se não encontrou nenhuma chance de completar, joga na primeira posição vazia
    for i in range(3):
        for j in range(3):
            if tab[i][j] == " ":
                tab[i][j] = computador
                return

def jogo_da_velha():
    tabuleiro = [[" "]*3 for _ in range(3)]
    jogador_humano = "X"
    computador = "O"
    jogador_atual = "X"
    jogadas = 0

    while True:
        print_tabuleiro(tabuleiro)

        if jogador_atual == jogador_humano:
            print(f"Vez do jogador {jogador_atual}. Escolha linha e coluna (0, 1 ou 2):")
            try:
                linha = int(input("Linha: "))
                coluna = int(input("Coluna: "))
            except ValueError:
                print("Por favor, digite números válidos.")
                continue
            if linha not in [0,1,2] or coluna not in [0,1,2]:
                print("Coordenadas inválidas! Use 0, 1 ou 2.")
                continue
            if tabuleiro[linha][coluna] != " ":
                print("Posição já ocupada! Tente outra.")
                continue

            tabuleiro[linha][coluna] = jogador_humano
        else:
            print("Vez do computador...")
            computador_joga(tabuleiro, computador)

        jogadas += 1

        if checa_vencedor(tabuleiro, jogador_atual):
            print_tabuleiro(tabuleiro)
            if jogador_atual == jogador_humano:
                print("Você venceu! 🎉")
            else:
                print("Computador venceu! 💻")
            break

        if jogadas == 9:
            print_tabuleiro(tabuleiro)
            print("Empate!")
            break

        jogador_atual = computador if jogador_atual == jogador_humano else jogador_humano

if __name__ == "__main__":
    jogo_da_velha()
