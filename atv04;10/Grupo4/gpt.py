import random

def rolar_d20():
    return random.randint(1, 20)

def calcular_utilidade(acao, reacao, hp):
    threat = 0
    if acao == "Risky Escape":
        threat += 1
    elif acao == "Stealth":
        threat -= 1

    if reacao == "Agressiva":
        threat += 2

    d20_sobrev = rolar_d20()
    d20_dano = rolar_d20()
    perdeu_membro = False
    morreu = False

    # Resultado da sobrevivência
    if d20_sobrev == 14:
        resultado = "Ileso"
    elif d20_sobrev == 10:
        perdeu_membro = True
        resultado = "Perdeu membro"
    elif d20_sobrev < 10:
        morreu = True
        resultado = "Morte"
    else:
        # Continua e sofre dano
        dano = 0
        if d20_dano == 6:
            dano = 2
        elif d20_dano == 10:
            dano = 5
        elif d20_dano == 20:
            morreu = True
            resultado = "Morte instantânea"
        else:
            resultado = "Ferido"
        dano += threat
        hp -= max(dano, 0)

    # Calcula utilidade
    if morreu:
        util = -1000
        hp_final = 0
    elif perdeu_membro:
        util = 1000 - 150 + hp
        hp_final = hp
    else:
        util = 1000 + hp
        hp_final = hp

    return {
        "acao": acao,
        "reacao": reacao,
        "d20_sobrev": d20_sobrev,
        "d20_dano": d20_dano,
        "resultado": resultado,
        "hp_final": hp_final,
        "utilidade": util
    }

# --- Simulação competitiva (jogador vs monstros) ---
acoes = ["Risky Escape", "Stealth", "Fight"]
reacoes = ["Agressiva", "Cautelosa"]
hp_inicial = 30

melhor_acao = None
melhor_utilidade = -float("inf")
melhor_resultado = None

for acao in acoes:
    pior_utilidade = float("inf")
    pior_resultado = None
    for reacao in reacoes:
        res = calcular_utilidade(acao, reacao, hp_inicial)
        if res["utilidade"] < pior_utilidade:
            pior_utilidade = res["utilidade"]
            pior_resultado = res
    # Aventureiro escolhe a melhor entre as piores (max-min)
    if pior_utilidade > melhor_utilidade:
        melhor_utilidade = pior_utilidade
        melhor_resultado = pior_resultado
        melhor_acao = acao

# Exibição final
print("=== Resultado da Simulação ===")
print(f"Ação escolhida pelo aventureiro: {melhor_resultado['acao']}")
print(f"Reação escolhida pelos monstros: {melhor_resultado['reacao']}")
print(f"Rolagem 1 (sobrevivência): {melhor_resultado['d20_sobrev']}")
print(f"Rolagem 2 (dano): {melhor_resultado['d20_dano']}")
print(f"Desfecho: {melhor_resultado['resultado']}")
print(f"HP final: {melhor_resultado['hp_final']}")
print(f"Utilidade final: {melhor_resultado['utilidade']}")
